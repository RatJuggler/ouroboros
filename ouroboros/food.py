import pygame

from ouroboros.cell import Cell
from ouroboros.input import FIXED, Selected
from ouroboros.display import Display
from ouroboros.snake import Snake
from ouroboros.sprite_images import SpriteImages


class FoodItem(Cell):

    def __init__(self, display: Display, images: SpriteImages, edge_buffer: int) -> None:
        super(FoodItem, self).__init__(display, images, display.get_random_position(edge_buffer), FIXED)


class Food:

    def __init__(self, display: Display, images: SpriteImages, snake: Snake, difficulty: Selected) -> None:
        self._display = display
        self._images = images
        self._snake = snake
        self._edge_buffer = 0
        if difficulty == Selected.DIFFICULTY_EASY:
            self._food_level = 9
            self._edge_buffer = 1
        elif difficulty == Selected.DIFFICULTY_MEDIUM:
            self._food_level = 6
        else:
            self._food_level = 3
        self._food = []

    def add_food(self) -> None:
        while len(self._food) < self._food_level:
            while True:
                food_item = FoodItem(self._display, self._images, self._edge_buffer)
                if not pygame.sprite.spritecollideany(food_item, self._food) and not self._snake.is_on(food_item):
                    break
            self._food.append(food_item)

    def eaten(self) -> bool:
        eaten = self._snake.eats(self._food)
        if eaten:
            self._food.remove(eaten)
            self.add_food()
        return eaten is not None

    def render(self) -> None:
        for food_item in self._food:
            food_item.render()
