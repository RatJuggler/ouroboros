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


class Game:

    def __init__(self) -> None:
        self._display = Display()
        self._clock = pygame.time.Clock()

    def play(self) -> None:
        snake = Snake.new_snake(self._display)
        food = Food(self._display)
        score = 0
        pause = False
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
                if snake.found(food):
                    score += 1
                    food.kill()
                    snake.grow()
                    food = Food(self._display)
                else:
                    snake.move_body()
            self._display.draw_background()
            self._display.show_score(score)
            snake.render()
            food.render()
            if pause:
                self._display.show_paused()
            pygame.display.flip()
            self._clock.tick(15)


if __name__ == '__main__':
    pygame.init()
    Game().play()
    pygame.quit()
