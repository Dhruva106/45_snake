import pygame

from game.game_engine import GameEngine


pygame.init()

WIDTH = 600
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 220, 0)
RED = (220, 60, 60)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Pygame Version")

clock = pygame.time.Clock()

engine = GameEngine(WIDTH, HEIGHT)


def draw_game_over_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill(BLACK)
    SCREEN.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont("Arial", 42, bold=True)
    font = pygame.font.SysFont("Arial", 28)

    title = title_font.render("GAME OVER", True, RED)
    score = font.render(
        f"Final Score: {engine.score}",
        True,
        WHITE
    )

    easy = font.render(
        "1 - Easy",
        True,
        GREEN
    )

    medium = font.render(
        "2 - Medium",
        True,
        YELLOW
    )

    hard = font.render(
        "3 - Hard",
        True,
        RED
    )

    exit_text = font.render(
        "Q - Exit",
        True,
        WHITE
    )

    SCREEN.blit(
        title,
        title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 130))
    )

    SCREEN.blit(
        score,
        score.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 75))
    )

    SCREEN.blit(
        easy,
        easy.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 15))
    )

    SCREEN.blit(
        medium,
        medium.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    )

    SCREEN.blit(
        hard,
        hard.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 75))
    )

    SCREEN.blit(
        exit_text,
        exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))
    )


def main():
    global engine

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
                    if event.key == pygame.K_1:
                        engine = GameEngine(WIDTH, HEIGHT)
                        engine.moves_per_second = 5

                    elif event.key == pygame.K_2:
                        engine = GameEngine(WIDTH, HEIGHT)
                        engine.moves_per_second = 8

                    elif event.key == pygame.K_3:
                        engine = GameEngine(WIDTH, HEIGHT)
                        engine.moves_per_second = 12

                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False

        if not engine.game_over:
            engine.handle_input()
            engine.update()

        engine.render(SCREEN)

        if engine.game_over:
            draw_game_over_menu()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()