import time
from typing import Tuple, Optional

from util.util import calc_angle_lonlat

from map.map import Map
from map.position import Position
from map.path import Path


class PositionTracker:

    hist_len = 10

    def __init__(self, osmap: Map):
        self.last_pos = None
        self.position_history = []
        self._rotation = None
        self.rotation_enabled = True
        self.last_updated = PositionTracker.time()
        self.prediction = None
        self.rotation_prediction = None
        self.last_prediction = PositionTracker.time()
        self.osmap = osmap

    @staticmethod
    def time():
        return time.time_ns() / 10**9

    @property
    def time_since_update(self):
        return PositionTracker.time() - self.last_updated

    def enable_rotation(self):
        self.rotation_enabled = True

    def disable_rotation(self):
        self.rotation_enabled = False

    @property
    def rotation(self):
        return self._rotation if self.rotation_enabled else None

    @property
    def current_position(self) -> Optional[Tuple[float, float]]:
        if not self.position_history or self.position_history[0] is None:
            return None

        weight = 1.0

        x_sum = 0.0
        y_sum = 0.0

        total = 0

        for pos in self.position_history:
            x_sum += pos[0] * weight
            y_sum += pos[1] * weight
            total += weight
            weight *= 0.7

        return x_sum / total, y_sum / total

    def trim_hist(self):
        if len(self.position_history) > PositionTracker.hist_len:
            self.position_history = self.position_history[0:-1]

    @staticmethod
    def _round_position(lonlat: Tuple[float, float]) -> Tuple[float, float]:
        return int(lonlat[0] * 10**6) / 10**6, int(lonlat[1] * 10**6) / 10**6

    def calc_rotation(self):
        if len(self.position_history) < 2 or self.position_history[0] is None or self.last_pos is None:
            return

        # Round positions to avoid floating point number inaccuracies and errors
        current = PositionTracker._round_position(self.current_position)
        last = PositionTracker._round_position(self.last_pos)

        if current == last:
            return

        self._rotation = calc_angle_lonlat(begin=last, end=current)

    def add(self, pos: Tuple[float, float]):
        self.last_pos = self.current_position
        self.last_updated = PositionTracker.time()

        if self.position_history and self.position_history[0] is None:
            self.position_history[0] = pos
        else:
            self.position_history.insert(0, pos)

        self.trim_hist()
        self.calc_rotation()

        print(f'Car heading: {self.rotation}')

        self.update_prediction(self.current_position, self._rotation)

    def update_prediction(self, position, rotation):
        self.prediction = position
        self.rotation_prediction = rotation
        self.last_prediction = PositionTracker.time()

    @property
    def closest_shortest_pair(self) -> Optional[Tuple[Path, Path]]:
        if self.last_pos is None:
            return None

        osm_pos = Position(lat=self.last_pos[1], lon=self.last_pos[0])

        closest_path = None
        shortest_distance = None
        length = None
        for v in self.osmap.paths:
            path = osm_pos.shortest_path(v)
            if path is None:
                continue
            if length is None or path.dist < length:
                shortest_distance = path
                closest_path = v
                length = path.dist
        return closest_path, shortest_distance

    @property
    def closest_path(self) -> Optional[Path]:
        pair = self.closest_shortest_pair
        return pair[0] if pair is not None else None

    @property
    def shortest_distance(self) -> Optional[Path]:
        pair = self.closest_shortest_pair
        return pair[1] if pair is not None else None
