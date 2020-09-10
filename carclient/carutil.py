import math
from typing import Tuple


def calc_angle(begin: Tuple[float, float], end: Tuple[float, float]) -> float:

    x_diff = end[0] - begin[0]
    y_diff = end[1] - begin[1]

    diff = (x_diff ** 2 + y_diff ** 2) ** 0.5

    cos = x_diff / diff

    angle = math.degrees(math.acos(cos))
    angle = 360.0 - angle if end[1] < begin[1] else angle

    return angle
