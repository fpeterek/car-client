import json
from typing import Tuple

import pygame


class Map:

    @staticmethod
    def get_map(map_name: str):
        with open('resources/maps.json') as f:
            j = json.load(f)
            j = j[map_name]

            img = pygame.image.load(f'resources/{j["image"]}')

            left_top = j['leftTop']
            lx = left_top['x']
            ly = left_top['y']

            right_bottom = j['rightBottom']
            rx = right_bottom['x']
            ry = right_bottom['y']

            return Map(img, (lx, ly), (rx, ry))

    def __init__(self, img: pygame.surface.Surface, left_top: Tuple[float, float], right_bottom: Tuple[float, float]):

        # self.orig_image = pygame.transform.scale(pygame.image.load('resources/car.png'), Car.sprite_dim)
        # self.image = self.orig_image

        self.img: pygame.surface.Surface = img
        self.left_top = left_top
        self.right_bottom = right_bottom

    def convert_img(self, width, height):
        self.img = pygame.transform.scale(self.img, (width, height)).convert()
