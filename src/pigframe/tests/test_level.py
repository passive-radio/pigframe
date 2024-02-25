from pigframe.scene import SceneManager

def test():
    scene_manager = SceneManager()
    scene_manager.add_scenes(["scene1", "scene2", "scene3"])
    scene_manager.add_scene_map("scene1", "scene2", lambda: 1 == 1)
    scene_manager.add_scene_events("scene1", "event1", lambda: 1 == 2)
    
    print("passed!")
    
if __name__ == "__main__":
    test()