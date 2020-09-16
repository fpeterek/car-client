from typing import List

from direction import Direction
from position_tracker import PositionTracker
from carutil import calc_angle
from waypoint import Waypoint

from client import drive


class PathPlanner:

    def __init__(self, pt: PositionTracker):
        self.desired_heading = 0.0
        self.pt = pt
        self.steering = 0.0
        self.velocity = 0.0

    @staticmethod
    def sign(x: float) -> float:
        return -1 if x < 0 else 1

    @staticmethod
    def calc_angle(cur: float, des: float) -> float:
        cur += 360 if cur == 0 else 0
        des += 360 if des == 0 else 0
        dist = des - cur
        dist2 = (360 - abs(dist)) * PathPlanner.sign(dist) * -1
        return dist if abs(dist) < abs(dist2) else dist2

    def adjust_steering(self):

        if self.pt.rotation is None:
            return

        angle = PathPlanner.calc_angle(cur=self.pt.rotation, des=self.desired_heading)
        direction = [Direction.LEFT, Direction.RIGHT][angle > 0]

        if abs(angle) <= 1.0:
            self.steering = 0
        elif abs(angle) <= 5.0:
            self.steering = 2 * int(direction)
        elif abs(angle) <= 10.0:
            self.steering = 5 * int(direction)
        else:
            self.steering = 20 * int(direction)

    def adjust_speed(self, waypoints: List[Waypoint]):

        car_pos = self.pt.current_position

        if not waypoints or car_pos is None:
            self.velocity = 0
            return

        w0 = waypoints[0]

        if w0.point_inside(car_pos):
            waypoints.pop(0)

        if waypoints:
            self.velocity = 100

    def calc_desired_heading(self, waypoints):
        if not waypoints or self.pt.rotation is None:
            return

        heading = calc_angle(begin=self.pt.current_position, end=waypoints[0].position)

        return heading

    def plan(self, waypoints: List[Waypoint]):

        car_pos = self.pt.current_position

        if not waypoints or car_pos is None:
            self.velocity = 0.0
            self.steering = 0.0
            return drive(int(self.velocity), int(self.steering))

        self.desired_heading = self.calc_desired_heading(waypoints)

        self.adjust_steering()
        self.adjust_speed(waypoints)

        drive(int(self.velocity), int(self.steering))
