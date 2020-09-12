from typing import Tuple

import pygame

from vmap import Map


class Visualizer:

    def __init__(self, map_name: str):

        self.map = Map.get_map(map_name)

        ratio = self.map.img.get_height() / self.map.img.get_width()
        width = 1000
        height = int(width * ratio)
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))

        self.map.convert_img(width, height)

        self.px = (self.map.right_bottom[0] - self.map.left_top[0]) / width
        self.py = (self.map.left_top[1] - self.map.right_bottom[1]) / height

        print(self.map.left_top, self.map.right_bottom)
        print(self.px, self.py)

        self.points = []

        pygame.display.set_caption('Visualizer')

    def load_csv(self, filename: str):
        with open(filename) as f:
            for line in f:
                if line:
                    split = line.split(';')
                    x = float(split[1])
                    y = float(split[0])
                    self.add_point(x, y)

    def coords_to_cart(self, x: float, y: float) -> Tuple[int, int]:
        x = (x - self.map.left_top[0]) / self.px
        y = self.height - (y - self.map.right_bottom[1]) / self.py
        return x, y

    def redraw(self):
        self.screen.fill((255, 255, 255))

        self.screen.blit(self.map.img, self.map.img.get_rect())

        for point in self.points:
            pygame.draw.circle(self.screen, (255, 0, 0), (point[0], point[1]), 2)

        pygame.display.flip()

    def add_point(self, x, y):
        self.points.append(self.coords_to_cart(x, y))

    def poll_events(self):
        for _ in pygame.event.get():
            pass


if __name__ == '__main__':
    vis = Visualizer('koberice')
    files = ['geodoma', 'geohrbitov', 'geolouky', 'geoolsina', 'geoolsinaauto', 'geoolsinazahradni']
    files = [f'resources/{name}.csv' for name in files]
    vis.load_csv(files[2])
    # vis.add_point(18.051836315436294, 49.98021897903856)
    # vis.add_point(18.051065580146712, 49.98034028731247)
    # vis.add_point(18.050132749635395, 49.98033176847581)

    while True:
        vis.poll_events()
        vis.redraw()
