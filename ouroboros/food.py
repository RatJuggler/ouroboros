from ouroboros.cell import Cell
from ouroboros.display import Display


class Food(Cell):

    def __init__(self, display: Display) -> None:
        super(Food, self).__init__(display,
                                   display.get_random_column(),
                                   display.get_random_row(),
                                   None,
                                   (255, 32, 0))
