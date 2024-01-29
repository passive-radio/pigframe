## Pigframe
![Pigframe](https://github.com/passive-radio/pigframe/blob/main/docs//images/pigframe-logo-rectangle-200x99.jpg)

<b>[English](../README.md)</b>

<b>Pigframe</b>は、ゲームアプリケーションをより簡単に、ルールベースに開発できるようにすることを目的とした、ミニマムな Python 製のゲーム開発用フレームワークです。Pigframe は柔軟性と使いやすさを念頭に置いて設計されており、開発者がゲーム体験を作り出すために基本となる堅牢な機能を提供します。

#### 主な特徴:
- <b>コンポーネントベースのアーキテクチャ</b>: Pigframe はコンポーネントベースのアプローチを採用し、モジュラーでスケーラブルなゲーム開発を可能にします。このアーキテクチャは、ゲーム要素の簡単な追加、変更、管理を容易にします。

- <b>直感的なシーン管理</b>: Pigframe の直感的なシーン遷移と制御システムで、ゲームシーンをシームレスに管理します。この機能により、スムーズな遷移と効率的なシーンの整理が可能になります。

- <b>効率的なエンティティ-コンポーネントシステム</b>: Pigframe の中心は、機能の分離を促しパフォーマンスを高めるのに効果的なエンティティ-コンポーネントシステム（ECS）です。

- <b>Python でわかりやすい</b>: Pigframe はシンプルさと可読性の高い Python で書かれています。Python でゲーム開発を学びたい人、ゲームを作ってみたい人、アクセスしやすいが頑健なツールを求めている個人開発者に最適におすすめのフレームワークです。

- <b>併用しやすい</b>: Pigframe は、Pyxel や Pygame のような人気のある Python ゲームエンジンライブラリを使って多様で創造的なゲームを開発したいときに使うとピッタリです。

#### はじめかた:
Pigframe を始めるには、pip を使用してパッケージをインストールするだけです:

```bash
pip install pigframe
```

#### コントリビューティング:
バグレポート、機能リクエスト、コードの貢献など、Pigframe をより良いツールにするためどんなインプットも貴重だと考えます。どのような形でも Pigframe への貢献を歓迎いたします。

#### ユーザーガイド:

- モジュールをインポートする
    ```python
    from pigframe.world import World, System, Event, Screen, Component
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

- エンティティーにコンポーネントを追加する
    ```python
    # Add component to entity ID.
    # Components are recorded as values where entity ID is the key inside dict.
    # Component instance are created automatically.
    app.add_component_to_entity(entity, ComponentA, component_args) # ComponentA is not an instance of Component but type.
    app.add_component_to_entity(entity, ComponentB, component_args) # ComponentB is not an instance of Component but type.
    # getter
    app.get_component(ComponentA) # Returns the list of tuple: entity id which has ComponentA, component implementation. 
    app.get_components(ComponentA, ComponentB) # Returns the list of tuple: entity id which has ComponentA and ComponentB, component implementations. 
    ```

- コンポーネントの値を syste, event, screen で使う
    ```python
    # Example of using get_components() method.
    class SystemA(System):
        def process(self):
            for ent, (component_a, component_b) in self.world.get_components(ComponentA, ComponentB):
                """
                Returns
                -------
                list: list of tuple: entity id, list of components
                """
                component_a.x += component_b.x
                component_a.y += component_b.x
    ```

- エンティティーを使う
    ```python
    # Example of using entity object
    class EventA(Event):
        def __process(self):
            player = self.world.get_entity_object(entity = 0)
            """
            Returns
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
    # scenes getter
    app.sceneces # -> [["launch", "game", "result", "settings"]
    ```

- ゲームのシステムをワールドに追加・削除する
    ```python
    # Add screen to a scene of world. Be sure you have added scenes before adding screens.
    # System instance are created automatically.
    app.add_system_to_scenes(SystemA, "launch", priority = 0, system_args)
    # system with its lower priority than the other systems is executed in advance., by default 0.
    # For here, SystemA().process() runs first in "launch" scene.
    app.add_system_to_scenes(SystemA, "game", priority = 0, system_args)
    app.add_system_to_scenes(SystemB, "launch", priority = 1)
    # Remove system from scene.
    app.remove_system_from_scene(SystemA, ["launch", "game"], system_args = system_args)
    ```

- 画面処理をワールドに追加・削除する
    ```python
    # Add screen to a scene of world. Be sure you have added scenes before adding screens.
    # Screen instance are created automatically.
    app.add_screen_to_scenes(ScreenA, "launch", priority = 0)
    app.add_screen_to_scenes(ScreenB, "launch", priority = 0)
    app.add_screen_to_scenes(ScreenC, "game", priority = 0, screen_args)
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

- 状態遷移（シーン・レベル遷移に使えるもの）を追加する
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
            # 1. level_manager.process()

        def draw(self):
            self.process_screens()
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

#### 使用例
| ゲームエンジン | 例 | 内容 |
| ---- | ----| ---- |
| Pygame | [control a ball](https://github.com/passive-radio/pigframe/tree/main/src/pigframe/examples/pygame_control_a_ball) | システム、イベント、コンポーネント、エンティティー、ワールドの実装例 |
| Pyxel | [control a ball](https://github.com/passive-radio/pigframe/tree/main/src/pigframe/examples/pyxel_control_a_ball) | システム、イベント、コンポーネント、エンティティー、ワールドの実装例 |