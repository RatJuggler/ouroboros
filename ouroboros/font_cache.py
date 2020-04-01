from pygame.font import Font


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
