import time
from typing import List

from path_planner import PathPlanner
from position_fetcher import PositionFetcher
from position_tracker import PositionTracker
from visualizer import Visualizer
from waypoint import Waypoint

from map.map_loader import MapLoader


class CarController:

    def __init__(self, map_name='campus'):
        self.map = MapLoader.load(path='resources/campus.osm')
        self.pt = PositionTracker(osmap=self.map)
        self.pf = PositionFetcher(self.pt)
        self.planner = PathPlanner(self.pt)
        self.vis = Visualizer(map_name=map_name, pt=self.pt, osmap=self.map)
        self.waypoints = None
        self.set_waypoints([])

    def update_position(self) -> None:
        if not self.pf.fetch():
            self.planner.predict_position()

    def set_waypoints(self, waypoints: List[Waypoint]) -> None:
        self.waypoints = waypoints
        self.vis.set_waypoints(self.waypoints)

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

        while True:
            self.update_position()
            self.vis.update()
            self.planner.plan(self.waypoints)
            self.pt.enable_rotation()
            time.sleep(0.1)

    def follow_qr(self):
        while True:
            self.planner.plan_from_camera()
            self.update_position()
            time.sleep(0.2)
            self.vis.update()
