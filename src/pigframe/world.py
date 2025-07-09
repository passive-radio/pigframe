"""
This module contains `World` class which is the core of the game, 
and `System`, `Screen`, `Event` classes which are the base systems 
in the context of ECS (Entity Component System).
"""

from typing import Type
from dataclasses import dataclass, asdict, field, make_dataclass
from .scene import SceneManager
from abc import ABCMeta, abstractmethod
from .action import ActionMap
from .base_world import BaseWorld
from .utils import save_game, load_game

class World(BaseWorld, metaclass=ABCMeta):
    """World is the core of the game.
    It contains all the entities and components.
    """
    
    def save_game(self, file_path: str):
        save_game(self.entities, file_path)
        
    def load_game(self, file_path: str):
        load_game(self, file_path)
        