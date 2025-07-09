"""Component is a class which is a base class for all components.

"""

from dataclasses import dataclass
from abc import ABCMeta


@dataclass
class Component(metaclass=ABCMeta):
    """Base class for components."""
