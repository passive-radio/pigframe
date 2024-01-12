from pigframe.world import Screen
from component import *
import pygame

class BaseScreen(Screen):
    def __init__(self, world, priority: int = 0, *args) -> None:
        super().__init__(world, priority, *args)
        self.font = pygame.font.Font(None, 12)
        self.COLORS = [(0, 0, 0), (43, 51, 95), (126, 32, 114), (25, 149, 156), (139, 72, 82), (57, 92, 152),
                    (169, 193, 255), (238, 238, 238), (212, 24, 108), (211, 132, 65), (233, 195, 91), (112, 198, 169), 
                    (118, 150, 222), (163, 163, 163), (255, 151, 152), (237, 199, 176)
                    ]
        
    def draw(self):
        pass

class ScLaunch(BaseScreen):
        
    def draw(self):
        self.world.screen.fill(self.COLORS[15])
        text1 = self.font.render("Hello World!", True, self.COLORS[self.world.frame_count // (self.world.FPS // 2) % 16])
        self.world.screen.blit(text1, (100, 100))
        text2 = self.font.render("Press SPACE to start", True, self.COLORS[7])
        self.world.screen.blit(text2, (85, 120))
        text3 = self.font.render("Press ESC to quit", True, self.COLORS[7])
        self.world.screen.blit(text3, (91, 132))
    
class ScGame(BaseScreen):
    
    def draw(self):
        self.world.screen.fill(self.COLORS[15])
        text1 = self.font.render("Game Screen", True, self.COLORS[7])
        self.world.screen.blit(text1, (100, 100))
        
        for ent, (pos, vel, mov) in self.world.get_components(Position, Velocity, Movable):
            print(mov.body_color)
            pygame.draw.circle(self.world.screen, self.COLORS[mov.body_color], (pos.x, pos.y), 8)
            pygame.draw.line(self.world.screen, self.COLORS[7], (pos.x, pos.y), (pos.x + vel.dx * 10, pos.y + vel.dy * 10), 2)