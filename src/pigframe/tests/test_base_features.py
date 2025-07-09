import pytest
from dataclasses import dataclass
from pigframe.world import World
from pigframe.system import System
from pigframe.event import Event
from pigframe.screen import Screen
from pigframe.component import Component


@dataclass
class Position(Component):
    x: int
    y: int


@dataclass
class Velocity(Component):
    x: int
    y: int


# 実際のWorldクラスを継承した具体クラス
class TestableWorld(World):
    def __init__(self):
        super().__init__()


class TestSystem(System):
    def __init__(self, world, priority=0, **kwargs):
        super().__init__(world, priority, **kwargs)
        self.processed = False
    
    def process(self):
        self.processed = True


class TestScreen(Screen):
    def __init__(self, world, priority=0, **kwargs):
        super().__init__(world, priority, **kwargs)
        self.drawn = False
    
    def draw(self):
        self.drawn = True


class TestEvent(Event):
    def __init__(self, world, priority=0, **kwargs):
        super().__init__(world, priority, **kwargs)
        self.triggered = False
    
    def __process(self):
        self.triggered = True


# World initialization test
def test_world_initialization():
    """Test that World class can be initialized properly"""
    world = TestableWorld()
    assert world is not None
    assert hasattr(world, "components")
    assert hasattr(world, "entities")
    assert hasattr(world, "scene_manager")
    assert world.next_entity_id == 0


# System creation and execution tests
def test_system_creation_and_execution():
    """Test that systems can be created and executed"""
    world = TestableWorld()
    world.add_scenes(["test_scene"])
    world.current_scene = "test_scene"
    
    system = TestSystem(world)
    world.add_system_to_scenes(TestSystem, "test_scene")
    assert not system.processed
    
    # Get system from the world
    world_system = world.current_systems[0]
    assert isinstance(world_system, TestSystem)
    
    # Process systems
    world.process_systems()
    assert world_system.processed


# Entity and component management tests
def test_entity_and_component_management():
    """Test entity creation and component management"""
    world = TestableWorld()
    
    # Test entity creation
    entity1 = world.create_entity()
    entity2 = world.create_entity()
    assert entity1 == 0
    assert entity2 == 1
    
    # Test component addition
    world.add_component_to_entity(entity1, Position, x=10, y=20)
    world.add_component_to_entity(entity2, Position, x=30, y=40)
    world.add_component_to_entity(entity1, Velocity, x=1, y=2)
    
    # Test component retrieval
    entity1_obj = world.get_entity_object(entity1)
    entity2_obj = world.get_entity_object(entity2)
    
    assert entity1_obj is not None
    assert entity2_obj is not None
    assert Position in entity1_obj
    assert Position in entity2_obj
    assert Velocity in entity1_obj
    
    assert entity1_obj[Position].x == 10
    assert entity1_obj[Position].y == 20
    assert entity2_obj[Position].x == 30
    assert entity2_obj[Position].y == 40
    assert entity1_obj[Velocity].x == 1
    assert entity1_obj[Velocity].y == 2
    
    # Test component existence checks
    assert world.component_exist(Position)
    assert world.component_exist(Velocity)
    assert world.has_component(entity1, Position)
    assert world.has_component(entity1, Velocity)
    assert world.has_component(entity2, Position)
    assert not world.has_component(entity2, Velocity)
    
    # Test component queries
    position_components = world.get_component(Position)
    assert len(position_components) == 2
    assert position_components[0][0] == entity1 or position_components[1][0] == entity1
    
    velocity_components = world.get_component(Velocity)
    assert len(velocity_components) == 1
    assert velocity_components[0][0] == entity1
    
    # Test multi-component queries
    position_velocity_components = world.get_components(Position, Velocity)
    assert len(position_velocity_components) == 1
    assert position_velocity_components[0][0] == entity1
    
    # Test component removal
    world.remove_component_from_entity(entity1, Position)
    assert not world.has_component(entity1, Position)
    assert world.has_component(entity1, Velocity)
    
    # Test entity removal
    world.remove_entity(entity2)
    assert world.get_entity_object(entity2) is None


# Scene management tests
def test_scene_management():
    """Test scene management functionality"""
    world = TestableWorld()
    
    # Test scene addition
    world.add_scenes(["scene1", "scene2"])
    assert "scene1" in world.scenes
    assert "scene2" in world.scenes
    
    # Test scene transitions
    world.current_scene = "scene1"
    assert world.current_scene == "scene1"
    
    world.set_next_scene("scene2")
    world.scene_manager.process()  # This should trigger the scene change
    world.scene_manager.update_scene()  # Update scene
    assert world.current_scene == "scene2"
    assert world.prev_scene == "scene1"


# Screen tests
def test_screen_functionality():
    """Test screen functionality"""
    world = TestableWorld()
    world.add_scenes(["test_scene"])
    world.current_scene = "test_scene"
    
    world.add_screen_to_scenes(TestScreen, "test_scene")
    assert len(world.current_screens) == 1
    
    screen = world.current_screens[0]
    assert isinstance(screen, TestScreen)
    assert not screen.drawn
    
    world.process_screens()
    assert screen.drawn


# Test with multiple systems with different priorities
def test_system_priorities():
    """Test systems with different priorities are executed in the correct order"""
    world = TestableWorld()
    world.add_scenes(["test_scene"])
    world.current_scene = "test_scene"
    
    execution_order = []
    
    class PrioritySystem(System):
        def __init__(self, world, priority=0, **kwargs):
            super().__init__(world, priority, **kwargs)
            self.name = kwargs.get("name", "unnamed")
        
        def process(self):
            execution_order.append(self.name)
    
    world.add_system_to_scenes(PrioritySystem, "test_scene", 2, name="high_priority")
    world.add_system_to_scenes(PrioritySystem, "test_scene", 1, name="medium_priority")
    world.add_system_to_scenes(PrioritySystem, "test_scene", 0, name="low_priority")
    
    world.process_systems()
    
    # Lower priority values should be executed first
    assert execution_order == ["low_priority", "medium_priority", "high_priority"]


# Test saving and loading game state
def test_save_load_game():
    """Test saving and loading game state"""
    import tempfile
    import os
    from pigframe.utils import register_component
    
    # コンポーネントクラスを登録
    register_component(Position)
    register_component(Velocity)
    
    world = TestableWorld()
    
    # Create entities with components
    entity1 = world.create_entity()
    entity2 = world.create_entity()
    world.add_component_to_entity(entity1, Position, x=10, y=20)
    world.add_component_to_entity(entity2, Position, x=30, y=40)
    world.add_component_to_entity(entity1, Velocity, x=1, y=2)
    
    # Save the game state
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        save_file = temp.name
    
    world.save_game(save_file)
    
    # Create a new world and load the saved state
    new_world = TestableWorld()
    new_world.load_game(save_file)
    
    # Verify the loaded state
    entity1_obj = new_world.get_entity_object(entity1)
    entity2_obj = new_world.get_entity_object(entity2)
    
    assert entity1_obj is not None
    assert entity2_obj is not None
    assert Position in entity1_obj
    assert Position in entity2_obj
    assert Velocity in entity1_obj
    
    assert entity1_obj[Position].x == 10
    assert entity1_obj[Position].y == 20
    assert entity2_obj[Position].x == 30
    assert entity2_obj[Position].y == 40
    assert entity1_obj[Velocity].x == 1
    assert entity1_obj[Velocity].y == 2
    
    # Clean up
    os.unlink(save_file) 