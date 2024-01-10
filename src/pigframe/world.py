from typing import Type
from dataclasses import dataclass
from .level import LevelManager

version = '0.0.1'

class System():
    def __init__(self, world, priority: int = 0) -> None:
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
        
    def process(self):
        pass
    
class Screen():
    def __init__(self, world, priority: int = 0) -> None:
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
        
    def draw(self):
        pass
    
@dataclass
class Component:
    """Base class for components."""
    

class World():
    def __init__(self):
        """World is a class which has entities, components, systems, screens. It is the core of the game.
        """
        self.components = {}
        self.entities = {}
        self.next_entity_id = 0
        self.scene_systems: dict[list[System]] = {}
        self.scene_screens: dict[list[Screen]] = {}
        self._get_component_cache = {}
        self._get_components_cache = {}
        self.running = True
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
    
    def add_component_to_entity(self, entity, component) -> None:
        """Add a component to an entity.
        
        Parameters
        ----------
        entity : int
            entity id
        component : Component
            component to be added
        """
        component_type = type(component)
        if component_type not in self.components:
            self.components[component_type] = set()
        
        if entity not in self.entities:
            self.entities[entity] = {}
            
        """
        Add entity id in the components[component_type] set where every entities which have the component: component_type is stored.
        Add component in the entities[entity] dict where every components which consists the entit stored.
        """
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
    
    def _get_component(self, component_type: Component):
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

    def get_component(self, component_type: Component):
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
    
    def _get_components(self, *component_types: list[Component]):
        """Get components.

        Yields
        ------
        _type_
            tuple: entity id, list of components
        """
        for entity in set.intersection(*[self.components[ct] for ct in component_types]):
            yield entity, [self.entities[entity][ct] for ct in component_types]
        
    def get_components(self, *component_types: list[Component]):
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
        
    def add_scene_system(self, system, scenes: list[str], priority: int = 0):
        """Add a system to scenes of world. Be sure you have added scenes before adding systems.

        Parameters
        ----------
        system : System
            system to be added
        scenes : list[str], optional
            scenes where the system is executed, by default None
        priority : int, optional
            system with its lower priority than the other systems is executed in advance., by default 0
        """
        system.priority = priority
        
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
            
    def add_system(self, system, priority: int = 0) -> None:
        """Add a system to all scenes of world. Be sure you have added scenes before adding systems.

        Parameters
        ----------
        system : System
            system to be added
        priority : int, optional
            system with its lower priority than the other systems is executed in advance., by default 0
        """
        scenes = self.scenes
        self.add_scene_system(system, scenes, priority)
        
    def add_scene_screen(self, screen, scenes: list[str], priority: int = 0):
        """Add a screen to scenes of world. Be sure you have added scenes before adding screens.

        Parameters
        ----------
        screen : Screen
            screen to be added
        scenes : list[str], optional
            scenes where the screen is executed, by default None
        priority : int, optional
            screen with its lower priority than the other screens is executed in advance., by default 0
        """
        screen.priority = priority
        
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
            
    def add_screen(self, screen, priority: int = 0) -> None:
        """Add a screen to all scenes of world. Be sure you have added scenes before adding screens.

        Parameters
        ----------
        screen : Screen
            screen to be added
        priority : int, optional
            screen with its lower priority than the other screens is executed in advance., by default 0
        """
        scenes = self.scenes
        self.add_scene_screen(screen, scenes, priority)
        
    def process_systems(self):
        """Process all systems in the current scene of world. Be sure you have added scenes before processing systems.
        """
        for system in self.scene_systems[self.level_manager.current_scene]:
            system: System
            system.process()
            
    def draw_screens(self):
        """Draw all screens in the current scene of world. Be sure you have added scenes before drawing screens.
        """
        for screen in self.scene_screens[self.level_manager.current_scene]:
            screen: Screen
            screen.draw()
        
    def has_component(self, entity: int, component_type: Component):
        """Check if an entity has a component.

        Parameters
        ----------
        entity : int
            entity id
        component_type : Component
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