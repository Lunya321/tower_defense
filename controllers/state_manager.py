from models.map_model import MapModel
from models.wave_manager import WaveManager
from models.effects import VisualEffect
from views.map_renderer import MapRenderer

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class StateManager:
    def __init__(self, screen, asset_manager):
        self.screen = screen
        self.asset_manager = asset_manager
        self.state = GameState.MENU
        self.map_model = None
        self.map_renderer = None
        self.wave_manager = None
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.effects = []
        self.money = 100
        self.base_hp = 20
        self.enemies_killed = 0
        self.gold_earned = 0

    def start_new_game(self):
        self.map_model = MapModel()
        self.asset_manager.tile_size = self.map_model.tile_size
        self.map_renderer = MapRenderer(self.screen, self.map_model)
        self.wave_manager = WaveManager(self.map_model.path, self.map_model.tile_size)
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        self.effects.clear()
        self.money = 100
        self.base_hp = 20
        self.enemies_killed = 0
        self.gold_earned = 0
        self.state = GameState.PLAYING

    def update(self, dt, spatial_hash, sound_manager):
        if self.state != GameState.PLAYING:
            return

        if self.base_hp <= 0:
            self.state = GameState.GAME_OVER
            sound_manager.play_sfx("game_over")
            return

        if self.wave_manager.current_wave > 5 and len(self.enemies) == 0:
            self.state = GameState.GAME_OVER
            sound_manager.play_sfx("game_over")
            return

        new_enemy = self.wave_manager.update(dt, len(self.enemies))
        if new_enemy:
            self.enemies.append(new_enemy)

        spatial_hash.clear()
        for enemy in self.enemies:
            spatial_hash.insert(enemy)

        for enemy in self.enemies:
            nearby_enemies = spatial_hash.get_nearby(enemy.pos.x, enemy.pos.y, 100)
            enemy.update(dt, nearby_enemies)

        for tower in self.towers:
            nearby_enemies = spatial_hash.get_nearby(tower.pos.x, tower.pos.y, tower.range)
            new_projectile = tower.update(dt, nearby_enemies)
            if new_projectile:
                self.projectiles.append(new_projectile)
                if tower.type_name == "arrow" or tower.type_name == "sniper":
                    sound_manager.play_sfx("arrow_shoot")
                elif tower.type_name == "cannon":
                    sound_manager.play_sfx("cannon_shoot")

        for proj in self.projectiles:
            proj.update(dt)
            if hasattr(proj, 'effect_type') and not proj.is_active:
                effect = VisualEffect(proj.pos, proj.effect_type, duration=0.3)
                self.effects.append(effect)

        for effect in self.effects:
            effect.update(dt)

        for enemy in self.enemies:
            if not enemy.is_alive:
                if enemy.reached_base:
                    self.base_hp -= enemy.base_damage
                    sound_manager.play_sfx("base_hit")
                else:
                    self.money += enemy.reward
                    self.enemies_killed += 1
                    self.gold_earned += enemy.reward
                    sound_manager.play_sfx("enemy_death")

        self.enemies = [e for e in self.enemies if e.is_alive]
        self.projectiles = [p for p in self.projectiles if p.is_active]
        self.effects = [e for e in self.effects if e.is_active]