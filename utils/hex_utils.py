import math
from utils.settings import SCREEN_HEIGHT, SCREEN_WIDTH

HEX_SIZE = 30  

HEX_DIRECTIONS = [
    (1, 0, -1),
    (1, -1, 0),
    (0, -1, 1),
    (-1, 0, 1),
    (-1, 1, 0),
    (0, 1, -1),
]


def hex_to_pixel(q, r, s):
    x = (q - r) * HEX_SIZE * math.sqrt(3) / 2 + SCREEN_WIDTH / 2
    y = (
        q + r
    ) * HEX_SIZE / 2 * 0.866 + SCREEN_HEIGHT / 4 
    return x, y


def pixel_to_hex(x, y):
    x = x - SCREEN_WIDTH / 2
    y = y - SCREEN_HEIGHT / 4

    q = (x * (2 / (HEX_SIZE * math.sqrt(3))) + y * (2 / (HEX_SIZE * 0.866))) / 2
    r = (y * (2 / (HEX_SIZE * 0.866)) - x * (2 / (HEX_SIZE * math.sqrt(3)))) / 2
    s = -q - r
    return hex_round(q, r, s)


def hex_round(q, r, s):
    q_int = round(q)
    r_int = round(r)
    s_int = round(s)

    q_diff = abs(q_int - q)
    r_diff = abs(r_int - r)
    s_diff = abs(s_int - s)

    if q_diff > r_diff and q_diff > s_diff:
        q_int = -r_int - s_int
    elif r_diff > s_diff:
        r_int = -q_int - s_int
    else:
        s_int = -q_int - r_int

    return int(q_int), int(r_int), int(s_int)
