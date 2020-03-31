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

    def __init__(self) -> None:
        self._display = Display()
        self._images = SpriteImages.load_images(self._display)
        self._clock = pygame.time.Clock()

    def place_food(self, snake: Snake) -> Food:
        while True:
            food = Food(self._display, self._images)
            if not snake.is_on_food(food):
                break
        return food

    def play(self) -> None:
        snake = Snake.new_snake(self._display, self._images)
        food = self.place_food(snake)
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
                if snake.eats_food(food):
                    score += 1
                    food.kill()
                    snake.grow()
                    food = self.place_food(snake)
                else:
                    snake.move_body()
            self._display.draw_background()
            self._display.show_score(score)
            snake.render()
            food.render()
            if pause:
                self._display.show_paused()
            pygame.display.flip()
            self._clock.tick(10)


if __name__ == '__main__':
    pygame.init()
    Game().play()
    pygame.quit()
