import os
import math
from typing import List

import geopy.distance

from direction import Direction
from position_tracker import PositionTracker
from carutil import calc_angle
from waypoint import Waypoint

from client import drive, camera_info


class PathPlanner:

    image_width = int(os.getenv('IMAGE_WIDTH'))
    image_half = image_width / 2

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

    @staticmethod
    def calc_des_heading(current, des):
        dx = geopy.distance.distance((current[0], current[1]), (des[0], current[1])).m
        dy = geopy.distance.distance((current[0], current[1]), (current[0], des[1])).m

        dx *= 1 if des[0] > current[0] else -1
        dy *= 1 if des[1] > current[1] else -1

        return calc_angle(begin=(0, 0), end=(dx, dy))

    def calc_linear(self, waypoints):
        if not waypoints or self.pt.rotation is None:
            return

        current = self.pt.current_position
        des = waypoints[0].position

        heading = PathPlanner.calc_des_heading(current, des)

        return heading

    def calc_curve(self, waypoints):
        if len(waypoints) < 2:
            return self.calc_linear(waypoints)

        current = self.pt.current_position
        p1 = waypoints[0].position
        p2 = waypoints[1].position

        d1 = geopy.distance.distance(current, p1).m
        d2 = geopy.distance.distance(current, p2).m

        if d1 > 10:
            return self.calc_linear(waypoints)

        ratio = max(0, d1-2) / max(0, d2-2)

        if ratio < 0.3 or d1 <= 2:
            waypoints.pop(0)

        h1 = PathPlanner.calc_des_heading(current, p1)
        h2 = PathPlanner.calc_des_heading(current, p2)

        return h1 * ratio + h2 * (1 - ratio)

    def calc_desired_heading(self, waypoints):
        return self.calc_curve(waypoints)

    def plan_from_camera(self):

        s, c = camera_info()

        sin = math.fabs(s/c)

        if sin < 0 or sin > 1:
            return

        print(f'From camera {(s, c)}; sin={sin}')

        deg = math.degrees(math.fabs(math.asin(sin)))

        alpha = min(20, int(deg)) * (-1 if c < 0 else 1)
        v = 100 if s > 2 else 0

        print(f'Drive cmd: v={v}, alpha={alpha}')

        # drive(v, int(alpha))

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
