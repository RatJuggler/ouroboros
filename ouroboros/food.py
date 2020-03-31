from ouroboros.cell import Cell
from ouroboros.direction import FIXED
from ouroboros.display import Display
from ouroboros.sprite_images import SpriteImages


class Food(Cell):

    def __init__(self, display: Display, images: SpriteImages) -> None:
        super(Food, self).__init__(display,
                                   images,
                                   display.get_random_position(),
                                   FIXED)
