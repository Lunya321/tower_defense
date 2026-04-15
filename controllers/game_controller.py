from models.map_model import MapModel
from views.map_renderer import MapRenderer

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.map_model = MapModel()
        self.map_renderer = MapRenderer(self.map_model)

    def handle_input(self, event):
        pass

    def update(self, dt):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))
        self.map_renderer.render(self.screen)