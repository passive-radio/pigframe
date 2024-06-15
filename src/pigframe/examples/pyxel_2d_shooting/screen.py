from pigframe.world import Screen
import pyxel
from component import *

class ScLaunch(Screen):
    def draw(self):
        pyxel.cls(0)
        pyxel.text(100, 100, "Press ENTER to Start", pyxel.frame_count % 16)

class ScEnemy(Screen):
    def draw(self):
        for ent, (enm) in self.world.get_component(CpEnemy):
            pos = self.world.get_entity_object(ent)[Position]
            pyxel.rect(pos.x, pos.y, 16, 16, 2)  # Example: Draw a rectangle for each entity
            pyxel.text(pos.x, pos.y, str(enm.hp), 7)
            pyxel.text(pos.x + 6, pos.y + 6, "E", 7)

class ScBG(Screen):
    def draw(self):
        pyxel.cls(0)
        
class ScStatus(Screen):
    def draw(self):
        for ent, (player) in self.world.get_component(Playable):
            pyxel.text(4, 10, f"Score: {player.score}", 7)

class ScPlayable(Screen):
    def draw(self):
        for ent, (playable) in self.world.get_component(Playable):
            pos = self.world.get_entity_object(ent)[Position]
            pyxel.rect(pos.x, pos.y, 16, 16, 8)  # Example: Draw a rectangle for each entity
            pyxel.text(pos.x, pos.y, str(playable.hp), 7)
            pyxel.text(pos.x + 6, pos.y + 6, "P", 7)

class ScGameOver(Screen):
    def draw(self):
        pyxel.cls(0)
        for ent, (player) in self.world.get_component(Playable):
            print(f"Player HP: {player.hp}")
            print(f"Player Score: {player.score}")
            score = player.score
        pyxel.text(100, 130, f"Score: {score}", 7)
        pyxel.text(100, 100, "Game Over! Press SPACE to Restart", 7)

class ScDrawBullet(Screen):
    def draw(self):
        # Draw projectiles if they exist
        entities_dict: dict = self.world.entities
        entity_ids = [ent for ent in entities_dict]
        has_bullet = False
        for ent in entity_ids:
            if self.world.has_component(ent, Bullet):
                has_bullet = True
                break
        
        if not has_bullet:
            return
        
        for ent, (bul) in self.world.get_component(Bullet):
            pos = self.world.get_entity_object(ent)[Position]
            pyxel.rect(pos.x, pos.y, 2, 3, 7)  # Example: Draw a rectangle for each entity