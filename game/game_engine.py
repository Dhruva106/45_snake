import pygame
import math
import array

from .snake import Snake
from .food import Food


WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)


def create_beep(frequency, duration, volume=0.4):
    """
    Creates a short sound effect in memory.
    No external sound files are required.
    """

    mixer_info = pygame.mixer.get_init()

    if mixer_info is None:
        return None

    sample_rate, sample_format, channels = mixer_info

    # This game uses the normal 16-bit mixer format.
    if abs(sample_format) != 16:
        return None

    samples = int(sample_rate * duration)

    buffer = array.array("h")

    for i in range(samples):
        value = int(
            32767
            * volume
            * math.sin(
                2 * math.pi * frequency * i / sample_rate
            )
        )

        for _ in range(channels):
            buffer.append(value)

    try:
        return pygame.mixer.Sound(buffer=buffer)
    except pygame.error:
        return None


class GameEngine:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.cell_size = 20

        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.snake = Snake(
            self.grid_width // 2,
            self.grid_height // 2,
            self.cell_size
        )

        self.food = Food(
            self.grid_width,
            self.grid_height,
            self.cell_size
        )

        self.score = 0

        self.font = pygame.font.SysFont(
            "Arial",
            30
        )

        self.moves_per_second = 8

        self._frame_counter = 0

        self.game_over = False

        self._game_over_logged = False

        # -----------------------------
        # Task 4: Sound Effects
        # -----------------------------

        self.eat_sound = create_beep(
            800,
            0.08,
            0.4
        )

        self.game_over_sound = create_beep(
            200,
            0.4,
            0.5
        )

        self._game_over_sound_played = False

    def handle_keydown(self, key):

        if key in (pygame.K_UP, pygame.K_w):

            self.snake.set_direction(
                0,
                -1
            )

        elif key in (pygame.K_DOWN, pygame.K_s):

            self.snake.set_direction(
                0,
                1
            )

        elif key in (pygame.K_LEFT, pygame.K_a):

            self.snake.set_direction(
                -1,
                0
            )

        elif key in (pygame.K_RIGHT, pygame.K_d):

            self.snake.set_direction(
                1,
                0
            )

    def handle_input(self):

        # Reserved for continuous input.
        pass

    def update(self):

        if self.game_over:
            return

        self._frame_counter += 1

        frames_per_move = max(
            1,
            60 // self.moves_per_second
        )

        if self._frame_counter < frames_per_move:
            return

        self._frame_counter = 0

        # Move snake
        self.snake.move()

        # -----------------------------
        # Wall Collision
        # -----------------------------

        if self.snake.collides_with_wall(
            self.grid_width,
            self.grid_height
        ):

            self.game_over = True

            if (
                self.game_over_sound
                and not self._game_over_sound_played
            ):
                self.game_over_sound.play()
                self._game_over_sound_played = True

            return

        # -----------------------------
        # Self Collision
        # -----------------------------

        if self.snake.collides_with_self():

            self.game_over = True

            if (
                self.game_over_sound
                and not self._game_over_sound_played
            ):
                self.game_over_sound.play()
                self._game_over_sound_played = True

            return

        # -----------------------------
        # Food Collision
        # -----------------------------

        if self.snake.head_rect().colliderect(
            self.food.rect()
        ):

            self.snake.grow()

            self.score += 1

            # Play eating sound
            if self.eat_sound:
                self.eat_sound.play()

            # Respawn food
            self.food.respawn(
                self.snake.body
            )

    def render(self, screen):

        # -----------------------------
        # Draw Food
        # -----------------------------

        pygame.draw.rect(
            screen,
            RED,
            self.food.rect()
        )

        # -----------------------------
        # Draw Snake
        # -----------------------------

        for rect in self.snake.segment_rects():

            pygame.draw.rect(
                screen,
                GREEN,
                rect
            )

        # -----------------------------
        # Draw Score
        # -----------------------------

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (10, 10)
        )

        # -----------------------------
        # Task 2: Game Over Screen
        # -----------------------------

        if self.game_over:

            overlay = pygame.Surface(
                (self.width, self.height)
            )

            overlay.set_alpha(180)

            overlay.fill(
                (0, 0, 0)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            game_over_text = self.font.render(
                "GAME OVER",
                True,
                WHITE
            )

            score_text = self.font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            continue_text = self.font.render(
                "Choose a difficulty to play again",
                True,
                WHITE
            )

            screen.blit(
                game_over_text,
                game_over_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 80
                    )
                )
            )

            screen.blit(
                score_text,
                score_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 30
                    )
                )
            )

            screen.blit(
                continue_text,
                continue_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 20
                    )
                )
            )