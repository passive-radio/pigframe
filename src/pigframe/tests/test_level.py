from pigframe.scene import SceneManager
from pigframe import Event


class Event1(Event):
    def _Event__process(self):
        pass


def test():
    scene_manager = SceneManager()
    scene_manager.add_scenes(["scene1", "scene2", "scene3"])
    scene_manager.add_scene_transition("scene1", "scene2", lambda: 1 == 1)
    scene_manager.add_scene_event("scene1", Event1, lambda: 1 == 2)
    assert True


if __name__ == "__main__":
    test()
