from pigframe.world import System
from component import *

class SysBallMovement(System):
        
    def process(self):
        print("ball movement")
        for ent, (pos, vel) in self.world.get_components(Position, Velocity):
            pos.x += vel.x
            pos.y += vel.y
            if pos.x < 16:
                pos.x = 16
                vel.x = 0
                # vel.x = -vel.x
            if pos.x > 240:
                pos.x = 240
                vel.x = 0
                # vel.x = -vel.x
            if pos.y < 16:
                pos.y = 16
                vel.y = 0
                # vel.y = -vel.y
            if pos.y > 240:
                pos.y = 240
                vel.y = 0
                # vel.y = -vel.y
                
class SysControlVelocity(System):
        
    def process(self):
        for ent, (pos, vel, mov) in self.world.get_components(Position, Velocity, Movable):
            actions = self.world.actions
            if actions.left:
                vel.x -= 1 * mov.speed
            if actions.right:
                vel.x += 1 * mov.speed
            if actions.up:
                vel.y -= 1 * mov.speed
            if actions.down:
                vel.y += 1 * mov.speed
            if not actions.left and not actions.right:
                vel.x = vel.x * 0.8
            if not actions.up and not actions.down:
                vel.y = vel.y * 0.8