import enum
import pygame

from typing import List, Optional

from pygame.locals import (
    K_1,
    K_2,
    K_3,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_UP, K_w,
    K_DOWN, K_s,
    K_LEFT, K_a,
    K_RIGHT, K_d,
)

from ouroboros.cell import UP, DOWN, LEFT, RIGHT


class Selected(enum.Enum):
    QUIT = 0
    DIFFICULTY_EASY = 1
    DIFFICULTY_MEDIUM = 2
    DIFFICULTY_HARD = 3
    PAUSE = 98
    CONTINUE = 99


def wait_for_selection(incl_continue: bool = True, incl_difficulty: bool = False) -> Selected:
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return Selected.QUIT
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return Selected.QUIT
                if incl_continue and event.key == K_SPACE:
                    return Selected.CONTINUE
                if incl_difficulty:
                    if event.key == K_1:
                        return Selected.DIFFICULTY_EASY
                    if event.key == K_2:
                        return Selected.DIFFICULTY_MEDIUM
                    if event.key == K_3:
                        return Selected.DIFFICULTY_HARD


def check_for_override():
    for event in pygame.event.get():
        if event.type == QUIT:
            return Selected.QUIT
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return Selected.QUIT
            if event.key == K_SPACE:
                return Selected.PAUSE


def decode_input(pressed: List[int]) -> Optional[str]:
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
