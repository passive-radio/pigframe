from .component import Component
from dataclasses import dataclass
from typing import Type

@dataclass
class WorldEntities:
    value: dict[int, dict[Type[Component], Component]]
    
@dataclass
class WorldComponents:
    value: dict[Type[Component], set[int]]
    