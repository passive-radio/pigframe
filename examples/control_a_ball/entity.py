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
        self.world.add_component_to_entity(ent, Position, 40, 40)
        self.world.add_component_to_entity(ent, Velocity, 0, 0)
        self.world.add_component_to_entity(ent, Movable, True)
        return ent