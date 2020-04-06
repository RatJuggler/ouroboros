import pygame

from ouroboros.utils import full_file_path

DEFAULT_TEXT_COLOUR = pygame.Color('WHITE')


class FontCache:

    def __init__(self) -> None:
        self._fonts = {}

    def _cache_font(self, size: int):
        font = pygame.font.Font(full_file_path('rainyhearts.ttf'), size)
        self._fonts[str(size)] = font
        return font

    def get_font(self, size: int) -> pygame.font.Font:
        font = self._fonts.get(str(size))
        if font is None:
            font = self._cache_font(size)
        return font

    def render_text(self, text: str, size: int, colour: pygame.Color = DEFAULT_TEXT_COLOUR) -> pygame.SurfaceType:
        font = self.get_font(size)
        return font.render(text, True, colour)
