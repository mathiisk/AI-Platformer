import numpy as np


def get_level(number: int, tile_size: int) -> tuple[np.ndarray, int, int]:
    """
    A level in text file looks like (1 = walls, 2 = spikes, 9 = goal):
     11111111100000000
     00000000000000000
     00000000000000000
     00000000002000000
     00000001111110000
     11110000000000000
     00000000000000000
     00000000000000000
     00020000020000090
     11111111111100111
    """

    with open (f"../levels_layout/level{number}.txt", "r") as f:
        lines = f.read().splitlines()
    # Convert to numpy array
    level = np.array([list(map(int, list(i))) for i in lines])
    # return level, along with screen width and height only if tile_size is greater than 0
    if tile_size > 0:
        return level, level.shape[1]*tile_size, level.shape[0]*tile_size
    else:
        raise ValueError(tile_size)


