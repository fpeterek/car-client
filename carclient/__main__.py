import time

import menu
from client import position, camera_info
from path_planner import PathPlanner
from position_fetcher import PositionFetcher
from position_tracker import PositionTracker
from visualizer import Visualizer
from waypoint import Waypoint


def follow_waypoints():

    pt = PositionTracker()
    pf = PositionFetcher(pt)
    planner = PathPlanner(pt)
    vis = Visualizer(map_name='garage', pt=pt)

    waypoints = [
        Waypoint(18.1622607, 49.8358360),
        Waypoint(18.1620518, 49.8356722)
        # Waypoint(18.1622303, 49.8356781),
        # Waypoint(18.1624181, 49.8356175),
        # Waypoint(49.8355103, 18.1625603),
        # Waypoint(49.8354083, 18.1626969),
        # Waypoint(49.8353356, 18.1627667),
        # Waypoint(49.8351281, 18.1626489)
    ]

    vis.set_waypoints(waypoints)

    pt.disable_rotation()
    for i in range(1, 0, -1):
        pf.fetch()
        vis.update_from_pt()
        vis.poll_events()
        print(i)
        time.sleep(1.0)

    while waypoints:
        pf.fetch()
        vis.update_from_pt()
        vis.poll_events()
        planner.plan(waypoints)
        pt.enable_rotation()
        time.sleep(0.1)

    planner.plan(waypoints)

    while True:
        pf.fetch()
        vis.update_from_pt()
        vis.poll_events()
        time.sleep(1.0)


def follow_qr():
    pt = PositionTracker()
    planner = PathPlanner(pt)
    vis = Visualizer(map_name='garage', pt=pt)

    while True:
        planner.plan_from_camera()
        # pt.add(position())
        time.sleep(0.2)
        vis.update_from_pt()
        vis.poll_events()


if __name__ == '__main__':

    try:
        follow_waypoints()
    except InterruptedError as e:
        # Shutdown on ctrl+c or window closed
        print('Shutting down as per user request')
