from typing import Tuple, Optional

from pygame.locals import (
    K_UP, K_w,
    K_DOWN, K_s,
    K_LEFT, K_a,
    K_RIGHT, K_d,
)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def decode_input(pressed: Tuple[int]) -> Optional[str]:
    new_direction = None
    if pressed[K_UP] or pressed[K_w]:
        new_direction = UP
    if pressed[K_DOWN] or pressed[K_s]:
        new_direction = DOWN
    if pressed[K_LEFT] or pressed[K_a]:
        new_direction = LEFT
    if pressed[K_RIGHT] or pressed[K_d]:
        new_direction = RIGHT
    return new_direction


def move_in(direction: str) -> Tuple[int, int]:
    if direction == UP:
        return 0, -1
    elif direction == DOWN:
        return 0, 1
    elif direction == LEFT:
        return -1, 0
    elif direction == RIGHT:
        return 1, 0
