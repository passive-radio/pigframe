from pigframe.world import Event
from component import *
from entity import *

class EvRestart(Event):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
        self.cnt_restart = 0
    
    def _Event__process(self):
        entity_ids = [ent for ent in self.world.entities]
        for ent in entity_ids:
            self.world.remove_entity(ent)
        
        print(self.world.entities)
        print(self.world.components)
        self.world.next_entity_id = 0
        Player(self.world, 100, 100).create()
        Enemy(self.world, 20, 40).create()

        print(self.world.entities)
        print(self.world.components)
        
        self.world.scene_manager.next_scene = "game"