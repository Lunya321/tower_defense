import math
import pygame


class GameView:

    def __init__(self, screen, asset_manager):
        self.screen = screen
        self.assets = asset_manager

    def draw_tower(self, tower, target_enemy=None):
        type_name = getattr(tower, "type_name", None)
        sprite = self.assets.towers.get(type_name) if type_name else None

        if not sprite:
            pygame.draw.circle(
                self.screen,
                (0, 0, 255),
                (int(tower.pos.x), int(tower.pos.y)),
                15,
            )
            return

        angle = 0
        if target_enemy:
            dx = target_enemy.pos.x - tower.pos.x
            dy = target_enemy.pos.y - tower.pos.y
            angle = math.degrees(math.atan2(-dy, dx)) - 90

        rotated_sprite = pygame.transform.rotate(sprite, angle)
        tower_rect = rotated_sprite.get_rect(center=tower.pos)
        self.screen.blit(rotated_sprite, tower_rect.topleft)

    def draw_enemy(self, enemy):
        type_name = getattr(enemy, "type_name", "basic")
        sprite = self.assets.enemies.get(type_name) if type_name else None

        if not sprite:
            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (int(enemy.pos.x), int(enemy.pos.y)),
                15,
            )
            self._draw_health_bar(enemy)
            return

        rotated_sprite = pygame.transform.rotate(sprite, enemy.angle)
        enemy_rect = rotated_sprite.get_rect(center=enemy.pos)
        self.screen.blit(rotated_sprite, enemy_rect.topleft)
        self._draw_health_bar(enemy)

    def _draw_health_bar(self, enemy):
        max_hp = getattr(enemy, "max_hp", 100)
        health_ratio = max(0, enemy.hp / max_hp)
        bar_width = int(enemy.tile_size * 0.8)
        bar_height = 4
        bar_x = int(enemy.pos.x - bar_width // 2)
        bar_y = int(enemy.pos.y - enemy.tile_size // 2 - 8)

        pygame.draw.rect(
            self.screen, (30, 30, 30), (bar_x, bar_y, bar_width, bar_height)
        )
        current_bar_width = int(bar_width * health_ratio)
        color = (0, 255, 0) if health_ratio > 0.5 else (255, 0, 0)
        pygame.draw.rect(
            self.screen, color, (bar_x, bar_y, current_bar_width, bar_height)
        )