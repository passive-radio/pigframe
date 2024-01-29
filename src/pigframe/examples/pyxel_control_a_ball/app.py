from pigframe.world import World
import pyxel

from system import *
from component import *
from screen import *
from event import *
from entity import Player

class App(World):
    def __init__(self):
        super().__init__()
        self.init()
        
    def init(self):
        self.FPS = 60
        self.SCREEN_SIZE = (256, 256)
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], title="Control a ball", fps=self.FPS, quit_key=pyxel.KEY_ESCAPE)
        pyxel.mouse(True)
        self.frame_count = 0
        
    def run(self):
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.process()
        self.frame_count += 1
        
    def draw(self):
        self.process_screens()
    
if __name__ == "__main__":
    app = App()
    app.add_scenes(["launch", "game"])
    
    app.add_scene_transition("launch", "game", lambda: pyxel.btn(pyxel.KEY_SPACE))
    app.add_scene_transition("game", "launch", lambda: pyxel.btn(pyxel.KEY_Q))
    
    app.add_system_to_scenes(SysControlVelocity, "game", 0)
    app.add_system_to_scenes(SysBallMovement, "game", 1)
    
    app.add_event_to_scene(EvChangeBallColor, "game", lambda: pyxel.btnp(pyxel.KEY_C), 0)
    
    app.add_screen_to_scenes(ScLaunch, "launch", 0)
    app.add_screen_to_scenes(ScGame, "game", 0)
    
    Player(app).create()
    app.current_scene = "launch"
    app.run()