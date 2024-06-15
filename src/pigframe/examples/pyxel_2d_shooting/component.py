from dataclasses import dataclass
from pigframe.world import Component

@dataclass
class Position(Component):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y

@dataclass
class Velocity(Component):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y

@dataclass
class Movable(Component):
    def __init__(self, speed: float = 1.0):
        super().__init__()
        self.speed = speed

@dataclass
class Character(Component):
    def __init__(self, hp: int = 10):
        super().__init__()
        self.hp = hp

@dataclass
class Playable(Character):
    def __init__(self, hp: int = 10, init_score: int = 0):
        super().__init__(hp=hp)
        self.score = init_score
        # Add any additional player-specific attributes if needed

@dataclass
class CpEnemy(Character):
    def __init__(self, hp: int = 10):
        super().__init__(hp=hp)
        # Add any additional enemy-specific attributes if needed

@dataclass
class Bullet(Component):
    def __init__(self):
        super().__init__()
        # Add any additional bullet-specific attributes if needed
