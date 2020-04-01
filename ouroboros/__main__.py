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

    def __init__(self) -> None:
        """
        Initialise the display controller and sprite image cache.
        """
        self._display = Display()
        self._images = SpriteImages.load_images(self._display)

    def wait_on_attract(self) -> bool:
        self._display.draw_background(0)
        self._display.show_text('O U R O B O R O S', 96, 0.5, 0.5)
        self._display.show_text('Hit SPACE to start', 32, 0.5, 0.75)
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

    def _place_food(self, snake: Snake) -> Food:
        """
        Ensure new food isn't placed on the snake.
        :param snake: current snake
        :return: the new food
        """
        while True:
            food = Food(self._display, self._images)
            if not snake.is_on_food(food):
                break
        return food

    def play(self) -> None:
        """
        Play the game.
        :return: no meaningful return
        """
        snake = Snake.new_snake(self._display, self._images)
        food = self._place_food(snake)
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
                if snake.eats_food(food):
                    score += 1
                    food.kill()
                    snake.grow()
                    food = self._place_food(snake)
                else:
                    snake.move_body()
            self._display.draw_background(score)
            snake.render()
            food.render()
            if pause:
                self._display.show_text('P a u s e d', 64, 0.5, 0.5)
            pygame.display.flip()
            clock.tick(10)


if __name__ == '__main__':
    pygame.init()
    game = Game()
    if game.wait_on_attract():
        game.play()
    pygame.quit()
