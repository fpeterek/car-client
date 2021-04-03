from typing import Tuple

from geopy import distance


class Path:

    def _to_meters(self) -> Tuple[float, float]:
        begin = self.begin.lat, self.begin.lon
        end1 = self.begin.lat, self.end.lon
        end2 = self.end.lat, self.begin.lon

        mx = distance.distance(begin, end1).m
        my = distance.distance(begin, end2).m

        mx = mx * (1 if self.end.lon > self.begin.lon else -1)
        my = my * (1 if self.end.lat > self.begin.lat else -1)

        return mx, my

    @property
    def reversed(self):
        return Path(begin=self.end, end=self.begin)

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.dist: float = distance.distance(begin.lonlat, end.lonlat).m

        self.m_begin: Tuple[float, float] = (0, 0)
        self.m_end: Tuple[float, float] = self._to_meters()
        self.m_normal: Tuple[float, float] = -self.m_end[1], self.m_end[0]

    def __hash__(self):
        return hash((self.begin, self.end))
