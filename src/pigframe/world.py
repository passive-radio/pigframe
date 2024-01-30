"""
This module contains `World` class which is the core of the game, 
and `System`, `Screen`, `Event` classes which are the base systems 
in the context of ECS (Entity Component System).
"""
from typing import Type
from dataclasses import dataclass
from .level import LevelManager
from abc import ABCMeta, abstractmethod

@dataclass
class Component(metaclass=ABCMeta):
    """Base class for components."""

class System(metaclass=ABCMeta):
    """System is a class which has a process method. The process method is executed every frame.
    """
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        """System is a class which has a process method. The process method is executed every frame.

        Parameters
        ----------
        world : World
            World object
        priority : int, optional
            system with its lower priority than the other systems is executed in advance., by default 0
        """
        self.world: World = world
        self.priority = priority
    
    @abstractmethod
    def process(self):
        """Process method is executed every frame."""

class Event(System, metaclass=ABCMeta):
    """Event is a class which has a process method. 
    The process method is executed when the event is trigered.
    """
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        """Event is a class which has a process method. 
        The process method is executed when the event is trigered.

        Parameters
        ----------
        world : World
            World object
        event_name : str
            name of event
        priority : int, optional
            event with its lower priority than the others events is executed in advance., by default 0
        """
        super().__init__(world, priority, **kwargs)
    
    def process(self):
        if self.world.level_manager.scenes_events[self.world.current_scene][type(self)]["run"] != 1:
            return
        
        self.__process()
        self.world.level_manager.scenes_events[self.world.current_scene][type(self)]["run"] = 0
    
    @abstractmethod
    def __process(self):
        pass
    
class Screen(metaclass=ABCMeta):
    """Screen is a class which has a draw method. 
    The draw method is executed every frame.
    """
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        """Screen is a class which has a draw method. The draw method is executed every frame.

        Parameters
        ----------
        world : World
            World object
        priority : int, optional
            system with its lower priority than the other systems is executed in advance., by default 0
        """
        self.world: World = world
        self.priority = priority
    
    @abstractmethod
    def draw(self):
        pass

