import math
import pygame
from algorithms.behavior_tree import Selector, Sequence, Condition, Action, BTState

class EnemyFSM:
    MOVING = "moving"
    SLOWED = "slowed"
    FLEEING = "fleeing"
    WAITING = "waiting"
    DEAD = "dead"

class Enemy:
    def __init__(self, path, tile_size):
        self.path = path
        self.tile_size = tile_size
        self.pos = pygame.Vector2(
            path[0][0] * tile_size + tile_size // 2,
            path[0][1] * tile_size + tile_size // 2,
        )
        self.target_waypoint_index = 1
        self.speed = 100
        self.base_speed = 100
        self.is_alive = True
        self.hp = 100
        self.max_hp = 100
        self.reward = 15
        self.base_damage = 1
        self.reached_base = False
        self.angle = 0
        self.type_name = "basic"
        
        self.state = EnemyFSM.MOVING
        self.slow_factor = 1.0
        self.slow_timer = 0.0
        self.flee_timer = 0.0
        
        self.behavior_tree = self._create_behavior_tree()
        self.nearby_healer = None

    def _create_behavior_tree(self):
        return Selector([
            Sequence([
                Condition(lambda e: e.hp < e.max_hp * 0.3),
                Action(self._flee_action)
            ]),
            Sequence([
                Condition(lambda e: e.nearby_healer is not None and e.hp < e.max_hp * 0.7),
                Action(self._wait_for_heal_action)
            ]),
            Action(self._follow_path_action)
        ])

    def _flee_action(self, enemy, dt):
        enemy.state = EnemyFSM.FLEEING
        flee_speed = enemy.base_speed * 1.5
        if enemy.target_waypoint_index < len(enemy.path):
            target_tile = enemy.path[enemy.target_waypoint_index]
            target_pos = pygame.Vector2(
                target_tile[0] * enemy.tile_size + enemy.tile_size // 2,
                target_tile[1] * enemy.tile_size + enemy.tile_size // 2,
            )
            move_vec = target_pos - enemy.pos
            if move_vec.length() > 0:
                enemy.angle = math.degrees(math.atan2(-move_vec.y, move_vec.x)) + 90
                enemy.pos += move_vec.normalize() * flee_speed * dt
                if move_vec.length() <= flee_speed * dt:
                    enemy.target_waypoint_index += 1
        return BTState.RUNNING

    def _wait_for_heal_action(self, enemy, dt):
        enemy.state = EnemyFSM.WAITING
        if enemy.nearby_healer and enemy.nearby_healer.is_alive:
            enemy.hp = min(enemy.max_hp, enemy.hp + 5 * dt)
        return BTState.RUNNING

    def _follow_path_action(self, enemy, dt):
        enemy.state = EnemyFSM.MOVING
        if enemy.target_waypoint_index >= len(enemy.path):
            enemy.reached_base = True
            enemy.is_alive = False
            enemy.state = EnemyFSM.DEAD
            return BTState.SUCCESS

        target_tile = enemy.path[enemy.target_waypoint_index]
        target_pos = pygame.Vector2(
            target_tile[0] * enemy.tile_size + enemy.tile_size // 2,
            target_tile[1] * enemy.tile_size + enemy.tile_size // 2,
        )

        move_vec = target_pos - enemy.pos
        distance = move_vec.length()

        if distance > 0:
            enemy.angle = math.degrees(math.atan2(-move_vec.y, move_vec.x)) + 90

        current_speed = enemy.base_speed * enemy.slow_factor
        if distance <= current_speed * dt:
            enemy.pos = target_pos
            enemy.target_waypoint_index += 1
        else:
            enemy.pos += move_vec.normalize() * current_speed * dt
        
        return BTState.RUNNING

    def apply_slow(self, factor, duration):
        self.slow_factor = factor
        self.slow_timer = duration
        self.state = EnemyFSM.SLOWED

    def update_slow_effect(self, dt):
        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.slow_factor = 1.0
                if self.state == EnemyFSM.SLOWED:
                    self.state = EnemyFSM.MOVING

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.is_alive = False
            self.state = EnemyFSM.DEAD

    def update(self, dt, nearby_enemies=None):
        if not self.is_alive:
            return

        self.update_slow_effect(dt)
        
        if nearby_enemies:
            self.nearby_healer = None
            for enemy in nearby_enemies:
                if enemy.type_name == "healer" and enemy.is_alive:
                    distance = self.pos.distance_to(enemy.pos)
                    if distance < 100:
                        self.nearby_healer = enemy
                        break

        self.behavior_tree.tick(self, dt)

        if self.target_waypoint_index >= len(self.path):
            self.reached_base = True
            self.is_alive = False
            self.state = EnemyFSM.DEAD