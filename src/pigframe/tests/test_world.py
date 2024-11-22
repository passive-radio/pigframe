from pigframe.world import World, System, Screen
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Velocity:
    x: int
    y: int


class System1(System):
    def process(self):
        pass


class Screen1(Screen):
    def draw(self):
        pass


def test_systems():
    app = World()
    app.add_scenes(["scene1"])
    app.add_system(System1, 0)
    app.add_screen(Screen1, 0)
    app.current_scene = "scene1"

    app.process_systems()
    app.process_screens()
    assert True


def test_entity_id():
    world = World()
    ent1 = world.create_entity()
    ent2 = world.create_entity(3)
    assert ent1 == 0
    assert ent2 == 3


def test_component():
    world = World()
    ent1 = world.create_entity()
    world.add_component_to_entity(ent1, Position, x=10, y=20)
    world.add_component_to_entity(ent1, Velocity, x=1, y=2)
    assert world.get_entity_object(ent1)[Position] == Position(x=10, y=20)
    assert world.get_entity_object(ent1)[Velocity] == Velocity(x=1, y=2)
    assert world.component_exist(Position) is True
    assert world.component_exist(Velocity) is True
    assert world.has_component(ent1, Position) is True
    assert world.has_components(ent1, Position, Velocity) is True
    assert world.set_of_components_exist([Position, Velocity]) is True


if __name__ == "__main__":
    test_systems()
    test_entity_id()
    test_component()
