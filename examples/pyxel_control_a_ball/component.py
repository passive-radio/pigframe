from pigframe.world import Component

class Movable(Component):
    def __init__(self, speed: float = 0.3, body_color: int = 9):
        super().__init__()
        self.speed = speed
        if body_color < 0 or body_color > 15:
            raise ValueError("body_color must be between 0 and 15")
        self.body_color = body_color

class Position(Component):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y
        
class Velocity(Component):
    def __init__(self, dx=0, dy=0):
        super().__init__()
        self.dx = dx
        self.dy = dy