from pigframe.world import World
import pyxel

from system import *
from component import *
from screen import *
from event import *

class App(World):
    def __init__(self):
        super().__init__()
        self.init()
        
    def init(self):
        self.FPS = 60
        self.SCREEN_SIZE = (256, 256)
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], title="Control a ball", fps=self.FPS, quit_key=pyxel.KEY_NONE)
        pyxel.mouse(True)
        self.frame_count = 0
        
    def run(self):
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.process()
        self.frame_count += 1
        
    def draw(self):
        self.draw_screens()

def create_player_entity(app: App):
    ent = app.create_entity()
    app.add_component_to_entity(ent, Position(40, 40))
    app.add_component_to_entity(ent, Velocity(0, 0))
    app.add_component_to_entity(ent, Movable(0.3, 0))
    
if __name__ == "__main__":
    app = App()
    app.add_scenes(["launch", "game"])
    
    app.add_scene_system(System(app), "launch")
    
    app.add_scene_map("launch", "game", lambda: pyxel.btn(pyxel.KEY_SPACE))
    app.add_scene_map("game", "launch", lambda: pyxel.btn(pyxel.KEY_ESCAPE))
    
    app.add_scene_system(SysControlVelocity(app), "game")
    app.add_scene_system(SysBallMovement(app), "game")
    
    app.add_scene_events_map("game", "change_ball_color", lambda: pyxel.btnp(pyxel.KEY_C))
    
    app.add_scene_event(EvChangeBallColor(app, "change_ball_color"), "game")
    
    app.add_scene_screen(ScLaunch(app), "launch", 0)
    app.add_scene_screen(ScGame(app), "game", 0)
    
    create_player_entity(app)
    app.current_scene = "launch"
    app.run()