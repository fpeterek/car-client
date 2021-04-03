import json

from map.map import Map
from map.node import Node
from map.position import Position
from map.path import Path


class MapLoader:

    @staticmethod
    def parse_position(position: dict) -> Position:
        return Position(lat=position["lat"], lon=position["lon"])

    @staticmethod
    def parse_nodes(m: Map, nodes: list) -> None:
        for node in nodes:
            position = MapLoader.parse_position(node["position"])
            m.add_node(Node(pos=position))

    @staticmethod
    def parse_paths(m: Map, paths: list) -> None:
        for path in paths:
            begin = MapLoader.parse_position(path["begin"])
            end = MapLoader.parse_position(path["end"])
            m.add_path(Path(begin=begin, end=end))

    @staticmethod
    def parse_map(json_object: dict) -> Map:
        res = Map()

        m = json_object["map"]
        MapLoader.parse_nodes(res, m["nodes"])
        MapLoader.parse_paths(res, m["paths"])

        return res

    @staticmethod
    def load(path: str) -> Map:
        with open(path) as file:
            json_object = json.load(file)
            return MapLoader.parse_map(json_object)
