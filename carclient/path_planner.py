from typing import List

import geopy.distance

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

        angle = abs(angle)
        d = int(direction)

        if angle <= 1.0:
            self.steering = 0
        elif angle <= 5.0:
            self.steering = 2 * d
        elif angle <= 10.0:
            self.steering = 4 * d
        elif angle <= 20.0:
            self.steering = 6 * d
        elif angle <= 40:
            self.steering = 8 * d
        elif angle <= 60.0:
            self.steering = 10 * d
        elif angle <= 90.0:
            self.steering = 15 * d
        else:
            self.steering = 20 * d

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

        current = self.pt.current_position
        des = waypoints[0].position

        dx = geopy.distance.distance((current[0], current[1]), (des[0], current[1])).m
        dy = geopy.distance.distance((current[0], current[1]), (current[0], des[1])).m

        dx *= 1 if des[0] > current[0] else -1
        dy *= 1 if des[1] > current[1] else -1

        heading = calc_angle(begin=(0, 0), end=(dx, dy))

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
