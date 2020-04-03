import pathlib

from typing import Tuple

Point = Tuple[int, int]


def full_file_path(filename: str) -> str:
    return str(pathlib.Path(__file__).parent / filename)
