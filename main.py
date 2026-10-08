import pygame

from game.game_engine import GameEngine


pygame.init()

WIDTH = 600
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Pygame Version")

clock = pygame.time.Clock()

engine = GameEngine(WIDTH, HEIGHT)


def main():
    running = True

    while running:
        SCREEN.fill(BLACK)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if not engine.game_over:
                    engine.handle_keydown(event.key)
                else:
                    running = False

        # Only update the game while it is still running
        if not engine.game_over:
            engine.handle_input()
            engine.update()

        # Always render, including the Game Over screen
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()