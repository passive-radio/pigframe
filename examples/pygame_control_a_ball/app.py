from pigframe.world import World
import pygame
import sys

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
        pygame.init()
        pygame.mouse.set_visible(True)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Control a ball")
        self.frame_count = 0
        self.clock = pygame.time.Clock()
        
    def run(self):
        while self.__running:
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
            print(self.current_scene)
        pygame.quit()
        sys.exit()
    
    def update(self):
        self.process()
        self.frame_count += 1
        
    def draw(self):
        self.process_screens()
        pygame.display.update()
    
    def set_running(self, running: bool):
        self.__running = running
        
    @property
    def running(self):
        return self.__running
    
    def was_pressed(self, key):
        return self.keys_pressed.get(key) is not None and self.keys_pressed.get(key) == True
    
if __name__ == "__main__":
    app = App()
    app.add_scenes(["launch", "game"])
    
    app.add_scene_transition("launch", "game", lambda: pygame.key.get_pressed()[pygame.K_SPACE])
    app.add_scene_transition("game", "launch", lambda: pygame.key.get_pressed()[pygame.K_q])
    
    app.add_system_to_scenes(SysControlVelocity, "game", 1)
    app.add_system_to_scenes(SysBallMovement, "game", 2)
    app.add_system_to_scenes(SysEventListner, ["launch", "game"], 0)
    
    app.add_event_to_scene(EvChangeBallColor, "game", lambda: app.was_pressed(pygame.K_c), 0)
    
    app.add_screen_to_scenes(ScLaunch, "launch", 0)
    app.add_screen_to_scenes(ScGame, "game", 0)
    
    Player(app).create()
    app.set_running(True)
    app.current_scene = "launch"
    app.run()