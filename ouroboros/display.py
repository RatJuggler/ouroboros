import pygame
import random

from typing import Tuple

from ouroboros.font_cache import FontCache

BACKGROUND_COLOUR = (64, 64, 64)
GRID_COLOUR = (128, 128, 128)
TEXT_COLOUR = (255, 255, 255)


class Display:

    def __init__(self, windowed: bool) -> None:
        self.CELL_SIZE = 32
        self.CELL_COLUMNS = 16 * 2
        self.CELL_ROWS = 9 * 2
        self.DISPLAY_WIDTH = self.CELL_COLUMNS * self.CELL_SIZE
        self.DISPLAY_HEIGHT = self.CELL_ROWS * self.CELL_SIZE
        assert self.DISPLAY_WIDTH % self.CELL_SIZE == 0, "Display width must be a multiple of the cell size."
        assert self.DISPLAY_HEIGHT % self.CELL_SIZE == 0, "Display height must be a multiple of the cell size."
        if windowed:
            flags = 0
        else:
            flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        self._screen = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT), flags)
        pygame.display.set_caption('Ouroboros')
        self._font_cache = FontCache()

    def show_text(self, text: str, size: int, x_prop: float, y_prop: float) -> None:
        font = self._font_cache.get_font(size)
        text_img = font.render(text, True, TEXT_COLOUR)
        rect = text_img.get_rect()
        self.blit(text_img, (self.DISPLAY_WIDTH * x_prop - rect.width // 2, self.DISPLAY_HEIGHT * y_prop - rect.height // 2))

    def create_surface(self, image_sheet: pygame.Surface, image_start: Tuple[int, int]) -> pygame.Surface:
        surface = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE), pygame.SRCALPHA)
        surface.blit(image_sheet, (0, 0), (image_start[0], image_start[1], self.CELL_SIZE, self.CELL_SIZE))
        return surface

    def get_rect(self, at_cell: Tuple[int, int]) -> pygame.Rect:
        return pygame.Rect(at_cell[0] * self.CELL_SIZE, at_cell[1] * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)

    def blit(self, image: pygame.Surface, rect: pygame.rect) -> None:
        self._screen.blit(image, rect)

    def move_ip(self, rect: pygame.rect, delta_x: int, delta_y: int) -> None:
        rect.move_ip(delta_x * self.CELL_SIZE, delta_y * self.CELL_SIZE)

    def valid_position(self, position: Tuple[int, int]) -> bool:
        return 0 <= position[0] < self.CELL_COLUMNS and 1 <= position[1] < self.CELL_ROWS

    def get_random_position(self, edge_buffer: int) -> Tuple[int, int]:
        return random.randint(edge_buffer, self.CELL_COLUMNS - edge_buffer - 1), \
               random.randint(edge_buffer + 1, self.CELL_ROWS - edge_buffer - 1)

    def get_center(self) -> Tuple[int, int]:
        return (self.CELL_COLUMNS - 1) // 2, self.CELL_ROWS // 2

    def draw_background(self, draw_grid: bool = True, score: int = 0) -> None:
        self._screen.fill(BACKGROUND_COLOUR)
        if draw_grid:
            for grid_row in range(self.CELL_SIZE, self.DISPLAY_HEIGHT, self.CELL_SIZE):
                pygame.draw.line(self._screen, GRID_COLOUR, (0, grid_row), (self.DISPLAY_WIDTH, grid_row))
            for grid_column in range(0, self.DISPLAY_WIDTH, self.CELL_SIZE):
                pygame.draw.line(self._screen, GRID_COLOUR, (grid_column, self.CELL_SIZE), (grid_column, self.DISPLAY_HEIGHT))
        font = self._font_cache.get_font(32)
        score_img = font.render('{0:04d}'.format(score), True, TEXT_COLOUR)
        self.blit(score_img, ((self.CELL_COLUMNS - 2) * self.CELL_SIZE, 2))
