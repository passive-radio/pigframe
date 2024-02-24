from dataclasses import dataclass
from pigframe.world import World, Component

@dataclass
class Position(Component):
    x: int
    y: int

@dataclass
class Velocity(Component):
    x: int
    y: int

def test():
    app = World()
    app.add_scenes(["scene1", "scene2", "scene3"])
    ent = app.create_entity()
    app.add_component_to_entity(ent, Position, x = 0, y = 0)
    print(app.get_entity_object(ent))
    app.remove_component_from_entity(ent, Position)
    print(app.get_entity_object(ent))
    
    app.add_component_to_entity(ent, Position, x = 0, y = 0)
    app.add_component_to_entity(ent, Velocity, x = 1, y = 1)
    print(app.get_entity_object(ent))
    app.remove_components_from_entity(ent, Position, Velocity)
    print(app.get_entity_object(ent))

test()