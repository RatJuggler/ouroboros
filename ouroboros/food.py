import pygame

from ouroboros.cell import Cell
from ouroboros.direction import FIXED
from ouroboros.display import Display
from ouroboros.snake import Snake
from ouroboros.sprite_images import SpriteImages


class FoodItem(Cell):

    def __init__(self, display: Display, images: SpriteImages) -> None:
        super(FoodItem, self).__init__(display, images, display.get_random_position(), FIXED)


class Food:

    def __init__(self, display: Display, images: SpriteImages, food_items: int) -> None:
        self._display = display
        self._images = images
        self._food_items = food_items
        self._food = []

    def add_food(self, snake: Snake) -> None:
        while len(self._food) < self._food_items:
            while True:
                food_item = FoodItem(self._display, self._images)
                if not pygame.sprite.spritecollideany(food_item, self._food) and not snake.is_on(food_item):
                    break
            self._food.append(food_item)

    def eaten_by(self, snake: Snake) -> bool:
        eaten = snake.eats(self._food)
        if eaten:
            self._food.remove(eaten)
            self.add_food(snake)
        return eaten is not None

    def render(self) -> None:
        for food_item in self._food:
            food_item.render()
