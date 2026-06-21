import sys
import pygame
from controllers.game_controller import GameController
from views.asset_manager import AssetManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Bastion Break")
    clock = pygame.time.Clock()

    asset_manager = AssetManager()
    game_controller = GameController(screen, asset_manager)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_controller.handle_input(event)

        game_controller.update(dt)
        game_controller.render()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()