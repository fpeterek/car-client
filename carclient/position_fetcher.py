import time

from client import position
from position_tracker import PositionTracker


class PositionFetcher:
    def __init__(self, pt: PositionTracker, interval=1.0):
        self.interval = interval
        self.last_update = 0.0
        self.pt = pt

    @property
    def current_time(self):
        return time.time_ns() / 10**9

    @property
    def should_fetch(self):
        return self.current_time >= (self.last_update + self.interval)

    def fetch(self) -> bool:
        if self.should_fetch:
            self.pt.add(position())
            self.last_update = self.current_time
            return True
        return False
