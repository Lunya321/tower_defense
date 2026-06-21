import os
import pygame

class AssetManager:
    def __init__(self, tile_size=40):
        self.tile_size = tile_size
        self.towers = {}
        self.enemies = {}
        self.projectiles = {}
        self.effects = {}
        self.load_assets()

    def load_assets(self):
        img_base = os.path.join("assets", "images")

        proj_dir = os.path.join(img_base, "projectiles")
        try:
            arrow_img = pygame.image.load(
                os.path.join(proj_dir, "arrow.png")
            ).convert_alpha()
            snip_img = pygame.image.load(
                os.path.join(proj_dir, "snip.png")
            ).convert_alpha()
            cannon_img = pygame.image.load(
                os.path.join(proj_dir, "cannonball.png")
            ).convert_alpha()
            ice_img = pygame.image.load(
                os.path.join(proj_dir, "ice.png")
            ).convert_alpha()

            self.projectiles["arrow"] = pygame.transform.scale(
                arrow_img, (28, 12)
            )
            self.projectiles["snip"] = pygame.transform.scale(
                snip_img, (32, 12)
            )
            self.projectiles["cannonball"] = pygame.transform.scale(
                cannon_img, (14, 14)
            )
            self.projectiles["ice"] = pygame.transform.scale(ice_img, (16, 16))
        except Exception:
            pass

        towers_dir = os.path.join(img_base, "towers")
        try:
            tower_img = pygame.image.load(
                os.path.join(towers_dir, "arrow.png")
            ).convert_alpha()
            self.towers["arrow"] = pygame.transform.scale(
                tower_img, (self.tile_size, self.tile_size)
            )
        except Exception:
            pass

        enemies_dir = os.path.join(img_base, "enemies")
        enemy_types = ["basic", "fast", "tank", "healer"]
        for enemy_type in enemy_types:
            try:
                enemy_img = pygame.image.load(
                    os.path.join(enemies_dir, f"{enemy_type}.png")
                ).convert_alpha()
                self.enemies[enemy_type] = pygame.transform.scale(
                    enemy_img, (self.tile_size, self.tile_size)
                )
            except Exception:
                pass

        eff_dir = os.path.join(img_base, "effects")
        try:
            cannon_eff = pygame.image.load(
                os.path.join(eff_dir, "cannonball_effect.png")
            ).convert_alpha()
            ice_eff = pygame.image.load(
                os.path.join(eff_dir, "ice_effect.png")
            ).convert_alpha()

            self.effects["cannonball"] = pygame.transform.scale(
                cannon_eff, (24, 24)
            )
            self.effects["ice"] = pygame.transform.scale(ice_eff, (24, 24))
        except Exception:
            pass