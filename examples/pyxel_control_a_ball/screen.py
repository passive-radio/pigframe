from pigframe.world import Screen
from component import *
import pyxel

class ScLaunch(Screen):
        
    def draw(self):
        pyxel.cls(15)
        pyxel.text(100, 100, "Hello World!", self.world.frame_count // (self.world.FPS // 2) % 16)
        pyxel.text(85, 120, "Press SPACE to start", 7)
        pyxel.text(91, 132, "Press ESC to quit", 7)
    
class ScGame(Screen):
    
    def draw(self):
        pyxel.cls(15)
        pyxel.text(100, 100, "Game Screen", 7)
        for ent, (pos, vel, mov) in self.world.get_components(Position, Velocity, Movable):
            print(mov.body_color)
            pyxel.circ(pos.x, pos.y, 8, mov.body_color)
            pyxel.line(pos.x, pos.y, pos.x + vel.dx * 10, pos.y + vel.dy * 10, 7)