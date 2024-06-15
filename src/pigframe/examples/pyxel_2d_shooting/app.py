from pigframe import World
import pyxel

from system import *
from screen import *
from event import *
from entity import Player, Enemy
from actions import Actions

class App(World):
    def __init__(self):
        super().__init__()
        self.init()
        
    def init(self):
        self.FPS = 60
        self.SCREEN_SIZE = (256, 256)
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1], title="Top-Down Shooter", fps=self.FPS, quit_key=pyxel.KEY_ESCAPE)
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
    app.add_scenes(["launch", "game", "game_over", "victory"])
    app.set_user_actions_map(Actions())
    
    app.add_scene_transition("launch", "game", lambda: app.actions.space_p)
    app.add_scene_transition("game_over", "game", lambda: app.actions.space_p)
    app.add_scene_transition("victory", "game", lambda: app.actions.space_p)
    
    app.add_system_to_scenes(SysPlayerMovement, "game", 0)
    app.add_system_to_scenes(SysEnemyMovement, "game", 1)
    app.add_system_to_scenes(SysShooting, "game", 2)
    app.add_system_to_scenes(SysBulletHitEnemy, "game", 3)
    app.add_system_to_scenes(SysPlayerHitEnemy, "game", 4)
    app.add_system_to_scenes(SysKillEnemy, "game", -1)
    app.add_system_to_scenes(SysGameOver, "game", -2)
    
    app.add_event_to_scene(EvRestart, "game_over", lambda: app.actions.space_p, 0)
    
    app.add_screen(ScBG, 0)
    app.add_screen_to_scenes(ScLaunch, "launch", 0)
    app.add_screen_to_scenes(ScPlayable, "game", 0)
    app.add_screen_to_scenes(ScEnemy, "game", 1)
    app.add_screen_to_scenes(ScDrawBullet, "game", 2)
    app.add_screen_to_scenes(ScStatus, "game", 3)
    app.add_screen_to_scenes(ScGameOver, "game_over", 0)
    
    Player(app, 200, 200).create()
    Enemy(app, 100, 100).create()
    app.current_scene = "launch"
    app.run()
