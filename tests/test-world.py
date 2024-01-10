from pigframe.world import World, System, Screen

def test():
    app = World()
    app.add_scenes(["scene1", "scene2", "scene3"])
    app.add_system(System(app), 0)
    app.add_screen(Screen(app), 0)
    app.current_scene = "scene1"
    
    app.process_systems()
    app.draw_screens()
    print(app.scenes)
    print(app.systems)
    print(app.screens)
    print("passed!")
    
if __name__ == "__main__":
    test()