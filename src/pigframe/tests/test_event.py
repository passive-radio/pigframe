import pytest
from dataclasses import dataclass
from pigframe.world import World
from pigframe.event import Event
from pigframe.component import Component


# 実際のWorldクラスを継承した具体クラス
class TestableWorld(World):
    def __init__(self):
        super().__init__()


@dataclass
class GameState(Component):
    score: int = 0
    is_game_over: bool = False


class TestEvent(Event):
    def __init__(self, world, priority=0, **kwargs):
        super().__init__(world, priority, **kwargs)
        self.executed = False
    
    def _Event__process(self):
        self.executed = True
        
        # イベント内でエンティティのコンポーネントを操作するテスト
        for entity_id, game_state in self.world.get_component(GameState):
            game_state.score += 10


class GameOverEvent(Event):
    def __init__(self, world, priority=0, **kwargs):
        super().__init__(world, priority, **kwargs)
    
    def _Event__process(self):
        for entity_id, game_state in self.world.get_component(GameState):
            game_state.is_game_over = True


def test_event_registration():
    """イベントの登録と実行をテストします"""
    world = TestableWorld()
    
    # シーンを作成
    world.add_scenes(["game", "game_over"])
    world.current_scene = "game"
    
    # イベントトリガーの設定
    trigger_condition = False
    world.add_event_to_scene(TestEvent, "game", lambda: trigger_condition)
    
    # ゲーム状態を持つエンティティを作成
    entity = world.create_entity()
    world.add_component_to_entity(entity, GameState, score=0, is_game_over=False)
    
    # イベントをトリガーしない状態でプロセスを実行
    world.process_events()
    
    # イベントが実行されていないことを確認
    entity_obj = world.get_entity_object(entity)
    assert entity_obj is not None
    game_state = entity_obj[GameState]
    assert game_state.score == 0
    
    # イベントをトリガーする
    trigger_condition = True
    
    # プロセスを手動で設定してイベント発生を模倣
    event_type = TestEvent
    scene = "game"
    world.scene_manager.scenes_events[scene][event_type]["run"] = 1
    
    # イベント処理
    world.process_events()
    
    # イベントが実行されたことを確認
    entity_obj = world.get_entity_object(entity)
    assert entity_obj is not None
    game_state = entity_obj[GameState]
    assert game_state.score == 10


def test_scene_transitions_with_events():
    """イベントによるシーン遷移をテストします"""
    world = TestableWorld()
    
    # シーンを作成
    world.add_scenes(["game", "game_over"])
    world.current_scene = "game"
    
    # ゲームオーバー状態を検出するトリガー関数
    def game_over_trigger():
        for _, game_state in world.get_component(GameState):
            if game_state.is_game_over:
                return True
        return False
    
    # シーン遷移の設定
    world.add_scene_transition("game", "game_over", game_over_trigger)
    
    # ゲーム状態を持つエンティティを作成
    entity = world.create_entity()
    world.add_component_to_entity(entity, GameState, score=0, is_game_over=False)
    
    # ゲームオーバーイベントの登録
    world.add_event_to_scene(GameOverEvent, "game", lambda: True)
    
    # イベントを手動で設定
    event_type = GameOverEvent
    scene = "game"
    world.scene_manager.scenes_events[scene][event_type]["run"] = 1
    
    # イベント処理
    world.process_events()
    
    # ゲームオーバーフラグが設定されたことを確認
    entity_obj = world.get_entity_object(entity)
    assert entity_obj is not None
    game_state = entity_obj[GameState]
    assert game_state.is_game_over is True
    
    # 通常の処理ループを実行
    world.process()
    
    # シーンが変更されたことを確認
    assert world.current_scene == "game_over" 