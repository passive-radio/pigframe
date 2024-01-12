from pigframe.world import System
import pyxel
from component import *

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
            if pyxel.btn(pyxel.KEY_A):
                vel.dx -= 1 * mov.speed
            if pyxel.btn(pyxel.KEY_D):
                vel.dx += 1 * mov.speed
            if pyxel.btn(pyxel.KEY_W):
                vel.dy -= 1 * mov.speed
            if pyxel.btn(pyxel.KEY_S):
                vel.dy += 1 * mov.speed
            if not pyxel.btn(pyxel.KEY_A) and not pyxel.btn(pyxel.KEY_D):
                vel.dx = vel.dx * 0.8
            if not pyxel.btn(pyxel.KEY_W) and not pyxel.btn(pyxel.KEY_S):
                vel.dy = vel.dy * 0.8