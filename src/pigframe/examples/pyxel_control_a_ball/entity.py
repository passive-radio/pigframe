from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from component import *
from pigframe.world import World

class Entity(metaclass=ABCMeta):
    
    def __init__(self, world: World) -> None:
        self.world = world
    
    @abstractmethod
    def create(self):
        pass

class Player(Entity):
    def __init__(self, world: World) -> None:
        super().__init__(world)
    
    def create(self):
        ent = self.world.create_entity()
        self.world.add_component_to_entity(ent, Position, x = 40, y = 40)
        self.world.add_component_to_entity(ent, Velocity, x = 0, y = 0)
        self.world.add_component_to_entity(ent, Movable, speed = 0.3, body_color = 9)
        return ent