"""
This module contains `World` class which is the core of the game, 
and `System`, `Screen`, `Event` classes which are the base systems 
in the context of ECS (Entity Component System).
"""

from typing import Type, TYPE_CHECKING, Callable
from dataclasses import asdict, field, make_dataclass
from .scene import SceneManager
from abc import ABCMeta
from .action import ActionMap
from .component import Component
from .object import WorldEntities, WorldComponents

# TYPE_CHECKING imports to avoid circular dependencies
if TYPE_CHECKING:
    from .system import System
    from .event import Event
    from .screen import Screen

class BaseWorld(metaclass=ABCMeta):
    """World is a class which has entities, components, systems, screens."""

    def __init__(self):
        """World is a class which has entities, components, systems, screens.
        It is the core of the game.
        """
        self.components: WorldComponents = WorldComponents(value={})
        self.entities: WorldEntities = WorldEntities(value={})
        self.__next_entity_id = 0
        self.scene_systems: dict[str, list[System]] = {}
        self.scene_screens: dict[str, list[Screen]] = {}
        self.scene_events: dict[str, list[Event]] = {}
        self._get_component_cache = {}
        self._get_components_cache = {}
        self.user_input_event_map = None
        self.scene_manager = SceneManager()

    def create_entity(self, id: int | None = None):
        """Create an entity.

        Returns
        -------
        _type_
            int: entity id
        """
        if id is None:
            entity = self.__next_entity_id
            self.__next_entity_id += 1
        else:
            entity = id
            self.__next_entity_id = id + 1
        return entity

    def add_component_to_entity(
        self, entity: int, component_type: Type[Component], **kwargs
    ) -> None:
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
        if component_type not in self.components.value:
            self.components.value[component_type] = set()

        if entity not in self.entities.value:
            self.entities.value[entity] = {}

        self.components.value[component_type].add(entity)
        self.entities.value[entity].setdefault(component_type, component)

        # Clear cache when a component is added
        self.clear_component_cache()

    def get_entity_object(self, entity: int) -> dict | None:
        """Get entity object.

        Parameters
        ----------
        entity : int
            entity id

        Returns
        -------
        _type_
            dict | None: entity object. If the entity does not exist, return None.
                key: component type
                value: component
        """
        if entity not in self.entities.value:
            return None
        return self.entities.value[entity]

    def _get_component(self, component_type: Type[Component]):
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
        for entity in self.components.value.get(component_type, set()):
            yield entity, self.entities.value[entity][component_type]

    def get_component(self, component_type: Type[Component]):
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
        cache_key = component_type
        if cache_key not in self._get_component_cache:
            self._get_component_cache[cache_key] = list(self._get_component(component_type))

        return self._get_component_cache[cache_key]

    def _get_components(self, *component_types: Type[Component]):
        """Get components.

        Yields
        ------
        _type_
            tuple: entity id, list of components
        """
        for entity in set.intersection(*[self.components.value[ct] for ct in component_types]):
            yield entity, [self.entities.value[entity][ct] for ct in component_types]

    def get_components(self, *component_types: Type[Component]):
        """Get components.

        Returns
        -------
        _type_
            list: list of tuple: entity id, list of components
        """
        cache_key = tuple(component_types)
        if cache_key not in self._get_components_cache:
            self._get_components_cache[cache_key] = list(self._get_components(*component_types))
        return self._get_components_cache[cache_key]

    def clear_component_cache(self):
        """Clear the component cache.
        Call this method when components are added, removed, or modified.
        """
        self._get_component_cache.clear()
        self._get_components_cache.clear()

    def component_exist(self, component_type: Type[Component]):
        """Check if component exist.

        Parameters
        ----------
        component_type : Type[Component]
            component type

        Returns
        -------
        _type_
            bool: True if component exist, False otherwise
        """
        if component_type not in self.components.value:
            return False

        if len(self.components.value[component_type]) == 0:
            return False

        return True

    def components_exist(self, *component_types: Type[Component]):
        """Check if components exist.

        Parameters
        ----------
        component_types : Type[Component]
            component types
        """
        return all(self.component_exist(component_type) for component_type in component_types)

    def set_of_components_exist(self, component_types: list[Type[Component]]):
        """Check if there's at least one entity that has given set of components.

        Parameters
        ----------
        component_types : list[Type[Component]]
            component types
        """
        return len(set.intersection(*[self.components.value[ct] for ct in component_types])) > 0

    def add_scene(self, scene: str):
        """Add a scene to world.

        Parameters
        ----------
        scene : str
            name of scene
        """
        self.scene_manager.add_scene(scene)

    def add_scenes(self, scenes: list[str]):
        """Add scenes to world.

        Parameters
        ----------
        scenes : list[str]
            names of scenes
        """
        self.scene_manager.add_scenes(scenes)

    def add_scene_transition(self, scene_from: str, scene_to: str, triger: Callable):
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
        self.scene_manager.add_scene_transition(scene_from, scene_to, triger)

    def add_scene_event_transition(self, scene: str, event_type: Type["Event"], triger: Callable):
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
        self.scene_manager.add_scene_event(scene, event_type, triger)

    def add_system_to_scenes(
        self, system_type: Type["System"], scenes: list[str] | str, priority: int = 0, **kwargs
    ):
        """Add a system to scenes of world. Be sure you have added scenes before adding systems.

        Parameters
        ----------
        system_type : Type["System"]
            type of system to be added. It must be a type of subclass of System.
            System instance is created automatically.
        scenes : list[str], optional
            scenes where the system is executed, by default None
        priority : int, optional
            system with its lower priority than the other systems is executed in advance., by default 0
        """
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

    def add_system(self, system_type: Type["System"], priority: int = 0, **kwargs) -> None:
        """Add a system to all scenes of world. Be sure you have added scenes before adding systems.

        Parameters
        ----------
        system_type : Type["System"]
            type of system to be added. It must be a type of subclass of System.
            System instance is created automatically.
        priority : int, optional
            system with its lower priority than the other systems is executed in advance., by default 0
        """
        scenes = list(self.scenes)
        self.add_system_to_scenes(system_type, scenes, priority, **kwargs)

    def add_screen_to_scenes(
        self, screen_type: Type["Screen"], scenes: list[str] | str, priority: int = 0, **kwargs
    ):
        """Add a screen to scenes of world. Be sure you have added scenes before adding screens.

        Parameters
        ----------
        screen_type : Type["Screen"]
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

    def add_screen(self, screen_type: Type["Screen"], priority: int = 0, **kwargs) -> None:
        """Add a screen to all scenes of world. Be sure you have added scenes before adding screens.

        Parameters
        ----------
        screen_type : Type["Screen"]
            type of screen to be added. It must be a type of subclass of Screen.
            Screen instance is created automatically.
        priority : int, optional
            screen with its lower priority than the other screens is executed in advance., by default 0
        """
        scenes = list(self.scenes)
        self.add_screen_to_scenes(screen_type, scenes, priority, **kwargs)

    def add_event_to_scene(
        self, event_type: Type["Event"], scene: str, triger: Callable, priority: int = 0, **kwargs
    ):
        """Add an event to a scene of world. Be sure you have added scenes before adding events.

        Parameters
        ----------
        event_type : Type["Event"]
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

    def add_event(self, event_type: Type["Event"], priority: int = 0, **kwargs):
        """Add an event to all scenes of world. Be sure you have added scenes before adding events.

        Parameters
        ----------
        event_type : Type["Event"]
            type of event to be added. It must be a type of subclass of Event.
            Event instance is created automatically.
        priority : int, optional
            event with its lower priority than the other events is executed in advance., by default 0
        """
        scenes = list(self.scenes)
        for scene in scenes:
            self.add_event_to_scene(event_type, scene, triger=lambda: False, priority=priority, **kwargs)

    def process_systems(self):
        """Process all systems in the current scene of world.
        Be sure you have added scenes before processing systems.
        """
        current = self.current_scene
        if current is None or self.scene_systems.get(current) is None:
            return
        for system in self.scene_systems[current]:
            system.process()

    def process_user_actions(self):
        """Process checking all user actions happened in a frame.
        Be sure you have added user acions definitions first by `set_user_actions_map` method.
        """
        if self.user_input_event_map is None:
            return
        self.update_user_actions()

    def process_screens(self):
        """Draw all screens in the current scene of world.
        Be sure you have added scenes before drawing screens.
        """
        current = self.current_scene
        if current is None or self.scene_screens.get(current) is None:
            return
        for screen in self.scene_screens[current]:
            screen.draw()

    def process_events(self):
        """Process all events in the current scene of world.
        Be sure you have added scenes before processing events.
        """
        current = self.current_scene
        if current is None or self.scene_events.get(current) is None:
            return
        for event in self.scene_events[current]:
            event.process()

    def process(self):
        """Process all systems, screens, events in the current scene of world.
        Be sure you have added scenes before processing.
        """
        self.process_user_actions()
        self.process_systems()
        self.scene_manager.process()
        self.process_events()

    def has_component(self, entity: int, component_type: Type[Component]):
        """Check if an entity has a component.

        Parameters
        ----------
        entity : int
            entity id
        component_type : Type[Component]
            component type

        Returns
        -------
        _type_
            bool: True if the entity has the component, False otherwise
        """
        return component_type in self.entities.value[entity]

    def has_components(self, entity: int, *component_types: Type[Component]):
        """Check if an entity has components.

        Parameters
        ----------
        entity : int
            entity id
        component_types : Type[Component]
            component types
        """
        return all(self.has_component(entity, component_type) for component_type in component_types)

    def remove_entity(self, entity: int) -> bool | None:
        """Remove an entity from world.

        Parameters
        ----------
        entity : int
            entity id

        Returns
        -------
        _type_
            bool | None: True if the entity is removed, None if the entity does not exist
        """
        if entity not in self.entities.value:
            return None

        for component_type in self.entities.value[entity]:
            self.components.value[component_type].remove(entity)

        del self.entities.value[entity]
        self.clear_component_cache()
        return True

    def remove_system_from_scene(self, system_type: Type["System"], scenes: list[str] | str):
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
                assert "scene not found!"
                continue
            for system in self.scene_systems[scene]:
                if type(system) is system_type:
                    self.scene_systems[scene].remove(system)

    def remove_system(self, system_type: Type["System"]):
        """Remove a system from all scenes of world.

        Parameters
        ----------
        system_type : Type["System"]
            type of system to be removed
        """
        scenes = list(self.scenes)
        for scene in scenes:
            if self.scene_systems.get(scene) is None:
                assert "scene not found!"
                continue
            for system in self.scene_systems[scene]:
                if type(system) is system_type:
                    self.scene_systems[scene].remove(system)

    def remove_screen_from_scene(self, screen_type: Type["Screen"], scenes: list[str] | str):
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
                assert "scene not found!"
                continue
            for screen in self.scene_screens[scene]:
                if type(screen) is screen_type:
                    self.scene_screens[scene].remove(screen)

    def remove_event_from_scene(self, event_type: Type["Event"], scenes: list[str] | str):
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
                assert "scene not found!"
                continue
            for event in self.scene_events[scene]:
                if type(event) is event_type:
                    self.scene_events[scene].remove(event)

    def remove_component_from_entity(self, entity: int, component_type: Type[Component]):
        """Remove a component from an entity.

        Parameters
        ----------
        entity : int
            entity id
        component_type : Type[Component]
            component type
        """
        if component_type not in self.entities.value[entity]:
            return
        self.components.value[component_type].remove(entity)
        del self.entities.value[entity][component_type]

    def remove_components_from_entity(self, entity: int, *component_types: Type[Component]):
        """Remove components from an entity.

        Parameters
        ----------
        entity : int
            entity id
        component_types : list[Type[Component]]
            component types
        """
        for component_type in component_types:
            if component_type not in self.entities.value[entity]:
                continue
            self.components.value[component_type].remove(entity)
            del self.entities.value[entity][component_type]

    def set_user_actions_map(self, action_map: Type[ActionMap]):
        """Add user action definitions to the world.

        Parameters
        ----------
        action_map : Type[ActionMap]
            User actions map (e.g. whether mouse left button was clicked or not.) to be added.
            It must be a subclass of ActionMap.
        """
        action_instance = action_map()
        event_dict = asdict(action_instance)
        self.user_input_event_map = event_dict
        events = {}
        for key, value in event_dict.items():
            if not callable(value[0]):
                break
            events.update({key: False})

        self._set_user_actions_map(events)

    def _set_user_actions_map(self, event_results_map: dict[str, bool]):
        """Set user input events to the world."""
        fields = [(key, bool, field(default=value)) for key, value in event_results_map.items()]
        event_results = make_dataclass("EventResults", fields=fields)
        self.actions = event_results

    def update_user_actions(self):
        """Update user input events results.
        if the user input event happened, the result is True, otherwise False.
        """
        if self.user_input_event_map is None:
            return
            
        events = {}
        for key, value in self.user_input_event_map.items():
            if not callable(value[0]):
                break
            happened = False
            if len(value) == 1:
                happened = value[0]()
            else:
                for v in value[1:]:
                    happened = value[0](v)
                    if happened:
                        break
            events.update({key: happened})

        self._set_user_actions_map(events)

    def set_next_entity_id(self, id: int):
        self.__next_entity_id = id

    def set_next_scene(self, scene: str):
        self.scene_manager.next_scene = scene

    @property
    def scenes(self):
        """Return all scenes of world.

        Returns
        -------
        _type_
            list[str]: names of all scenes
        """
        return self.scene_manager.scenes

    @property
    def current_scene(self):
        """Return current scene of world.

        Returns
        -------
        _type_
            str: current scene name
        """
        return self.scene_manager.current_scene

    @property
    def next_scene(self):
        """Return next scene of world.

        Returns
        -------
        _type_
            str: next scene name
        """
        return self.scene_manager.next_scene

    @property
    def prev_scene(self):
        """Return previous scene of world.

        Returns
        -------
        _type_
            str: previous scene name
        """
        return self.scene_manager.prev_scene

    @property
    def current_systems(self):
        """Return systems of current scene of world.

        Returns
        -------
        _type_
            list["System"]: systems of current scene
        """
        current = self.current_scene
        if current is None:
            return []
        return self.scene_systems.get(current, [])

    @property
    def current_screens(self):
        """Return screens of current scene of world.

        Returns
        -------
        _type_
            list["Screen"]: screens of current scene
        """
        current = self.current_scene
        if current is None:
            return []
        return self.scene_screens.get(current, [])

    @property
    def current_events(self):
        """Return events of current scene of world.

        Returns
        -------
        _type_
            list["Event"]: events of current scene
        """
        current = self.current_scene
        if current is None:
            return []
        return self.scene_events.get(current, [])

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
        self.scene_manager.current_scene = scene

    @property
    def next_entity_id(self):
        return self.__next_entity_id
