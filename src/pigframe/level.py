class LevelManager():
    def __init__(self) -> None:
        self.__scenes_events = {}
        self.__scenes_map = {}
        
    def add_scenes(self, scenes: list[str]) -> None:
        for scene in scenes:
            if self.__scenes_events.get(scene) is None:
                self.__scenes_events.update({scene: {}})
                self.__scenes_map.update({scene: {}})
            
    def add_scene(self, scene: str) -> None:
        if self.__scenes_events.get(scene) is None:
            self.__scenes_events.update({scene: {}})
            self.__scenes_map.update({scene: {}})
    
    def add_scene_events(self, scene: str, event: str, triger: callable) -> None:
        if self.__scenes_events.get(scene) is None:
            self.__scenes_events.update({scene: {}})
        
        self.__scenes_events[scene].update({event: {"triger": triger, "run": 0}})
        # self.scenes_events: dict[dict] = {"launch": {"launch": 0, "start-playing": 0},
        #     "choose-difficulty": {"choose-difficulty": 0, "start-playing": 0},
        #     "start-playing": {"start-timer": 0},
        #     "main": {"main": 0, "update-resources": 0, "cal-result": 0},
        #     "result": {"difficulty-up": 0},
        #     "update-resources": {"update-resources": 0}}
        
    def add_scene_map(self, scene: str, to: str, triger: callable) -> None:
        if self.__scenes_map.get(scene) is None:
            self.__scenes_map.update({scene: {}})
        
        self.__scenes_map[scene].update({to: triger})
        
    def update_scene_event(self, scene, event, run: int):
        self.__scenes_events[scene][event]["run"] = run

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
        