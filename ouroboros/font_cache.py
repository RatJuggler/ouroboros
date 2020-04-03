from pygame.font import Font
from pygame.surface import SurfaceType

TEXT_COLOUR = (255, 255, 255)


class FontCache:

    def __init__(self) -> None:
        self._fonts = {}

    def _cache_font(self, size: int):
        font = Font('rainyhearts.ttf', size)
        self._fonts[str(size)] = font
        return font

    def get_font(self, size: int) -> Font:
        font = self._fonts.get(str(size))
        if font is None:
            font = self._cache_font(size)
        return font

    def render_text(self, text: str, size: int) -> SurfaceType:
        font = self.get_font(size)
        return font.render(text, True, TEXT_COLOUR)
