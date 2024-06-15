from pigframe.world import Event
from component import *
from entity import *

class EvRestart(Event):
    def _Event__process(self):
        entity_ids = [ent for ent in self.world.entities]
        for ent in entity_ids:
            self.world.remove_entity(ent)
        
        print(self.world.entities)
        print(self.world.components)
        self.world.next_entity_id = 0
        Player(self.world, 100, 100).create()
        Enemy(self.world, 20, 160).create()

        print(self.world.entities)
        print(self.world.components)
        
        for ent, (player) in self.world.get_component(Playable):
            print(player.hp)