from time import sleep
from typing import Tuple

import pygame

from position_tracker import PositionTracker
from vmap import Map
from waypoint import Waypoint
from map.map import Map as OSMap
from map.position import Position


class Visualizer:

    draw_car = True

    def __init__(self, map_name: str, pt: PositionTracker, osmap: OSMap = None):

        self.map = Map.get_map(map_name)
        self.osmap = osmap

        ratio = self.map.img.get_height() / self.map.img.get_width()
        width = 1000
        height = int(width * ratio)
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))

        self.map.convert_img(width, height)

        self.px = (self.map.right_bottom[0] - self.map.left_top[0]) / width
        self.py = (self.map.left_top[1] - self.map.right_bottom[1]) / height

        self.orig_car = pygame.transform.scale(pygame.image.load('resources/car.png'), (32, 15))
        self.car_image = self.orig_car

        self.points = []
        self.adjusted = []
        self.waypoints = []

        self.pt = pt

        self.draw_exact = True
        self.draw_adjusted = True

        pygame.display.set_caption('Visualizer')

    def set_waypoints(self, waypoints):
        self.waypoints = waypoints

    def load_csv(self, filename: str):
        with open(filename) as f:
            for line in f:
                if line:
                    split = line.split(';')
                    x = float(split[1])
                    y = float(split[0])
                    self.pt.add((x, y))
                    self.update_from_pt()
                    self.poll_events()
                    sleep(0.2)

    def coords_to_cart(self, x: float, y: float) -> Tuple[int, int]:
        x = (x - self.map.left_top[0]) / self.px
        y = self.height - (y - self.map.right_bottom[1]) / self.py
        return x, y

    def cart_to_coords(self, x: float, y: float) -> Tuple[float, float]:
        lon = self.map.left_top[0] + x * self.px
        lat = self.map.right_bottom[1] + (self.height - y) * self.py
        return lon, lat

    def redraw(self):
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.map.img, self.map.img.get_rect())

        if self.draw_exact:
            for point in self.points:
                pygame.draw.circle(self.screen, (255, 0, 0), (point[0], point[1]), 1)

        if self.draw_adjusted:
            for point in self.adjusted:
                pygame.draw.circle(self.screen, (66, 135, 245), (point[0], point[1]), 1)

        if self.osmap is not None:
            for vector in self.osmap.vectors:
                begin = self.coords_to_cart(vector.begin.lon, vector.begin.lat)
                end = self.coords_to_cart(vector.end.lon, vector.end.lat)
                pygame.draw.line(self.screen, (66, 135, 245), begin, end, 2)

            for node in self.osmap.nodes:
                pos = self.coords_to_cart(node.lon, node.lat)
                pygame.draw.circle(self.screen, (13, 70, 161), pos, 4)
                pygame.draw.circle(self.screen, (66, 135, 245), pos, 2)

        if self.osmap is not None:
            car_pos = self.pt.position_history[0]
            car_pos = Position(lat=car_pos[1], lon=car_pos[0])
            for vector in self.osmap.vectors:
                shortest = car_pos.shortest_path(vector)
                if shortest is None:
                    continue
                begin = self.coords_to_cart(shortest.begin.lon, shortest.begin.lat)
                end = self.coords_to_cart(shortest.end.lon, shortest.end.lat)
                pygame.draw.line(self.screen, (245, 117, 66), begin, end, 2)

                begin = self.coords_to_cart(vector.begin.lon, vector.begin.lat)
                end = self.coords_to_cart(vector.end.lon, vector.end.lat)
                pygame.draw.line(self.screen, (245, 117, 66), begin, end, 3)

        for wp in self.waypoints:
            x, y = self.coords_to_cart(wp.x, wp.y)
            pygame.draw.circle(self.screen, (255, 138, 138), (x, y), 15)
            pygame.draw.circle(self.screen, (255, 78, 78), (x, y), 5)

        if self.pt.position_history and self.pt.position_history[0] is not None and Visualizer.draw_car:
            w = self.car_image.get_rect().width
            h = self.car_image.get_rect().height
            pos = self.pt.position_history[0]
            pos = self.coords_to_cart(pos[0], pos[1])
            x = pos[0] - w/2
            y = pos[1] - h/2
            self.screen.blit(self.car_image, pygame.Rect(x, y, w, h))

        pygame.display.flip()

    def update_from_pt(self):
        if self.pt.prediction is not None:
            hist = self.pt.prediction  # self.pt.position_history[0]
            if hist is None:
                return self.redraw()
            self.points.append(self.coords_to_cart(hist[0], hist[1]))
            adj = self.pt.current_position
            self.adjusted.append(self.coords_to_cart(adj[0], adj[1]))
            rot = 0 if self.pt.rotation is None else self.pt.rotation
            self.car_image = pygame.transform.rotate(self.orig_car, rot)

        self.redraw()

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise InterruptedError('Program closed by user')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.draw_adjusted = not self.draw_adjusted
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.draw_exact = not self.draw_exact
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                x, y = self.cart_to_coords(x, y)
                self.waypoints.append(Waypoint(x, y))

    def update(self):
        self.update_from_pt()
        self.poll_events()


if __name__ == '__main__':
    pt = PositionTracker()
    vis = Visualizer('garage', pt)
    files = ['geodoma', 'geohrbitov', 'geolouky', 'geoolsina', 'geoolsinaauto',
             'geoolsinazahradni', 'garage', 'waypoint1', 'waypoint2', 'waypointstart']
    files = [f'resources/{name}.csv' for name in files]

    begin_x = vis.map.left_top[0]
    begin_y = vis.map.left_top[1]
    w = vis.map.right_bottom[0] - vis.map.left_top[0]
    h = vis.map.left_top[1] - vis.map.right_bottom[1]

    _waypoints = [
        Waypoint(begin_x + w * 0.7, begin_y - h * 0.6),
        # Waypoint(begin_x + w * 0.32, begin_y - h * 0.8),
        # Waypoint(begin_x + w * 0.2, begin_y - h * 0.3)
    ]

    waypoints = [
        Waypoint(18.1621976, 49.8358295),
        Waypoint(18.1621679, 49.8357131),
        # Waypoint(18.1622303, 49.8356781),
        # Waypoint(18.1624181, 49.8356175),
        # Waypoint(49.8355103, 18.1625603),
        # Waypoint(49.8354083, 18.1626969),
        # Waypoint(49.8353356, 18.1627667),
        # Waypoint(49.8351281, 18.1626489)
    ]

    vis.set_waypoints(waypoints)

    vis.load_csv(files[-1])
    print(pt.current_position)

    while True:
        vis.poll_events()
        vis.redraw()
