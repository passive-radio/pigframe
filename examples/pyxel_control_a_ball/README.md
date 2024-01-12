## control a ball [Pyxel version]

#### Files include:

- app.py: main file where a World's child class `App` is implemented and run.
- component.py: `Component` examples (Movable, Position, Velocity)
- entity.py: Player class with create method which create player entity and add components to world.
- event.py: `Event` examples (EvChangeBallColor)
- screen.py: `Screen` examples (ScLaunch, ScGame)
- system.py: `System` examples (SysBallMovement, SysControlVelocity)

#### User guide:

1. Download this code.
1. install module dependency
    ```bash
    pip install -U pyxel pigframe
    ```
1. Run app.py
    ```bash
    python app.py
    ```