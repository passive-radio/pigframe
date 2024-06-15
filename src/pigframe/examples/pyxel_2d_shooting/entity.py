from pigframe import World
from component import Position, Velocity, Movable, Playable, CpEnemy, Bullet

class Player:
    def __init__(self, world: World, x, y):
        self.world = world
        self.x = x
        self.y = y

    def create(self):
        entity = self.world.create_entity()
        self.world.add_component_to_entity(entity, Position, x = self.x, y = self.y)
        self.world.add_component_to_entity(entity, Velocity, x = 0, y = 0)
        self.world.add_component_to_entity(entity, Movable, speed = 2)
        self.world.add_component_to_entity(entity, Playable, hp = 10)

class Enemy:
    def __init__(self, world: World, x, y):
        self.world = world
        self.x = x
        self.y = y

    def create(self):
        entity = self.world.create_entity()
        self.world.add_component_to_entity(entity, Position, x = self.x, y = self.y)
        self.world.add_component_to_entity(entity, Velocity, x = 0, y = 0)
        self.world.add_component_to_entity(entity, Movable, speed = 1)
        self.world.add_component_to_entity(entity, CpEnemy, hp = 3)
