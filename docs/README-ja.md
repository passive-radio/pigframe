## Pigframe
![Pigframe](https://github.com/passive-radio/pigframe/blob/main/docs//images/pigframe-logo-rectangle-200x99.jpg)

<b>[README(en)](../README.md)</b>

<b>Pigframe</b>は主に Python を使ったゲーム開発プロジェクト向けのミニマムな ECS (Entity Component System) ライブラリです。言語が Python でゲーム開発に ECS を採用したいケースはごく稀だとは思いますが、
ECS がやれてシーンマネージャー機能もついている 1 つの OSS が(開発を始めた時点では) 存在しなかったので、このライブラリを制作しました。

個人ゲーム開発者にとって、以下のような機能を備えたフレームワークを歓迎する方は少なくないのではないかと考えています：

### 主な特徴:

- <b>ECS（Entity Component System）ができる</b> ゲームの全要素を整数のオブジェクトIDとデータとして管理し、ロジックを完全に分離できる
- <b>実用的なシーンマネージャー機能もついている</b> (オプションで使わない選択もできる)
- <b>エンジン依存の物理システムをある程度抽象化して扱える機能</b>

これらの機能が組み合わさって１つのライブラリとして提供されていると、個人開発者にとってゲーム開発体験を結構向上させられると実感しています。

### はじめかた:
Pigframe を始めるには、PyPI から `pigframe` をインストールするだけです。
Pigframe に依存するパッケージはありません。

```bash
pip install -U pigframe # pigframe has no dependencies.
```

### 使い方:

- モジュールをインポートする
    ```python
    from pigframe import World, System, Event, Screen, Component
    ```

- 専用の world クラスを作成する。world クラスは エンティティー, エンティティーに紐づいたコンポーネント, システム, イベント, 画面処理 を管理するゲームのコアとなるクラスです。
    ```python
    # Implement World class for your own project.
    class App(World):
        def __init__(self):
            super().__init__()
            self.init() # write initial process which is unique to the game engine and the game you develop.
        
        ... # other game engine unique methods.
    
    app = App()
    ```

- エンティティーをワールドに追加、削除する
    ```python
    # Create entity to world.
    entity = app.create_entity() # -> int: entity ID
    # Remove entity from world.
    app.remove_entity(entity) # deletes from entites list
    ```

- エンティティーにコンポーネントを追加/削除する
    - エンティティーにコンポーネントを追加する
    ```python
    # Add component to entity ID.
    # Components are recorded as values where entity ID is the key inside dict.
    # Component instance are created automatically.
    app.add_component_to_entity(entity, ComponentA, **component_args) # ComponentA is not an instance of Component but type.
    app.add_component_to_entity(entity, ComponentB(**component_args)) # this is wrong way of use.
    # getter
    app.get_component(ComponentA) # Returns the list of tuple: entity id which has ComponentA, component object. -> list((int, ComponentA object))
    app.get_components(ComponentA, ComponentB) # Returns the list of tuple: entity id (which has ComponentA and ComponentB), tuple of components objects. -> list((int, (ComponentA obj, ComponentB obj)) 
    ```

    - エンティティーに紐づいているコンポーネントを削除する
    ```python
    app.add_component_to_entity(ent, ComponentA, component_argsA)
    app.add_component_to_entity(ent, ComponentB, component_argsB)
    app.remove_component_from_entity(ent, ComponentA) # remove single component instance from entity

    app.add_component_to_entity(ent, ComponentC, component_argsC)
    app.remove_components_from_entity(ent, ComponentB, ComponentC) # remove components instances from entity
    ```

- コンポーネントの値を syste, event, screen で使う
    ```python
    # Example of using get_components() method.
    class SystemA(System):
        def process(self):
            for ent, (pos, vel) in self.world.get_components(Position, Velocity):
                """
                This method returns
                -------
                list: list of tuple: entity id, list of components
                """
                pos.x += vel.x
                pos.y += vel.y
    ```

- エンティティーを使う
    ```python
    # Example of using entity object
    class EventA(Event):
        def __process(self):
            player = self.world.get_entity_object(entity = 0)
            """
            This method returns a dict
            -----------
            dict: entity object
                key: component type
                value: component
            """
    ```

- ゲームのシーンをワールドに追加する
    ```python
    # Add scenes to world.
    app.add_scenes(["launch", "game", "result", "settings"])
    app.add_scene("game_over")
    # scenes getter
    app.sceneces # -> [["launch", "game", "result", "settings", "game_over"]
    ```

- ゲームのシステムをワールドに追加・削除する
    ```python
    # Add screen to a scene of world. Be sure you have added scenes before adding screens.
    # System instance are created automatically.
    app.add_system_to_scenes(SystemA, "launch", priority = 0, **system_args)
    # system with its lower priority than the other systems is executed in advance., by default 0.
    # World calls System A then System B.
    app.add_system_to_scenes(SystemA, "game", priority = 0, **system_args)
    app.add_system_to_scenes(SystemB, "launch", priority = 1)
    # Remove system from scene.
    app.remove_system_from_scene(SystemA, ["launch", "game"])
    ```

- 画面処理をワールドに追加・削除する
    ```python
    # Add screen to a scene of world. Be sure you have added scenes before adding screens.
    # Screen instance are created automatically.
    app.add_screen_to_scenes(ScreenA, "launch", priority = 0)
    app.add_screen_to_scenes(ScreenB, "launch", priority = 0)
    app.add_screen_to_scenes(ScreenC, "game", priority = 0, **screen_args)
    # Remove screen from scene.
    app.remove_screen_from_scene(ScreenB, "launch")
    ```

- イベント処理をワールドに追加・削除する
    ```python
    # Add an event, event triger to a scene of world. Be sure you have added scenes before adding events.
    # Event instance are created automatically.
    app.add_event_to_scene(EventA, "game", callable_triger, priority = 0)
    # Remove event from scene.
    app.remove_event_from_scene(EventA, "game")
    ```

- 状態遷移（シーン・ステート遷移に使えるもの）を追加する
    ```python
    app.add_scene_transition(scene_from = "launch", scene_to = "game", triger = callable_triger)
    # triger has to be callable.
    ```

- システム、イベント、画面処理を実行する
     ```python
    # Pyxel Example
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

セーブデータをロードする際に、いくつかのコンポーネントのパラメータが `entity_id` である場合、
`create_entity` メソッドに `entity_id` を渡し、`World` クラスの `set_next_entity_id` メソッドを使用して、
前のゲームと現在のゲームセッション間で 同じ `entity_id` が同じゲームオブジェクトを表すことを保証します。

```python
## セッション1
a = world.create_entity() # -> 0
b = world.create_entity() # -> 1
c = world.create_entity() # -> 2
world.add_components_to_entity(c, Relation, friends=[b])
## aを削除
world.remove_entity(a)
```

```python
## セッション2
max_entity_id = 0
for entity_id, data in loaded_data:
    world.create_entity(entity_id=entity_id) # セッション間で同じ `entity_id` が同じゲームオブジェクトを表すことを保証します。
    for component_name, component_data in data["components"].items():
        component_class = globals()[component_name]
        world.add_component_to_entity(entity_id, component_class, **component_data)
    max_entity_id = max(max_entity_id, entity_id)
... # ロード後
world.set_next_entity_id(max_entity_id + 1) # `entity_id` の競合を防ぐ
```

実際のゲームプロジェクトでの使用例を確認したい場合は、Pigframe を使用した極めてシンプルなプロジェクトを以下にリストアップしています。

#### 使用例
| ゲームエンジン | 例 | 内容 |
| ---- | ----| ---- |
| Pyxel | [2D shooting game](https://github.com/passive-radio/pigframe/tree/main/src/pigframe/examples/pyxel_2d_shooting) | システム、イベント、コンポーネント、エンティティー、ワールドの実装例 |
| Pygame | [control a ball](https://github.com/passive-radio/pigframe/tree/main/src/pigframe/examples/pygame_control_a_ball) | システム、イベント、コンポーネント、エンティティー、ワールドの実装例 |
| Pyxel | [control a ball](https://github.com/passive-radio/pigframe/tree/main/src/pigframe/examples/pyxel_control_a_ball) | システム、イベント、コンポーネント、エンティティー、ワールドの実装例 |

### コントリビューティング:
バグレポート、機能リクエスト、コードの貢献など、Pigframe をより良いライブラリにするためのどんなインプットも貴重だと考えます。どのような形であれ PR, issue を歓迎します。
