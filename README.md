## Pigframe
![Pigframe](docs/images/pigframe-logo-rectangle-200x99.jpg)

[![Downloads](https://static.pepy.tech/badge/pigframe)](https://pepy.tech/project/pigframe)

<b>[日本語版 README](docs/README-ja.md)</b>

<b>Pigframe</b> is a minimum ECS (Entity Component System) library for any Python-based game dev project. While I think it's quite rare to want to adopt ECS for game development in Python, I created this library because there wasn't an open-source library (at the time I started development) that provided both ECS and state management as a single package.

### Key Features:
- <b>Component-Based Architecture</b>: Pigframe adopts a component-based approach, allowing for modular and scalable game development. This architecture facilitates easy addition, modification, and management of game elements.

- <b>Intuitive Scene Management</b>: Manage game scenes seamlessly with Pigframe's intuitive scene transition and control system. This feature allows for smooth transitions and efficient scene organization.

- <b>Efficient Entity-Component System</b>: At the heart of Pigframe is an efficient entity-component system (ECS), which promotes a clean separation of concerns and enhances performance.

- <b>Pythonic Simplicity</b>: Designed with Python's philosophy of simplicity and readability, Pigframe is ideal for those learning game development or individual developers seeking an accessible yet powerful tool.

- <b>Versatile Integration</b>: Pigframe is optimized to work seamlessly with popular Python game libraries like Pyxel and Pygame, making it a perfect choice for diverse and creative game development projects.

### Getting Started:
To get started with Pigframe, simply install the `pigframe` from PyPI.
Pigframe has no dependencies.

```bash
pip install pigframe # pigframe has no dependencies.
```

### How to use:

- import module
    ```python
    from pigframe import World, System, Event, Screen, Component
    ```

- create your own world class which manage entities, components, systems, events and screens. It is the start of your game scripts.
    ```python
    # Implement World class for your own project.
    # Example 
    class App(World):
        def __init__(self):
            super().__init__()
            self.init() # write initial process which is unique to the game engine and the game you develop.
        
        ... # other game engine unique methods.
    
    app = App()
    ```

- create and remove entity
    ```python
    # Create entity to world.
    entity = app.create_entity() # -> int: entity ID
    # Remove entity from world.
    app.remove_entity(entity) # deletes from entites list
    ```

- add/remove components to entity
    - add components to entity
        ```python
        # Add component to entity ID.
        # Components are recorded as values where entity ID is the key inside dict.
        # Component instance are created automatically.
        app.add_component_to_entity(entity, ComponentA, **component_args) # ComponentA is not an instance of Component but type.
        app.add_component_to_entity(entity, ComponentB(**component_args)) # This is wrong way of use.
        # getter
        app.get_component(ComponentA) # Returns the list of tuple: entity id which has ComponentA, component object. -> list((int, ComponentA object))
        app.get_components(ComponentA, ComponentB) # Returns the list of tuple: entity id which has ComponentA and ComponentB, component objects.  -> list((int, (ComponentA object, ComponentB object)))
        ```

    - remove components from entity
        ```python
        app.add_component_to_entity(ent, ComponentA, **component_argsA)
        app.add_component_to_entity(ent, ComponentB, **component_argsB)
        app.remove_component_from_entity(ent, ComponentA) # remove single component instance from entity

        app.add_component_to_entity(ent, ComponentC, **component_argsC)
        app.remove_components_from_entity(ent, ComponentB, ComponentC) # remove components instances from entity
        ```

- use component values inside system, event and screen
    ```python
    # Example of using get_components() method.
    class SystemA(System):
        def process(self):
            for ent, (pos, vel) in self.world.get_components(Position, Velocity):
                """
                Update positions by velocity
                """
                pos.x += vel.x
                pos.y += vel.x
    ```

- use entity
    ```python
    # Example of using entity object
    class EventA(Event):
        def __process(self):
            player = self.world.get_entity_object(0) # 0 is the entity ID
            """
            This method returns a dict
            -----------
            dict: entity object
                key: component type
                value: component
            """
    ```

- add scenes to world
    ```python
    # Add scenes to world.
    app.add_scenes(["launch", "game", "result", "settings"])
    add.add_scene("game_over")
    # scenes getter
    app.sceneces # -> [["launch", "game", "result", "settings", "game_over"]
    ```

- add/remove system to/from world
    ```python
    # Add screen to a scene of world. Be sure you have added scenes before adding systems.
    # System instance are created automatically.
    app.add_system_to_scenes(SystemA, "launch", priority = 0, **system_args)
    # system with its lower priority than the other systems is executed in advance., by default 0.
    # World calls System A then System B.
    app.add_system_to_scenes(SystemA, "game", priority = 0, **system_args)
    app.add_system_to_scenes(SystemB, "launch", priority = 1)
    # Remove system from scene.
    app.remove_system_from_scene(SystemA, ["launch", "game"])
    ```

- add/remove screens to/from world
    ```python
    # Add screen to a scene of world. Be sure you have added scenes before adding screens.
    # Screen instance are created automatically.
    app.add_screen_to_scenes(ScreenA, "launch", priority = 0)
    app.add_screen_to_scenes(ScreenB, "launch", priority = 0)
    app.add_screen_to_scenes(ScreenC, "game", priority = 0, screen_args)
    # Remove screen from scene.
    app.remove_screen_from_scene(ScreenB, "launch")
    ```

- add/remove event to/from world
    ```python
    # Add an event, event triger to a scene of world. Be sure you have added scenes before adding events.
    # Event instance are created automatically.
    app.add_event_to_scene(EventA, "game", callable_triger, priority = 0)
    # Remove event from scene.
    app.remove_event_from_scene(EventA, "game")
    ```

- add scene transitions settings
    ```python
    app.add_scene_transition(scene_from = "launch", scene_to = "game", triger = callable_triger)
    # triger has to be callable.
    ```

- execute systems, events and draw screens
    ```python
    # Example with Pyxel (Python retro game engine)
    class App(World):
        ...

        def run(self):
            pyxel.run(self.update, self.draw)

        def update(self):
            self.process() # World class has process method.
            # process method calls these internal methods below.
            # 1. process_systems()
            # 1. process_events()
            # 1. scene_manager.process()

        def draw(self):
            self.process_screens()
    ```

    In `update()` method, of course, you can customize execution order as well.
    ```python
    def update(self):
      self.process_user_actions()
      self.process_systems()
      self.proces_events()
      self.scene_manager.process() # Pigframe implements scene listener and World class use this class to manage scenes.
    ```

    ```python
    # Pygame Example
    class App(World):
        ...
        
        def run(self):
            while self.running:
                self.update()
                self.draw()
                
        def update(self):
            self.process()
        
        def draw(self):
            self.process_screens()
    ```

    If you'd like to know further information, please check example mini projects listed below.

### Examples
| game engine | example | contents |
| ---- | ----| ---- |
| Pygame | [Demo of player's controlling a ball](https://github.com/passive-radio/pigframe/tree/main/src/pigframe/examples/pygame_control_a_ball) | examples of system, event, component and world implementations. |
| Pyxel | [Demo of player's controlling a ball](https://github.com/passive-radio/pigframe/tree/main/src/pigframe/examples/pyxel_control_a_ball) | examples of system, event, component and world implementations. |
| Pyxel | [Super simple 2D shooting](https://github.com/passive-radio/pigframe/tree/main/src/pigframe/examples/pyxel_2d_shooting) | examples of system, event, component, actions and world implementations. |

### Contributing:
Contributions to Pigframe are welcome! Whether it's bug reports, feature requests or code contributions, any inputs are valuable in making Pigframe better for everyone.
