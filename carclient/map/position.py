from typing import Tuple

from map.vector import Vector
from util.util import find_intersection, add_meters


class Position:
    def __init__(self, lon: float, lat: float):
        self.lon = lon
        self.lat = lat

    @property
    def x(self) -> float:
        return self.lon

    @property
    def y(self) -> float:
        return self.lat

    def __eq__(self, other):
        return self.lon == other.lon and self.lat == other.lat

    @property
    def tuple(self) -> Tuple[float, float]:
        return self.lon, self.lat

    def __hash__(self):
        return hash(self.tuple)

    def __str__(self):
        return f'Position {{lat={self.lat}, lon={self.lon}}}'

    def __repr__(self):
        return str(self)

    def shortest_path(self, vector: Vector):
        begin_vector = Vector(begin=vector.begin, end=self)
        end_vector = Vector(begin=self, end=vector.end)

        x1, y1 = (begin_vector.m_end[0], begin_vector.m_end[1])
        x2, y2 = x1 + vector.m_normal[0], y1 + vector.m_normal[1]
        x3, y3 = vector.m_begin[0], vector.m_begin[1]
        x4, y4 = vector.m_end[0], vector.m_end[1]

        intersect = find_intersection(x1, y1, x2, y2, x3, y3, x4, y4)
        ix, iy = intersect[0], intersect[1]

        x_int_begin = min(vector.m_begin[0], vector.m_end[0])
        x_int_end = max(vector.m_begin[0], vector.m_end[0])
        y_int_begin = min(vector.m_begin[1], vector.m_end[1])
        y_int_end = max(vector.m_begin[1], vector.m_end[1])

        if x_int_begin <= ix <= x_int_end and y_int_begin <= iy <= y_int_end:

            dx, dy = ix - x_int_begin, iy - y_int_begin

            end = add_meters((self.lat, self.lon), (dx, dy))
            end = Position(lat=end[0], lon=end[1])
            return Vector(begin=self, end=end)

        # return min(begin_vector, end_vector, key=lambda vec: vec.dist)

