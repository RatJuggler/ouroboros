import pathlib


def full_file_path(filename: str) -> str:
    return str(pathlib.Path(__file__).parent / filename)
