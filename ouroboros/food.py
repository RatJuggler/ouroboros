from ouroboros.cell import Cell
from ouroboros.direction import FIXED
from ouroboros.display import Display
from ouroboros.snake import Snake
from ouroboros.sprite_images import SpriteImages


class FoodItem(Cell):

    def __init__(self, display: Display, images: SpriteImages) -> None:
        super(FoodItem, self).__init__(display, images, display.get_random_position(), FIXED)


class Food:

    def __init__(self, display: Display, images: SpriteImages) -> None:
        self._display = display
        self._images = images
        self._food = None

    def add_food(self, snake: Snake) -> None:
        if self._food:
            self._food.kill()
        while True:
            self._food = FoodItem(self._display, self._images)
            if not snake.is_on(self._food):
                break

    def eaten_by(self, snake: Snake) -> bool:
        return snake.eats(self._food)

    def render(self) -> None:
        self._food.render()
