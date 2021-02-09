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
