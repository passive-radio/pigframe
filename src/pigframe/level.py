"""
This module contains the level manager class.
"""

from typing import TypeVar

_T_event = TypeVar('_T_event')

class LevelManager():
    """Level manager class.
    """
    def __init__(self) -> None:
        self.__scenes_events: dict[dict] = {}
        self.__scenes_map: dict[dict] = {}
        self.current_scene = None
        self.next_scene = None
        self.prev_scene = None
        
    def add_scenes(self, scenes: list[str]) -> None:
        """Add scenes to the level manager.

        Parameters
        ----------
        scenes : list[str]
            List of scenes to add.
        """
        for scene in scenes:
            if self.__scenes_events.get(scene) is None:
                self.__scenes_events.update({scene: {}})
                self.__scenes_map.update({scene: {}})
            
    def add_scene(self, scene: str) -> None:
        """Add scene to the level manager.

        Parameters
        ----------
        scene : str
            Scene to add.
        """
        if self.__scenes_events.get(scene) is None:
            self.__scenes_events.update({scene: {}})
            self.__scenes_map.update({scene: {}})
    
    def add_scene_event(self, scene: str, event_type: _T_event, triger: callable) -> None:
        """Add event to the scene.

        Parameters
        ----------
        scene : str
            Scene to add event.
        event_type : _T_event
            Event type.
        triger : callable
            Event triger.
        """
        if self.__scenes_events.get(scene) is None:
            self.__scenes_events.update({scene: {}})
        
        self.__scenes_events[scene].update({event_type: {"triger": triger, "run": 0}})
        
    def add_scene_transition(self, scene_from: str, scene_to: str, triger: callable) -> None:
        """Add transition between scenes.

        Parameters
        ----------
        scene_from : str
            scene from
        scene_to : str
            scene to
        triger : callable
            transition triger
        """
        if self.__scenes_map.get(scene_from) is None:
            self.__scenes_map.update({scene_from: {}})
        
        self.__scenes_map[scene_from].update({scene_to: triger})
        
    def update_scene_event(self, scene: str, event_type: _T_event, run: int):
        """Update event run.

        Parameters
        ----------
        scene : str
            scene where event is located
        event_type : _T_event
            event type
        run : int
            whether the event should be run
        """
        self.__scenes_events[scene][event_type]["run"] = run
        
    def process(self):
        """Process events and transitions. Update current scene.
        """
        self.__process_events()
        self.__process_transitions()
        self.update_scene()
        
    def __process_events(self):
        """Process events.
        """
        if self.__scenes_events.get(self.current_scene) is None:
            return
        for event, event_data in self.__scenes_events[self.current_scene].items():
            if event_data["triger"]():
                self.update_scene_event(self.current_scene, event, 1)
    
    def __process_transitions(self):
        """Process transitions.
        """
        if self.__scenes_map.get(self.current_scene) is None:
            return
        for scene, triger in self.__scenes_map[self.current_scene].items():
            if triger():
                self.next_scene = scene
                return
    
    def update_scene(self):
        """Update current scene.
        """
        self.prev_scene = self.current_scene
        if self.next_scene is not None:
            self.current_scene = self.next_scene

    @property
    def transitions(self):
        """Return transitions.

        Returns
        -------
        dict
            transitions
        """
        return self.__scenes_map.items()
    
    @property
    def scenes(self):
        """Return scenes.

        Returns
        -------
        dict_keys
            scenes
        """
        return self.__scenes_map.keys()
    
    @property
    def scenes_events(self):
        """Return scenes events.
        
        Returns
        -------
        dict
            scenes events
        """
        return self.__scenes_events
    
    @property
    def scenes_map(self):
        """Return scenes map.
        
        Returns
        -------
        dict
            scenes map
        """
        return self.__scenes_map

    def get_scene_events(self, scene: str):
        """Return scene events.

        Parameters
        ----------
        scene : str
            scene

        Returns
        -------
        dict
            scene events
        """
        return self.__scenes_events.get(scene)
    
    def get_scene_transitions(self, scene: str):
        """Return scene transitions.

        Parameters
        ----------
        scene : str
            scene

        Returns
        -------
        dict
            scene transitions
        """
        return self.__scenes_map.get(scene)
        