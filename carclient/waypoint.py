from typing import Tuple


class Waypoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # self.radius = 10
        self.tolerance = 0.00010

    def point_inside(self, point: Tuple[float, float]) -> bool:
        sx = self.x - point[0]
        sy = self.y - point[1]
        dist = (sx**2 + sy**2) ** 0.5
        return dist <= self.tolerance

    @property
    def position(self) -> Tuple[float, float]:
        return self.x, self.y
