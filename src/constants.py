from enum import Enum

class COLOR:
    LIGHT_BLUE = (56, 212, 218)
    LIGHT_GREY = (200, 200, 200)
    BLACK  = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GREEN = (0, 100, 0)
    RED = (255, 0, 0)

class TILE:
    EMPTY = 0
    FRUIT = -1
    WALL = -2


def tile_to_color(tile: int) -> tuple:
    if tile == TILE.EMPTY:
        return COLOR.WHITE
    elif tile == TILE.WALL:
        return COLOR.BLACK
    elif tile == TILE.FRUIT:
        return COLOR.RED
    elif is_snake(tile):
        return COLOR.DARK_GREEN
    else:
        raise ValueError(f"invalid tile value: {tile}")

def is_snake(tile: int) -> bool:
    return tile > 0