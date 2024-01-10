from pigframe.world import Event
from component import *

class EvChangeBallColor(Event):
    """Event to change ball color
    """
    
    def process(self):
        if self.world.level_manager.scenes_events[self.world.current_scene][self.event_name]["run"] != 1:
            return
        
        print("process event!: ", self.event_name)
        self.__process()
        self.world.level_manager.scenes_events[self.world.current_scene][self.event_name]["run"] = 0
    
    def __process(self):
        print("change ball color")
        for ent, (mov) in self.world.get_component(Movable):
            print(mov)
            mov.body_color += 1
            if mov.body_color > 15:
                mov.body_color = 0