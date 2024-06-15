from pigframe.world import System
from component import Position, Velocity, Movable, Playable, CpEnemy, Bullet
import random
from entity import Enemy


class SysPlayerMovement(System):
    def process(self):
        actions = self.world.actions
        screen_width = self.world.SCREEN_SIZE[0]
        screen_height = self.world.SCREEN_SIZE[1]

        for ent, (play) in self.world.get_component(Playable):
            pos = self.world.get_entity_object(ent)[Position]
            vel = self.world.get_entity_object(ent)[Velocity]
            mov = self.world.get_entity_object(ent)[Movable]
            
            # Reset velocity
            vel.x = 0
            vel.y = 0

            # Update velocity based on input
            if actions.up:
                vel.y = -mov.speed
            if actions.down:
                vel.y = mov.speed
            if actions.left:
                vel.x = -mov.speed
            if actions.right:
                vel.x = mov.speed

            # Update position based on velocity
            pos.x += vel.x
            pos.y += vel.y

            # Ensure player stays within screen bounds
            pos.x = max(0, min(screen_width - 16, pos.x))
            pos.y = max(0, min(screen_height - 16, pos.y))

class SysEnemyMovement(System):
    def process(self):
        screen_width = self.world.SCREEN_SIZE[0]
        screen_height = self.world.SCREEN_SIZE[1]

        for ent, (enm) in self.world.get_component(CpEnemy):
            pos = self.world.get_entity_object(ent)[Position]
            vel = self.world.get_entity_object(ent)[Velocity]
            mov = self.world.get_entity_object(ent)[Movable]
            # Randomly change direction occasionally
            if random.random() < 0.02:  # 2% chance each frame to change direction
                vel.x = random.choice([-1, 0, 1]) * mov.speed
                vel.y = random.choice([-1, 0, 1]) * mov.speed

            # Update position based on velocity
            pos.x += vel.x
            pos.y += vel.y

            # Ensure CpEnemy stays within screen bounds
            pos.x = max(0, min(screen_width - 16, pos.x))
            pos.y = max(0, min(screen_height - 16, pos.y))

class SysShooting(System):
    def process(self):
        actions = self.world.actions

        if actions.shoot:
            # Create a new projectile
            for ent, (_) in self.world.get_component(Playable):
                player_pos = self.world.get_entity_object(ent)[Position]
                bullet_entity = self.world.create_entity()
                print("Add bullet: ", bullet_entity)
                bullet_speed = 2
                self.world.add_component_to_entity(bullet_entity, Position, x = player_pos.x, y = player_pos.y)
                self.world.add_component_to_entity(bullet_entity, Velocity, x = 0, y = -bullet_speed)  # Shoot upwards
                self.world.add_component_to_entity(bullet_entity, Movable, speed = bullet_speed)
                self.world.add_component_to_entity(bullet_entity, Bullet)
                
                print(self.world.get_entity_object(bullet_entity))

        # Move projectiles if they exist
        entities_dict: dict = self.world.entities
        ent_ids = [ent for ent in entities_dict]
        has_bullet = False
        for ent in ent_ids:
            if self.world.has_component(ent, Bullet):
                has_bullet = True
                break
        
        if not has_bullet:
            return
        
        cnt_bullet = 0
        for ent, (pos) in self.world.get_component(Bullet):
            pos = self.world.get_entity_object(ent)[Position]
            vel = self.world.get_entity_object(ent)[Velocity]
            mov = self.world.get_entity_object(ent)[Movable]
            pos.x += vel.x * mov.speed
            pos.y += vel.y * mov.speed

            # Remove projectiles that are out of bounds
            if pos.y < 0 or pos.y > self.world.SCREEN_SIZE[1] or pos.x < 0 or pos.x > self.world.SCREEN_SIZE[0]:
                self.world.remove_entity(ent)
                continue
            
            cnt_bullet += 1

class SysBulletHitEnemy(System):
    def process(self):
        # Get all bullet and enemy entities
        bullets = []
        enemies = []
        
        entities_dict: dict = self.world.entities
        ent_ids = [ent for ent in entities_dict]
        has_bullet = False
        for ent in ent_ids:
            if self.world.has_component(ent, Bullet):
                has_bullet = True
                break
        
        if not has_bullet:
            return
        
        for ent, (bul) in self.world.get_component(Bullet):
            pos = self.world.get_entity_object(ent)[Position]
            bullets.append((ent, pos))

        for ent, (enm) in self.world.get_component(CpEnemy):
            pos = self.world.get_entity_object(ent)[Position]
            enemies.append((ent, pos))
        
        for ent, (player) in self.world.get_component(Playable):
            player_pos = self.world.get_entity_object(ent)[Position]
            player_ent = ent
            
        # Check for bullet-enemy collisions
        for enemy_ent, enemy_pos in enemies:
            for bullet_ent, bullet_pos in bullets:
                if self.check_collision(bullet_pos, enemy_pos):
                    self.world.remove_entity(bullet_ent)
                    if self.world.get_entity_object(enemy_ent) == None:
                        break
                    self.world.get_entity_object(enemy_ent)[CpEnemy].hp -= 1
                    self.world.get_entity_object(player_ent)[Playable].score += 1
                    # self.world.remove_entity(enemy_ent)

    @staticmethod
    def check_collision(pos1, pos2, size=16):
        return (abs(pos1.x - pos2.x) < size) and (abs(pos1.y - pos2.y) < size)

class SysPlayerHitEnemy(System):
    def process(self):
        # Check for enemy-player collisions
        for player_ent, (play) in self.world.get_component(Playable):
            for enemy_ent, (enm) in self.world.get_component(CpEnemy):
                if self.check_collision(self.world.get_entity_object(player_ent)[Position], self.world.get_entity_object(enemy_ent)[Position]):
                    print(f"Player hit by Enemy {enemy_ent}")
                    self.world.get_entity_object(player_ent)[Playable].hp -= 1
                    # Trigger game over event or reduce player health here

    @staticmethod
    def check_collision(pos1, pos2, size=16):
        return (abs(pos1.x - pos2.x) < size) and (abs(pos1.y - pos2.y) < size)

class SysKillEnemy(System):
    def process(self):
        # Remove enemies with 0 or less HP
        
        player_ent = self.world.get_component(Playable)[0][0]
        
        killed = 0
        for ent, (enm) in self.world.get_component(CpEnemy):
            if enm.hp > 0:
                continue
            self.world.remove_entity(ent)
            killed += 1
            print(f"Enemy {ent} killed")
            self.world.get_entity_object(player_ent)[Playable].score += 2
        
        if killed > 0:
            for i in range(killed + 1):
                Enemy(self.world, random.randint(0, 240), random.randint(0, 240)).create()

class SysGameOver(System):
    def process(self):
        # Check if player is dead
        for ent, (play) in self.world.get_component(Playable):
            if play.hp <= 0:
                self.world.scene_manager.next_scene = "game_over"