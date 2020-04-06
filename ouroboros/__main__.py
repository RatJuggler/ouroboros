import click
import pygame

from ouroboros.input import decode_input, Selected, check_for_selection, check_for_override
from ouroboros.display import Display
from ouroboros.food import Food
from ouroboros.snake import Snake
from ouroboros.sounds import Sounds
from ouroboros.sprite_images import SpriteImages

LOW_GREEN = pygame.Color('GREENYELLOW')
HIGH_GREEN = pygame.Color('SPRINGGREEN')


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
        self._sounds = Sounds.load_sounds()

    def _attract(self) -> Selected:
        """
        Show the attract/title screen and wait for the start key.
        :return: MenuKey selected to start or exit the game
        """
        selection = None
        title_swap = True
        clock = pygame.time.Clock()
        while selection is None:
            self._display.draw_background()
            self._display.show_text('O   R   B   R   S', 96, 0.5,
                                    0.4 if title_swap else 0.5,
                                    HIGH_GREEN if title_swap else LOW_GREEN)
            self._display.show_text('  U   O   O   O  ', 96, 0.5,
                                    0.5 if title_swap else 0.4,
                                    LOW_GREEN if title_swap else HIGH_GREEN)
            title_swap = not title_swap
            self._display.show_text('Hit SPACE to start', 32, 0.5, 0.75, pygame.Color('GOLD'))
            self._display.show_text('ESC to quit', 24, 0.5, 0.80, pygame.Color('GOLD'))
            pygame.display.flip()
            clock.tick(3)
            selection = check_for_selection(False)
        return selection

    def _difficulty(self) -> Selected:
        """
        Show the difficulty levels and wait for a selection.
        :return: the difficulty level
        """
        self._display.draw_background()
        self._display.show_text('Select difficulty level', 32, 0.5, 0.15, HIGH_GREEN)
        self._display.show_text('(1) Easy - More food, grid lines', 32, 0.5, 0.30, pygame.Color('GOLD'))
        self._display.show_text('(2) Medium - Less food, grid lines', 32, 0.5, 0.40, pygame.Color('GREEN'))
        self._display.show_text('(3) Hard - Even less food, no grid lines', 32, 0.5, 0.50, pygame.Color('SALMON'))
        self._display.show_text('Use WASD or the arrow keys to control the snake.', 32, 0.5, 0.70, LOW_GREEN)
        pygame.display.flip()
        return check_for_selection(True, False, True)

    def _play(self, difficulty: Selected) -> None:
        """
        Play the game.
        :param difficulty: level to play the game
        :return: no meaningful return
        """
        snake = Snake.new_snake(self._display, self._images, self._sounds)
        food = Food(self._display, self._images, self._sounds, snake, difficulty)
        food.add_food()
        score = 0
        pause = False
        clock = pygame.time.Clock()
        while True:
            override = check_for_override()
            if override == Selected.QUIT:
                return
            if override == Selected.PAUSE:
                pause = not pause
            if not pause:
                new_direction = decode_input(pygame.key.get_pressed())
                if not snake.move_head(new_direction):
                    return
                if food.eaten():
                    score += 1
                else:
                    snake.move_body()
            self._display.draw_background(difficulty != Selected.DIFFICULTY_HARD, score)
            snake.render()
            food.render()
            if pause:
                self._display.show_text('P a u s e d', 64, 0.5, 0.5)
            pygame.display.flip()
            clock.tick(10)

    def _over(self) -> Selected:
        """
        Show the game over screen and wait for the key to restart.
        :return: MenuKey to continue or exit the game
        """
        selection = None
        title_swap = True
        clock = pygame.time.Clock()
        while selection is None:
            self._display.show_text('G a m e  O v e r', 64, 0.5, 0.5, HIGH_GREEN if title_swap else LOW_GREEN)
            title_swap = not title_swap
            self._display.show_text('Hit SPACE to restart', 32, 0.5, 0.75, pygame.Color('GOLD'))
            self._display.show_text('ESC to quit', 16, 0.5, 0.80, pygame.Color('GOLD'))
            pygame.display.flip()
            clock.tick(3)
            selection = check_for_selection(False)
        return selection

    def run(self) -> None:
        """
        Entry point, show screens and play game.
        :return: No meaningful return
        """
        while True:
            if self._attract() == Selected.QUIT:
                break
            difficulty = self._difficulty()
            if difficulty == Selected.QUIT:
                break
            self._play(difficulty)
            if self._over() == Selected.QUIT:
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
