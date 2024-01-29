from pigframe.world import Event
from component import *

class EvChangeBallColor(Event):
    """Event to change ball color
    """
    
    def _Event__process(self):
        print("change ball color")
        for ent, (mov) in self.world.get_component(Movable):
            print(mov)
            mov.body_color += 1
            if mov.body_color > 15:
                mov.body_color = 0