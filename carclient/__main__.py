import time

import menu
from client import position
from path_planner import PathPlanner
from position_tracker import PositionTracker
from visualizer import Visualizer
from waypoint import Waypoint


def follow_waypoints():

    pt = PositionTracker()
    planner = PathPlanner(pt)
    vis = Visualizer(map_name='garage', pt=pt)

    waypoints = [
        Waypoint(18.1622607, 49.8358360),
        Waypoint(18.1621518, 49.8356722)
        # Waypoint(18.1622303, 49.8356781),
        # Waypoint(18.1624181, 49.8356175),
        # Waypoint(49.8355103, 18.1625603),
        # Waypoint(49.8354083, 18.1626969),
        # Waypoint(49.8353356, 18.1627667),
        # Waypoint(49.8351281, 18.1626489)
    ]

    vis.set_waypoints(waypoints)

    pt.disable_rotation()
    for i in range(10, 0, -1):
        pos = position()
        pt.add(pos)
        vis.update_from_pt()
        vis.poll_events()
        print(i)
        time.sleep(1.0)

    while waypoints:
        pos = position()
        pt.add(pos)
        vis.update_from_pt()
        vis.poll_events()
        planner.plan(waypoints)
        pt.enable_rotation()
        time.sleep(1.0)

    planner.plan(waypoints)

    while True:
        pt.add(position())
        vis.update_from_pt()
        vis.poll_events()
        time.sleep(1.0)


if __name__ == '__main__':
    # pt = PositionTracker()
    # for i in range(10):
    #     pt.add(position())
    #     print(pt.position_history[0])
    #     time.sleep(1)
    # print(pt.current_position)
    follow_waypoints()
    menu.menu()
