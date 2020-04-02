import enum

import click
import pygame

from pygame.locals import (
    K_1,
    K_2,
    K_3,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from ouroboros.direction import decode_input
from ouroboros.display import Display
from ouroboros.food import Food
from ouroboros.snake import Snake
from ouroboros.sprite_images import SpriteImages


class MenuKey(enum.Enum):
    QUIT = 0
    DIFFICULTY_EASY = 1
    DIFFICULTY_MEDIUM = 2
    DIFFICULTY_HARD = 3
    CONTINUE = 99


class Game:
    """
    The overall controlling class.
    """

    def __init__(self, windowed: bool) -> None:
        """
        Initialise the display controller and sprite image cache.
        :param windowed: display in a window rather than full-screen
        """
        self._display = Display(windowed)
        self._images = SpriteImages.load_images(self._display)

    @classmethod
    def _wait(cls) -> MenuKey:
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return MenuKey.QUIT
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return MenuKey.QUIT
                    if event.key == K_SPACE:
                        return MenuKey.CONTINUE

    def _attract(self) -> MenuKey:
        """
        Show the attract/title screen and wait for the start key.
        :return: MenuKey selected to start or exit the game
        """
        self._display.draw_background()
        self._display.show_text('O U R O B O R O S', 96, 0.5, 0.5)
        self._display.show_text('Hit SPACE to start', 32, 0.5, 0.75)
        self._display.show_text('ESC to quit', 24, 0.5, 0.80)
        return self._wait()

    def _difficulty(self) -> MenuKey:
        """
        Show the difficulty levels and wait for a selection.
        :return: the difficulty level
        """
        self._display.draw_background()
        self._display.show_text('Select difficulty level', 32, 0.5, 0.15)
        self._display.show_text('(1) Easy - More food, grid lines', 32, 0.5, 0.30)
        self._display.show_text('(2) Medium - Less food, grid lines', 32, 0.5, 0.40)
        self._display.show_text('(3) Hard - Even less food, no grid lines', 32, 0.5, 0.50)
        self._display.show_text('Use WASD or the arrow keys to control the snake.', 32, 0.5, 0.70)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return MenuKey.QUIT
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return MenuKey.QUIT
                    if event.key == K_1:
                        return MenuKey.DIFFICULTY_EASY
                    if event.key == K_2:
                        return MenuKey.DIFFICULTY_MEDIUM
                    if event.key == K_3:
                        return MenuKey.DIFFICULTY_HARD

    def _play(self, difficulty: MenuKey) -> None:
        """
        Play the game.
        :param difficulty: level to play the game
        :return: no meaningful return
        """
        snake = Snake.new_snake(self._display, self._images)
        if difficulty == MenuKey.DIFFICULTY_EASY:
            food_level = 9
        elif difficulty == MenuKey.DIFFICULTY_MEDIUM:
            food_level = 6
        else:
            food_level = 3
        food = Food(self._display, self._images, food_level)
        food.add_food(snake)
        score = 0
        pause = False
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    if event.key == K_SPACE:
                        pause = not pause
            if not pause:
                new_direction = decode_input(pygame.key.get_pressed())
                if not snake.move_head(new_direction):
                    return
                if food.eaten_by(snake):
                    score += 1
                else:
                    snake.move_body()
            self._display.draw_background(difficulty != MenuKey.DIFFICULTY_HARD, score)
            snake.render()
            food.render()
            if pause:
                self._display.show_text('P a u s e d', 64, 0.5, 0.5)
            pygame.display.flip()
            clock.tick(10)

    def _over(self) -> MenuKey:
        """
        Show the game over screen and wait for the key to restart.
        :return: MenuKey to continue or exit the game
        """
        self._display.show_text('G a m e  O v e r', 64, 0.5, 0.5)
        self._display.show_text('Hit SPACE to restart', 32, 0.5, 0.75)
        self._display.show_text('ESC to quit', 16, 0.5, 0.80)
        return self._wait()

    def run(self) -> None:
        """
        Entry point, show screens and play game.
        :return: No meaningful return
        """
        while True:
            if self._attract() == MenuKey.QUIT:
                break
            difficulty = self._difficulty()
            if difficulty == MenuKey.QUIT:
                break
            self._play(difficulty)
            if self._over() == MenuKey.QUIT:
                break


@click.command(help="""
    Ouroborus - A snake game.
                    """)
@click.version_option()
@click.option('-w', '--windowed', 'windowed', default=False, is_flag=True,
              help="Run in a window rather than full-screen.",
              show_default=True)
def main(windowed: bool) -> None:
    pygame.init()
    Game(windowed).run()
    pygame.quit()


if __name__ == '__main__':
    main()
