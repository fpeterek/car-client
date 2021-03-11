from typing import Tuple
import math


# https://en.wikipedia.org/wiki/Line-line_intersection
def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4) -> Tuple[float, float]:
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

    return px, py


def add_meters(latlon_pair, delta_meters) -> Tuple[float, float]:
    dy = delta_meters[1]
    dx = delta_meters[0]
    lat = latlon_pair[0]
    lon = latlon_pair[1]
    y = lat + dy / 6_378_000 * 180 / math.pi
    x = lon + (dx / 6_378_000 * 180 / math.pi) / math.cos(math.radians(lat))
    return y, x


def calc_angle(begin: Tuple[float, float], end: Tuple[float, float]) -> float:

    x_diff = end[0] - begin[0]
    y_diff = end[1] - begin[1]

    diff = (x_diff ** 2 + y_diff ** 2) ** 0.5

    cos = x_diff / diff

    angle = math.degrees(math.acos(cos))
    angle = 360.0 - angle if end[1] < begin[1] else angle

    return angle
