## Pigframe
![Pigframe](https://github.com/passive-radio/pigframe/blob/main/docs//images/pigframe-logo-rectangle-200x99.jpg)

<b>[English](../README.md)</b>

<b>Pigframe</b>は、ゲームアプリケーションの開発プロセスを簡素化し、合理化することを目的とした、最小限のPythonベースのゲームエンジンバックエンドライブラリです。柔軟性と使いやすさを念頭に置いて設計されたPigframeは、開発者が没入型でダイナミックなゲーム体験を作り出すための堅牢なツールと機能を提供します。

#### 主な特徴:
- <b>コンポーネントベースのアーキテクチャ</b>: Pigframeはコンポーネントベースのアプローチを採用し、モジュラーでスケーラブルなゲーム開発を可能にします。このアーキテクチャは、ゲーム要素の簡単な追加、変更、管理を容易にします。

- <b>直感的なシーン管理</b>: Pigframeの直感的なシーン遷移と制御システムで、ゲームシーンをシームレスに管理します。この機能により、スムーズな遷移と効率的なシーンの整理が可能になります。

- <b>効率的なエンティティ-コンポーネントシステム</b>: Pigframeの中心には、関心の分離を促進し、パフォーマンスを高める効率的なエンティティ-コンポーネントシステム（ECS）があります。

- <b>Python的なシンプルさ</b>: シンプルさと可読性のPythonの哲学で設計されたPigframeは、ゲーム開発を学ぶ人や、アクセスしやすいが強力なツールを求める個々の開発者に最適です。

- <b>多様な統合</b>: Pigframeは、PyxelやPygameのような人気のあるPythonゲームライブラリとシームレスに動作するよう最適化されており、多様で創造的なゲーム開発プロジェクトに最適な選択です。

#### はじめかた:
Pigframeを始めるには、pipを使用してパッケージをインストールするだけです:

```bash
pip install pigframe
```

#### コントリビューティング:
Pigframeへの貢献を歓迎します！バグレポート、機能リクエスト、コードの貢献など、あなたのインプットはPigframeをみんなのためにより良くするために貴重です。

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

- エンティティーを追加、削除する
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
    app.add_component_to_entity(entity, ComponentA(some_args))
    app.add_component_to_entity(entity, ComponentB(some_args))
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

- ゲームのシーンを world に追加する
    ```python
    # Add scenes to world.
    app.add_scenes(["launch", "game", "result", "settings"])
    # scenes getter
    app.sceneces # -> [["launch", "game", "result", "settings"]
    ```

- ゲームのシステムを world に追加・削除する
    ```python
    # Add screen to a scene of world. Be sure you have added scenes before adding screens.
    app.add_scene_system(SystemA(app), "launch", priority = 0)
    # system with its lower priority than the other systems is executed in advance., by default 0.
    # For here, SystemA().process() runs first in "launch" scene.
    app.add_scene_system(SystemA(app), "game", priority = 0)
    app.add_scene_system(SystemB(app), "launch", priority = 1)
    # Remove system from scene.
    app.remove_system_from_scene(SystemA, ["launch", "game"])
    ```

- 画面処理をゲームに追加・削除する
    ```python
    # Add screen to a scene of world. Be sure you have added scenes before adding screens.
    app.add_scene_screen(ScreenA(app), "launch", priority = 0)
    app.add_scene_screen(ScreenB(app), "launch", priority = 0)
    app.add_scene_screen(ScreenC(app), "game", priority = 0)
    # Remove screen from scene.
    app.remove_screen_from_scene(ScreenB, "launch")
    ```

- イベント処理をゲームに追加・削除する
    ```python
    # Add an event to a scene of world. Be sure you have added scenes before adding events.
    app.add_scene_event(EventA(app), "game", priority = 0)
    # Remove event from scene.
    app.remove_event_from_scene(EventA, "game")
    ```

- シーン・レベル（状態）遷移を追加する
    ```python
    app.add_scene_map(scene = "launch", to = "game", triger = callable_triger)
    # triger has to be callable.
    ```

- イベントを実行するトリガーを追加する
    ```python
    app.add_scene_events_map(scene = "game", event_name = "event name", triger = callable_triger)
    # triger has to be callable
    ```

- システム、イベント、画面処理を実行する
    ```python
    app.process_systems() # execute systems of current scene.
    app.process_events() # execute events of current scene.
    app.draw_screens() # execute screens of current scene.
    ```

#### 使用例
| ゲームエンジン | 例 |
| ---- | ----|
| Pyxel | https://github.com/passive-radio/pigframe/tree/main/examples/control_a_ball |