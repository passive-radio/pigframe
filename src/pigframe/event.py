from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .system import System
    from .base_world import BaseWorld

class Event(metaclass=ABCMeta):
    """Event is a class which has a process method.
    The process method is executed when the event is trigered.
    """

    def __init__(self, world: "BaseWorld", priority: int = 0, **kwargs) -> None:
        """Event is a class which has a process method.
        The process method is executed when the event is trigered.

        Parameters
        ----------
        world : World
            World object
        event_name : str
            name of event
        priority : int, optional
            event with its lower priority than the others events is executed in advance., by default 0
        """
        self.world: "BaseWorld" = world
        self.priority = priority

    def process(self):
        current_scene = self.world.current_scene
        if current_scene is None:
            return
            
        if self.world.scene_manager.scenes_events[current_scene][type(self)]["run"] != 1:
            return

        self.__process()
        self.world.scene_manager.scenes_events[current_scene][type(self)]["run"] = 0

    @abstractmethod
    def __process(self):
        pass