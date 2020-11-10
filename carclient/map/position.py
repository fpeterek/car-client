from typing import Tuple


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
