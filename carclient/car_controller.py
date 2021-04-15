import time
from typing import List, Optional
from threading import Lock

from path_planner import PathPlanner
from position_fetcher import PositionFetcher
from position_tracker import PositionTracker
from visualizer import Visualizer
from waypoint import Waypoint

from map.map_loader import MapLoader
from map.position import Position


class CarController:

    def __init__(self, map_name='campus'):
        self.map = MapLoader.load(path='resources/campus.json')
        self.pt = PositionTracker(osmap=self.map)
        self.pf = PositionFetcher(self.pt)
        self.planner = PathPlanner(self.pt, on_wp_reached=self.remove_waypoint)
        self.vis = Visualizer(map_name=map_name, pt=self.pt, add_wp=self.add_waypoint, osmap=self.map)
        self.waypoints_lock = Lock()
        self.waypoints_changed = True
        self.waypoints: Optional[List[Waypoint]] = None
        self.set_waypoints([])

    def get_waypoints(self) -> List[Waypoint]:
        with self.waypoints_lock:
            return self.waypoints[:]

    def on_waypoint_change(self) -> None:
        self.waypoints_changed = True
        self.vis.set_waypoints(self.waypoints[:])

    def remove_waypoint(self, waypoint_id: int) -> None:
        with self.waypoints_lock:
            self.waypoints = list(filter(lambda wp: wp.id != waypoint_id, self.waypoints))
            self.on_waypoint_change()

    def update_position(self) -> None:
        if not self.pf.fetch():
            self.planner.predict_position()

    def add_waypoint(self, waypoint: Waypoint) -> None:
        with self.waypoints_lock:
            orig_pos = Position(lat=waypoint.lat, lon=waypoint.lon)
            adjusted_position, path = self.map.closest_point(orig_pos)
            waypoint.path = path
            waypoint.lat = adjusted_position.lat
            waypoint.lon = adjusted_position.lon
            self.waypoints.append(waypoint)
            self.on_waypoint_change()

    def set_waypoints(self, waypoints: List[Waypoint]) -> None:
        with self.waypoints_lock:
            self.waypoints = waypoints
            self.on_waypoint_change()

    def init_position(self):
        for i in range(1, 0, -1):
            self.update_position()
            self.vis.update()
            print(i)
            time.sleep(1.0)

    def follow_waypoints(self) -> None:

        self.set_waypoints([
            # Waypoint(18.1622607, 49.8358360),
            # Waypoint(18.1620518, 49.8356722)

            # Waypoint(18.1622303, 49.8356781),
            # Waypoint(18.1624181, 49.8356175),
            # Waypoint(49.8355103, 18.1625603),
            # Waypoint(49.8354083, 18.1626969),
            # Waypoint(49.8353356, 18.1627667),
            # Waypoint(49.8351281, 18.1626489)
        ])

        self.pt.disable_rotation()

        copy = None

        while True:
            self.update_position()
            self.vis.update()
            if self.waypoints_changed:
                with self.waypoints_lock:
                    copy = self.waypoints[:]
                    self.waypoints_changed = False
            self.planner.plan(copy)
            self.pt.enable_rotation()
            time.sleep(0.1)

    def follow_qr(self):
        while True:
            self.planner.plan_from_camera()
            self.update_position()
            time.sleep(0.2)
            self.vis.update()