class World(metaclass=ABCMeta):
    """World is a class which has entities, components, systems, screens.
    """
    def __init__(self):
        """World is a class which has entities, components, systems, screens. 
        It is the core of the game.
        """
        self.components = {}
        self.entities = {}
        self.next_entity_id = 0
        self.scene_systems: dict[list[System]] = {}
        self.scene_screens: dict[list[Screen]] = {}
        self.scene_events: dict[list[Event]] = {}
        self._get_component_cache = {}
        self._get_components_cache = {}
        self.level_manager = LevelManager()
        
    def create_entity(self,):
        """Create an entity.

        Returns
        -------
        _type_
            int: entity id
        """
        entity = self.next_entity_id
        self.next_entity_id += 1
        return entity
    
    def add_component_to_entity(self, entity: int, component_type: type(Component), **kwargs) -> None:
        """Add a component to an entity.
        
        Add entity id in the components[component_type] set where every entities 
        which have the component: component_type is stored.
        Add component in the entities[entity] dict where every components 
        which consists the entit stored.
        
        Parameters
        ----------
        entity : int
            entity id
        component : Component
            component to be added
        """
        component = component_type(**kwargs)
        if component_type not in self.components:
            self.components[component_type] = set()
        
        if entity not in self.entities:
            self.entities[entity] = {}
            
        self.components[component_type].add(entity)
        self.entities[entity].setdefault(component_type, component)
        
    def get_entity_object(self, entity: int):
        """Get entity object.

        Parameters
        ----------
        entity : int
            entity id

        Returns
        -------
        _type_
            dict: entity object
                key: component type
                value: component
        """
        return self.entities[entity]
    
    def _get_component(self, component_type: type(Component)):
        """Get component.

        Parameters
        ----------
        component_type : Component
            component type

        Yields
        ------
        _type_
            tuple: entity id, component
        """
        for entity in self.components.get(component_type):
            yield entity, self.entities[entity][component_type]

    def get_component(self, component_type: type(Component)):
        """Get component.

        Parameters
        ----------
        component_type : Component
            component type

        Returns
        -------
        _type_
            list: list of tuple: entity id, component
        """
        return self._get_component_cache.setdefault(component_type, list(
            self._get_component(component_type))
            )
    
    def _get_components(self, *component_types: list[type(Component)]):
        """Get components.

        Yields
        ------
        _type_
            tuple: entity id, list of components
        """
        for entity in set.intersection(*[self.components[ct] for ct in component_types]):
            yield entity, [self.entities[entity][ct] for ct in component_types]
        
    def get_components(self, *component_types: list[type(Component)]):
        """Get components.

        Returns
        -------
        _type_
            list: list of tuple: entity id, list of components
        """
        return self._get_components_cache.setdefault(component_types, list(self._get_components(*component_types)))
    
    def add_scene(self, scene: str):
        """Add a scene to world.

        Parameters
        ----------
        scene : str
            name of scene
        """
        self.level_manager.add_scene(scene)
        
    def add_scenes(self, scenes: list[str]):
        """Add scenes to world.

        Parameters
        ----------
        scenes : list[str]
            names of scenes
        """
        self.level_manager.add_scenes(scenes)
        
    def add_scene_transition(self, scene_from: str, scene_to: str, triger: callable):
        """Add a scene transition to world.

        Parameters
        ----------
        scene_from : str
            name of scene
        scene_to : str
            name of scene to be transitioned
        triger : callable
            triger of transition
        """
        self.level_manager.add_scene_transition(scene_from, scene_to, triger)
        
    def add_scene_event_transition(self, scene: str, event_type: type(Event), triger: callable):
        """Add an event info to a scene of world.

        Parameters
        ----------
        scene : str
            name of scene
        event_type : str
            name of event
        triger : callable
            triger of event
        """
        self.level_manager.add_scene_event(scene, event_type, triger)
        
    def add_system_to_scenes(self, system_type: type(System), scenes: list[str] | str, priority: int = 0, **kwargs):
        """Add a system to scenes of world. Be sure you have added scenes before adding systems.

        Parameters
        ----------
        system : type(System)
            type of system to be added. It must be a type of subclass of System. 
            System instance is created automatically.
        scenes : list[str], optional
            scenes where the system is executed, by default None
        priority : int, optional
            system with its lower priority than the other systems is executed in advance., by default 0
        """
        system_type: Type[System]
        system = system_type(self, priority, **kwargs)
        
        if type(scenes) == str:
            scene = scenes
            if self.scene_systems.get(scene) is None:
                self.scene_systems.update({scene: []})
            self.scene_systems[scene].append(system)
            self.scene_systems[scene] = sorted(self.scene_systems[scene], key=lambda x: x.priority)
            return
        
        for scene in scenes:
            if self.scene_systems.get(scene) is None:
                self.scene_systems.update({scene: []})
            self.scene_systems[scene].append(system)
            self.scene_systems[scene] = sorted(self.scene_systems[scene], key=lambda x: x.priority)
            
    def add_system(self, system_type: type(System), priority: int = 0, **kwargs) -> None:
        """Add a system to all scenes of world. Be sure you have added scenes before adding systems.

        Parameters
        ----------
        system : System
            system to be added
        priority : int, optional
            system with its lower priority than the other systems is executed in advance., by default 0
        """
        scenes = self.scenes
        self.add_system_to_scenes(system_type, scenes, priority, **kwargs)
        
    def add_screen_to_scenes(self, screen_type: type(Screen), scenes: list[str] | str, priority: int = 0, **kwargs):
        """Add a screen to scenes of world. Be sure you have added scenes before adding screens.

        Parameters
        ----------
        screen_type : type(Screen)
            type of screen to be added. It must be a type of subclass of Screen. 
            Screen instance is created automatically.
        scenes : list[str], optional
            scenes where the screen is executed, by default None
        priority : int, optional
            screen with its lower priority than the other screens is executed in advance., by default 0
        """
        
        screen = screen_type(self, priority, **kwargs)
        
        if type(scenes) == str:
            scene = scenes
            if self.scene_screens.get(scene) is None:
                self.scene_screens.update({scene: []})
            self.scene_screens[scene].append(screen)
            self.scene_screens[scene] = sorted(self.scene_screens[scene], key=lambda x: x.priority)
            return
        
        for scene in scenes:
            if self.scene_screens.get(scene) is None:
                self.scene_screens.update({scene: []})
            self.scene_screens[scene].append(screen)
            self.scene_screens[scene] = sorted(self.scene_screens[scene], key=lambda x: x.priority)
            
    def add_screen(self, screen_type: type(Screen), priority: int = 0, **kwargs) -> None:
        """Add a screen to all scenes of world. Be sure you have added scenes before adding screens.

        Parameters
        ----------
        screen_type : type(Screen)
            type of screen to be added. It must be a type of subclass of Screen. 
            Screen instance is created automatically.
        priority : int, optional
            screen with its lower priority than the other screens is executed in advance., by default 0
        """
        scenes = self.scenes
        self.add_screen_to_scenes(screen_type, scenes, priority, **kwargs)
        
    def add_event_to_scene(self, event_type: type(Event), scene: str, triger: callable, priority: int = 0, **kwargs):
        """Add an event to a scene of world. Be sure you have added scenes before adding events.

        Parameters
        ----------
        event_type : type(Event)
            event to be added. It must be a type of subclass of Event. 
            Event instance is created automatically.
        scene : str
            scene where the event is executed
        triger : callable
            triger of event. It must be a callable object.
        priority : int, optional
            event with its lower priority than the other events is executed in advance., by default 0
        """
        event = event_type(self, priority, **kwargs)
        
        if self.scene_events.get(scene) is None:
            self.scene_events.update({scene: []})
            
        self.add_scene_event_transition(scene, event_type, triger)
        self.scene_events[scene].append(event)
        self.scene_events[scene] = sorted(self.scene_events[scene], key=lambda x: x.priority)
        
    def add_event(self, event_type: type(Event), priority: int = 0, **kwargs):
        """Add an event to all scenes of world. Be sure you have added scenes before adding events.

        Parameters
        ----------
        event_type : type(Event)
            type of event to be added. It must be a type of subclass of Event. 
            Event instance is created automatically.
        priority : int, optional
            event with its lower priority than the other events is executed in advance., by default 0
        """
        scenes = self.scenes
        self.add_event_to_scene(event_type, scenes, priority, **kwargs)
        
    def process_systems(self):
        """Process all systems in the current scene of world. 
        Be sure you have added scenes before processing systems.
        """
        if self.scene_systems.get(self.current_scene) is None:
            return
        for system in self.scene_systems[self.current_scene]:
            system: System
            system.process()
            
    def process_screens(self):
        """Draw all screens in the current scene of world. 
        Be sure you have added scenes before drawing screens.
        """
        if self.scene_screens.get(self.current_scene) is None:
            return
        for screen in self.scene_screens[self.current_scene]:
            screen: Screen
            screen.draw()

    def process_events(self):
        """Process all events in the current scene of world. 
        Be sure you have added scenes before processing events.
        """
        if self.scene_events.get(self.current_scene) is None:
            return
        for event in self.scene_events[self.current_scene]:
            event: Event
            event.process()
            
    def process(self):
        """Process all systems, screens, events in the current scene of world.
        Be sure you have added scenes before processing.
        """
        self.process_systems()
        self.level_manager.process()
        self.process_events()
        
    def has_component(self, entity: int, component_type: type(Component)):
        """Check if an entity has a component.

        Parameters
        ----------
        entity : int
            entity id
        component_type : type(Component)
            component type

        Returns
        -------
        _type_
            bool: True if the entity has the component, False otherwise
        """
        return component_type in self.entities[entity]
    
    def remove_entity(self, entity: int):
        """Remove an entity from world.

        Parameters
        ----------
        entity : int
            entity id
        """
        for component_type in self.entities[entity]:
            self.components[component_type].remove(entity)
            
        del self.entities[entity]
        
    def remove_system_from_scene(self, system_type: type(System), scenes: list[str] | str):
        """Remove a system from scenes of world.

        Parameters
        ----------
        system_type : type
            type of system to be removed
        scenes : list[str] | str
            scenes where the system is removed
        """
        if type(scenes) == str:
            scenes = [scenes]
        
        for scene in scenes:
            if self.scene_systems.get(scene) is None:
                assert("scene not found!")
                continue
            for system in self.scene_systems[scene]:
                if type(system) is system_type:
                    self.scene_systems[scene].remove(system)
    
    def remove_system(self, system_type: type(System)):
        """Remove a system from all scenes of world.

        Parameters
        ----------
        system_type : type(System)
            type of system to be removed
        """
        scenes = self.scenes
        for scene in scenes:
            if self.scene_systems.get(scene) is None:
                assert("scene not found!")
                continue
            for system in self.scene_systems[scene]:
                if type(system) is system_type:
                    self.scene_systems[scene].remove(system)
                    
    def remove_screen_from_scene(self, screen_type: type(Screen), scenes: list[str] | str):
        """Remove a screen from scenes of world.

        Parameters
        ----------
        screen_type : type
            type of screen to be removed
        scenes : list[str] | str
            scenes where the screen is removed
        """
        if type(scenes) == str:
            scenes = [scenes]
        
        for scene in scenes:
            if self.scene_screens.get(scene) is None:
                assert("scene not found!")
                continue
            for screen in self.scene_screens[scene]:
                if type(screen) is screen_type:
                    self.scene_screens[scene].remove(screen)
    
    def remove_event_from_scene(self, event_type: type(Event), scenes: list[str] | str):
        """Remove an event from scenes of world.

        Parameters
        ----------
        event_type : type
            type of event to be removed
        scenes : list[str] | str
            scenes where the event is removed
        """
        if type(scenes) == str:
            scenes = [scenes]
        
        for scene in scenes:
            if self.scene_events.get(scene) is None:
                assert("scene not found!")
                continue
            for event in self.scene_events[scene]:
                if type(event) is event_type:
                    self.scene_events[scene].remove(event)
        
    @property
    def scenes(self):
        """Return all scenes of world.

        Returns
        -------
        _type_
            list[str]: names of all scenes
        """
        return self.level_manager.scenes
    
    @property
    def current_scene(self):
        """Return current scene of world.

        Returns
        -------
        _type_
            str: current scene name
        """
        return self.level_manager.current_scene
    
    @property
    def next_scene(self):
        """Return next scene of world.

        Returns
        -------
        _type_
            str: next scene name
        """
        return self.level_manager.next_scene
    
    @property
    def prev_scene(self):
        """Return previous scene of world.

        Returns
        -------
        _type_
            str: previous scene name
        """
        return self.level_manager.prev_scene
    
    @property
    def current_systems(self):
        """Return systems of current scene of world.

        Returns
        -------
        _type_
            list[System]: systems of current scene
        """
        return self.scene_systems[self.current_scene]
    
    @property
    def current_screens(self):
        """Return screens of current scene of world.

        Returns
        -------
        _type_
            list[Screen]: screens of current scene
        """
        return self.scene_screens[self.current_scene]
    
    @property
    def current_events(self):
        """Return events of current scene of world.

        Returns
        -------
        _type_
            list[Event]: events of current scene
        """
        return self.scene_events[self.current_scene]
    
    @property
    def systems(self):
        """Return systems of world.

        Returns
        -------
        _type_
            dict[list[System]]: systems of world
        """
        return self.scene_systems
    
    @property
    def screens(self):
        """_summary_

        Returns
        -------
        _type_
            dict[list[Screen]]: screens of world
        """
        return self.scene_screens
    
    @current_scene.setter
    def current_scene(self, scene: str):
        """Set current scene of world.

        Parameters
        ----------
        scene : str
            name of scene
        """
        self.level_manager.current_scene = scene