from enum import Enum

class COLOR:
    BLUE = (8,115,229)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    DARKER_GREEN = (74,117,45)
    DARK_GREEN = (87,138,53)
    MEDIUM_GREEN = (162,208,74)
    LIGHT_GREEN = (171,214,83)

    BLUE_ONE = (10, 126, 246)
    BLUE_LAST = (8, 38, 69)

class TILE:
    EMPTY = 0
    FRUIT = -1
    WALL = -2

class DIRECTION(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

dark = True

def flip_background_color():
    global dark
    dark = not dark

def tile_to_color(tile: int) -> tuple:
    if tile == TILE.EMPTY: 
        return COLOR.MEDIUM_GREEN if dark else COLOR.LIGHT_GREEN
    elif tile == TILE.WALL:
        return COLOR.DARK_GREEN
    elif tile == TILE.FRUIT:
        return COLOR.RED
    elif is_snake(tile):
        return COLOR.BLUE
    else:
        raise ValueError(f"invalid tile value: {tile}")

def is_snake(tile: int) -> bool:
    return tile > 0