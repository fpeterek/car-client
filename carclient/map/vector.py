from typing import Tuple

from geopy import distance


class Vector:

    def _to_meters(self) -> Tuple[float, float]:
        begin = self.begin.lat, self.begin.lon
        end1 = self.begin.lat, self.end.lon
        end2 = self.end.lat, self.begin.lon

        mx = distance.distance(begin, end1).m
        my = distance.distance(begin, end2).m

        mx = mx * (1 if self.end.lon > self.begin.lon else -1)
        my = my * (1 if self.end.lat > self.begin.lat else -1)

        return mx, my

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.dist = distance.distance(begin.tuple, end.tuple).m

        self.m_begin = (0, 0)
        self.m_end = self._to_meters()
        self.m_normal = -self.m_end[1], self.m_end[0]
