import click
import pygame

from pygame.locals import (
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


class Game:
    """
    The overall controlling class.
    """

    def __init__(self, windowed: bool) -> None:
        """
        Initialise the display controller and sprite image cache.
        @param windowed: display in a window rather than full-screen
        """
        self._display = Display(windowed)
        self._images = SpriteImages.load_images(self._display)

    @classmethod
    def _wait(cls) -> bool:
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return False
                    if event.key == K_SPACE:
                        return True

    def _attract(self) -> bool:
        """
        Show the attract/title screen and wait for the start key.
        :return: True start game otherwise exit
        """
        self._display.draw_background(0)
        self._display.show_text('O U R O B O R O S', 96, 0.5, 0.5)
        self._display.show_text('Hit SPACE to start', 32, 0.5, 0.75)
        self._display.show_text('ESC to quit', 24, 0.5, 0.80)
        return self._wait()

    def _play(self) -> None:
        """
        Play the game.
        :return: no meaningful return
        """
        snake = Snake.new_snake(self._display, self._images)
        food = Food(self._display, self._images)
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
                    food.add_food(snake)
                else:
                    snake.move_body()
            self._display.draw_background(score)
            snake.render()
            food.render()
            if pause:
                self._display.show_text('P a u s e d', 64, 0.5, 0.5)
            pygame.display.flip()
            clock.tick(10)

    def _over(self) -> bool:
        """
        Show the game over screen and wait for the key to restart.
        :return: True continue otherwise exit
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
        new_game = self._attract()
        while new_game:
            self._play()
            new_game = self._over()


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
