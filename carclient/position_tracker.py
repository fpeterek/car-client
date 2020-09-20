from typing import Tuple

from carutil import calc_angle


class PositionTracker:

    hist_len = 10

    def __init__(self):
        self.last_pos = None
        self.position_history = []
        self._rotation = None
        self.rotation_enabled = True

    def enable_rotation(self):
        self.rotation_enabled = True

    def disable_rotation(self):
        self.rotation_enabled = False

    @property
    def rotation(self):
        return self._rotation if self.rotation_enabled else None

    @property
    def current_position(self):
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

    def calc_rotation(self):
        if len(self.position_history) < 2 or self.position_history[0] is None or self.last_pos is None:
            return

        if self.current_position == self.last_pos:
            return

        self._rotation = calc_angle(begin=self.last_pos, end=self.current_position)

    def add(self, pos: Tuple[float, float]):
        self.last_pos = self.current_position

        if self.position_history and self.position_history[0] is None:
            self.position_history[0] = pos
        else:
            self.position_history.insert(0, pos)

        self.trim_hist()
        self.calc_rotation()













