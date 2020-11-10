import osmium

from map.map import Map
from map.node import Node
from map.position import Position
from map.vector import Vector


class MapLoaderHandler(osmium.SimpleHandler):
    excluded_ways = ('footway', 'corridor', 'sidewalks', 'steps', 'crossing')

    def __init__(self):
        super(MapLoaderHandler, self).__init__()
        self.map = Map()

    def node(self, n):
        position = Position(lon=n.location.lon, lat=n.location.lat)
        node = Node(pos=position)
        self.map.add_node(node)

    def way(self, way):
        if not way.nodes or 'highway' not in way.tags or way.is_closed():
            return
        if way.tags['highway'] in MapLoaderHandler.excluded_ways:
            return
        previous = way.nodes[0]

        for i in range(1, len(way.nodes)):
            current = way.nodes[i]

            begin = Position(lon=previous.lon, lat=previous.lat)
            end = Position(lon=current.lon, lat=current.lat)

            vector = Vector(begin=begin, end=end)
            self.map.add_vector(vector)

            previous = current

    def relation(self, way):
        """noop -> There's no need to handle relations, at least not now"""


class MapLoader:
    def __init__(self):
        pass

    @staticmethod
    def remove_unnecessary_nodes(map: Map):
        map.nodes = {node: node for node in map.nodes if node.vectors}
        return map

    @staticmethod
    def load(path: str) -> Map:
        handler = MapLoaderHandler()
        handler.apply_file(path, locations=True)
        MapLoader.remove_unnecessary_nodes(handler.map)
        return handler.map















