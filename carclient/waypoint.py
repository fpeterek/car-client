import json

import geopy.distance

from typing import Tuple


class Waypoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # self.radius = 10
        # self.tolerance = 0.00002
        self.tolerance = 2

    def point_inside(self, point: Tuple[float, float]) -> bool:

        dist = geopy.distance.distance(self.position, point).m

        # sx = self.x - point[0]
        # sy = self.y - point[1]
        # dist = (sx**2 + sy**2) ** 0.5
        return dist <= self.tolerance

    @property
    def position(self) -> Tuple[float, float]:
        return self.x, self.y

    @property
    def json(self):
        return json.dumps(self.dict)

    @property
    def dict(self):
        return {
            'latitude': self.y,
            'longitude': self.x
        }
