import json
from threading import Lock

import geopy.distance

from typing import Tuple


class Waypoint:

    waypoint_lock = Lock()
    counter = 1

    @staticmethod
    def get_id() -> int:
        with Waypoint.waypoint_lock:
            copy = Waypoint.counter
            Waypoint.counter += 1
            return copy

    def __init__(self, x, y):
        self.id = Waypoint.get_id()
        self.path = None
        self.x = x
        self.y = y
        self.tolerance = 2

    def point_inside(self, point: Tuple[float, float]) -> bool:
        dist = geopy.distance.distance(self.position, point).m
        return dist <= self.tolerance

    @property
    def position(self) -> Tuple[float, float]:
        return self.x, self.y

    @property
    def latlon(self) -> Tuple[float, float]:
        return self.y, self.x

    @property
    def lat(self) -> float:
        return self.y

    @lat.setter
    def lat(self, value: float) -> None:
        self.y = value

    @property
    def lon(self) -> float:
        return self.x

    @lon.setter
    def lon(self, value: float) -> None:
        self.x = value

    @property
    def json(self):
        return json.dumps(self.dict)

    @property
    def dict(self):
        return {
            "position": {
                'latitude': self.y,
                'longitude': self.x,
            },
            'id': self.id
        }
