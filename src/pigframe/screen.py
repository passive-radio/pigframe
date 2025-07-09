from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_world import BaseWorld

class Screen(metaclass=ABCMeta):
    """Screen is a class which has a draw method.
    The draw method is executed every frame.
    """

    def __init__(self, world: "BaseWorld", priority: int = 0, **kwargs) -> None:
        """Screen is a class which has a draw method. The draw method is executed every frame.

        Parameters
        ----------
        world : World
            World object
        priority : int, optional
            system with its lower priority than the other systems is executed in advance., by default 0
        """
        self.world: "BaseWorld" = world
        self.priority = priority

    @abstractmethod
    def draw(self):
        pass