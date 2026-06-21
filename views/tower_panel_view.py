import pygame

class TowerPanelView:
    def __init__(self, screen, asset_manager):
        self.screen = screen
        self.assets = asset_manager
        self.panel_height = 80
        self.tower_types = ["arrow", "cannon", "slow", "sniper"]
        self.tower_costs = {"arrow": 50, "cannon": 100, "slow": 75, "sniper": 150}
        self.selected_tower = "arrow"
        self.font = pygame.font.SysFont('Arial', 16, bold=True)
        self.panel_rect = pygame.Rect(0, 600 - self.panel_height, 800, self.panel_height)

    def render(self, money):
        pygame.draw.rect(self.screen, (40, 40, 40), self.panel_rect)
        pygame.draw.line(self.screen, (80, 80, 80), (0, 600 - self.panel_height), (800, 600 - self.panel_height), 2)

        tower_width = 180
        spacing = 20
        start_x = (800 - (len(self.tower_types) * tower_width + (len(self.tower_types) - 1) * spacing)) // 2
        y = 600 - self.panel_height + 10

        for i, tower_type in enumerate(self.tower_types):
            x = start_x + i * (tower_width + spacing)
            rect = pygame.Rect(x, y, tower_width, 60)
            cost = self.tower_costs[tower_type]
            can_afford = money >= cost
            is_selected = tower_type == self.selected_tower

            if is_selected:
                pygame.draw.rect(self.screen, (100, 150, 255), rect, 3)
                pygame.draw.rect(self.screen, (60, 60, 80), rect)
            else:
                pygame.draw.rect(self.screen, (80, 80, 80), rect)

            sprite = self.assets.towers.get(tower_type)
            if sprite:
                sprite_rect = sprite.get_rect(center=(x + 30, y + 30))
                self.screen.blit(sprite, sprite_rect)

            name_surface = self.font.render(tower_type.capitalize(), True, (255, 255, 255))
            self.screen.blit(name_surface, (x + 60, y + 10))

            cost_color = (255, 215, 0) if can_afford else (255, 50, 50)
            cost_surface = self.font.render(f"{cost}g", True, cost_color)
            self.screen.blit(cost_surface, (x + 60, y + 35))

    def handle_click(self, mouse_pos):
        if not self.panel_rect.collidepoint(mouse_pos):
            return None

        tower_width = 180
        spacing = 20
        start_x = (800 - (len(self.tower_types) * tower_width + (len(self.tower_types) - 1) * spacing)) // 2
        y = 600 - self.panel_height + 10

        for i, tower_type in enumerate(self.tower_types):
            x = start_x + i * (tower_width + spacing)
            rect = pygame.Rect(x, y, tower_width, 60)
            if rect.collidepoint(mouse_pos):
                self.selected_tower = tower_type
                return tower_type

        return None

    def get_selected_tower(self):
        return self.selected_tower