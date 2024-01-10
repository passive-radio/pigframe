version = '0.0.1'

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
    
    def add_scene_events(self, scene: str, event_name: str, triger: callable) -> None:
        if self.__scenes_events.get(scene) is None:
            self.__scenes_events.update({scene: {}})
        
        self.__scenes_events[scene].update({event_name: {"triger": triger, "run": 0}})
        
    def add_scene_map(self, scene: str, to: str, triger: callable) -> None:
        if self.__scenes_map.get(scene) is None:
            self.__scenes_map.update({scene: {}})
        
        self.__scenes_map[scene].update({to: triger})
        
    def update_scene_event(self, scene, event, run: int):
        self.__scenes_events[scene][event]["run"] = run
        
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
    def to(self):
        return self.__scenes_map.values()
    
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
        