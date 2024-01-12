from pigframe.world import System
import pygame
from component import *

class SysEventListner(System):
    def __init__(self, world, priority: int = 0, *args) -> None:
        super().__init__(world, priority, *args)
        self.world.keys_down = {}
        self.world.keys_pressed = {}
    
    def process(self):
        self.world.keys_pressed.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.world.set_running(False)
            if event.type == pygame.KEYDOWN:
                self.world.keys_down.update({event.key: True})
                if event.key == pygame.K_ESCAPE:
                    self.world.set_running(False)
            if event.type == pygame.KEYUP:
                if self.world.keys_down.get(event.key) is not None and self.world.keys_down.get(event.key) == True:
                    self.world.keys_down.update({event.key: False})
                    self.world.keys_pressed.update({event.key: True})
                    

class SysBallMovement(System):
        
    def process(self):
        print("ball movement")
        for ent, (pos, vel) in self.world.get_components(Position, Velocity):
            pos.x += vel.dx
            pos.y += vel.dy
            if pos.x < 16:
                pos.x = 16
                vel.dx = 0
                # vel.x = -vel.x
            if pos.x > 240:
                pos.x = 240
                vel.dx = 0
                # vel.x = -vel.x
            if pos.y < 16:
                pos.y = 16
                vel.dy = 0
                # vel.y = -vel.y
            if pos.y > 240:
                pos.y = 240
                vel.dy = 0
                # vel.y = -vel.y
                
class SysControlVelocity(System):
        
    def process(self):
        for ent, (pos, vel, mov) in self.world.get_components(Position, Velocity, Movable):
            if pygame.key.get_pressed()[pygame.K_a]:
                vel.dx -= 1 * mov.speed
            if pygame.key.get_pressed()[pygame.K_d]:
                vel.dx += 1 * mov.speed
            if pygame.key.get_pressed()[pygame.K_w]:
                vel.dy -= 1 * mov.speed
            if pygame.key.get_pressed()[pygame.K_s]:
                vel.dy += 1 * mov.speed
            if not pygame.key.get_pressed()[pygame.K_a] and not pygame.key.get_pressed()[pygame.K_d]:
                vel.dx = vel.dx * 0.8
            if not pygame.key.get_pressed()[pygame.K_w] and not pygame.key.get_pressed()[pygame.K_s]:
                vel.dy = vel.dy * 0.8
                