import pytest
from pigframe.scene import SceneManager
from pigframe.event import Event


def test_scene_manager_initialization():
    """シーンマネージャーの初期化をテストします"""
    scene_manager = SceneManager()
    assert scene_manager.current_scene is None
    assert scene_manager.next_scene is None
    assert scene_manager.prev_scene is None
    assert len(scene_manager.scenes) == 0


def test_scene_management():
    """シーンの追加と取得をテストします"""
    scene_manager = SceneManager()
    
    # シーンの追加
    scene_manager.add_scene("title")
    scene_manager.add_scene("game")
    scene_manager.add_scene("game_over")
    
    # シーンが正しく追加されているかチェック
    assert "title" in scene_manager.scenes
    assert "game" in scene_manager.scenes
    assert "game_over" in scene_manager.scenes
    
    # 一括でシーン追加
    scene_manager.add_scenes(["options", "credits"])
    assert "options" in scene_manager.scenes
    assert "credits" in scene_manager.scenes


def test_scene_transitions():
    """シーン遷移をテストします"""
    scene_manager = SceneManager()
    
    # シーンの追加
    scene_manager.add_scenes(["title", "game", "game_over"])
    
    # 初期シーン設定
    scene_manager.current_scene = "title"
    assert scene_manager.current_scene == "title"
    
    # シーン遷移トリガーを定義
    title_to_game_triggered = False
    
    def title_to_game_trigger():
        return title_to_game_triggered
    
    # シーン遷移を設定
    scene_manager.add_scene_transition("title", "game", title_to_game_trigger)
    
    # トリガーがFalseのとき、遷移しないことを確認
    scene_manager.process()
    assert scene_manager.current_scene == "title"
    assert scene_manager.next_scene is None
    
    # トリガーをTrueにして遷移を発生させる
    title_to_game_triggered = True
    scene_manager.process()
    scene_manager.update_scene()
    
    # シーン遷移が起きたことを確認
    assert scene_manager.current_scene == "game"
    assert scene_manager.prev_scene == "title"


def test_scene_events():
    """シーンイベントの処理をテストします"""
    scene_manager = SceneManager()
    
    # モックイベントクラス
    class MockEvent(Event):
        def __init__(self, world=None, priority=0, **kwargs):
            if world is None:
                pass  # Eventクラスの初期化をスキップ（テスト用）
            else:
                super().__init__(world, priority, **kwargs)
                
        def __process(self):
            pass
    
    # シーンの追加
    scene_manager.add_scene("game")
    
    # イベントトリガーを定義
    event_triggered = False
    
    def event_trigger():
        return event_triggered
    
    # イベントの追加
    scene_manager.add_scene_event("game", MockEvent, event_trigger)
    
    # 現在のシーンを設定
    scene_manager.current_scene = "game"
    
    # イベントが未トリガーのとき、runフラグが0であることを確認
    scene_manager.process()
    assert scene_manager.scenes_events["game"][MockEvent]["run"] == 0
    
    # イベントをトリガーし、runフラグが1になることを確認
    event_triggered = True
    scene_manager.process()
    assert scene_manager.scenes_events["game"][MockEvent]["run"] == 1 