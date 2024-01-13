from typing import TypeVar

_T_event = TypeVar('_T_event')

class LevelManager():
    def __init__(self) -> None:
        self.__scenes_events: dict[dict] = {}
        self.__scenes_map: dict[dict] = {}
        self.current_scene = None
        self.next_scene = None
        self.prev_scene = None
        
    def add_scenes(self, scenes: list[str]) -> None:
        for scene in scenes:
            if self.__scenes_events.get(scene) is None:
                self.__scenes_events.update({scene: {}})
                self.__scenes_map.update({scene: {}})
            
    def add_scene(self, scene: str) -> None:
        if self.__scenes_events.get(scene) is None:
            self.__scenes_events.update({scene: {}})
            self.__scenes_map.update({scene: {}})
    
    def add_scene_event(self, scene: str, event_type: _T_event, triger: callable) -> None:
        if self.__scenes_events.get(scene) is None:
            self.__scenes_events.update({scene: {}})
        
        self.__scenes_events[scene].update({event_type: {"triger": triger, "run": 0}})
        
    def add_scene_transition(self, scene_from: str, scene_to: str, triger: callable) -> None:
        if self.__scenes_map.get(scene_from) is None:
            self.__scenes_map.update({scene_from: {}})
        
        self.__scenes_map[scene_from].update({scene_to: triger})
        
    def update_scene_event(self, scene: str, event_type: _T_event, run: int):
        self.__scenes_events[scene][event_type]["run"] = run
        
    def process(self):
        self.__process_events()
        self.__process_transitions()
        self.update_scene()
        
    def __process_events(self):
        for event, event_data in self.__scenes_events[self.current_scene].items():
            if event_data["triger"]():
                self.update_scene_event(self.current_scene, event, 1)
    
    def __process_transitions(self):
         for scene, triger in self.__scenes_map[self.current_scene].items():
            if triger():
                self.next_scene = scene
                return
    
    def update_scene(self):
        self.prev_scene = self.current_scene
        if self.next_scene is not None:
            self.current_scene = self.next_scene

    @property
    def transitions(self):
        return self.__scenes_map.items()
    
    @property
    def scenes(self):
        return self.__scenes_map.keys()
    
    @property
    def scenes_events(self):
        return self.__scenes_events
    
    @property
    def scenes_map(self):
        return self.__scenes_map

    def get_scene_events(self, scene: str):
        return self.__scenes_events.get(scene)
    
    def get_scene_transitions(self, scene: str):
        return self.__scenes_map.get(scene)
        