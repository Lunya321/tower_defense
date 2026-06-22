import pygame

class TowerInfoView:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont('Arial', 20, bold=True)
        self.font_info = pygame.font.SysFont('Arial', 16)
        self.font_button = pygame.font.SysFont('Arial', 14)
        self.selected_tower = None
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        self.close_button = pygame.Rect(0, 0, 30, 30)
        self.upgrade_button = pygame.Rect(0, 0, 150, 30)
        self.sell_button = pygame.Rect(0, 0, 150, 30)

    def render(self, tower, money):
        if not tower:
            return

        self.selected_tower = tower
        panel_x = 620
        panel_y = 50
        panel_width = 170
        panel_height = 180

        pygame.draw.rect(self.screen, (40, 40, 60), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, (255, 215, 0), (panel_x, panel_y, panel_width, panel_height), 2)

        title = self.font_title.render(tower.type_name.capitalize(), True, (255, 215, 0))
        self.screen.blit(title, (panel_x + 10, panel_y + 10))

        info_lines = [
            f"Урон: {tower.damage}",
            f"Дальность: {tower.range}",
            f"Скорость: {tower.cooldown:.1f}с",
        ]
        for i, line in enumerate(info_lines):
            text = self.font_info.render(line, True, (255, 255, 255))
            self.screen.blit(text, (panel_x + 10, panel_y + 40 + i * 25))

        upgrade_cost = int(tower.cost * 0.7)
        sell_value = int(tower.cost * 0.5)

        self.close_button = pygame.Rect(panel_x + panel_width - 35, panel_y + 5, 25, 25)
        self.upgrade_button = pygame.Rect(panel_x + 10, panel_y + 120, 150, 25)
        self.sell_button = pygame.Rect(panel_x + 10, panel_y + 150, 150, 25)

        pygame.draw.rect(self.screen, (200, 50, 50), self.close_button, border_radius=4)
        close_text = self.font_button.render("X", True, (255, 255, 255))
        close_rect = close_text.get_rect(center=self.close_button.center)
        self.screen.blit(close_text, close_rect)

        can_upgrade = money >= upgrade_cost
        for button, text_label, cost in [
            (self.upgrade_button, "Улучшить", upgrade_cost),
            (self.sell_button, "Продать", sell_value),
        ]:
            mouse_pos = pygame.mouse.get_pos()
            if button.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (100, 100, 150), button)
            else:
                pygame.draw.rect(self.screen, (60, 60, 80), button)
            
            text_color = (255, 215, 0) if (can_upgrade or button == self.sell_button) else (150, 150, 150)
            button_text = f"{text_label} ({cost}g)"
            text = self.font_button.render(button_text, True, text_color)
            text_rect = text.get_rect(center=button.center)
            self.screen.blit(text, text_rect)

    def handle_click(self, mouse_pos):
        if not self.selected_tower:
            return None

        if self.close_button.collidepoint(mouse_pos):
            self.close()
            return "close"

        if self.upgrade_button.collidepoint(mouse_pos):
            return "upgrade"
        elif self.sell_button.collidepoint(mouse_pos):
            return "sell"
        
        return None

    def close(self):
        self.selected_tower = None