from typing import Set, Optional, Tuple

from map.path import Path
from map.node import Node
from map.position import Position


class Map:
    def __init__(self):
        self.nodes: Set[Node] = set()
        self.paths: Set[Path] = set()

    def add_node(self, node: Node):
        if node not in self.nodes:
            self.nodes.add(node)

    def add_path(self, path):
        if path in self.paths or path.reversed in self.paths:
            return

        self.paths.add(path)

        for node in self.nodes:
            node.add_path(path)

    def closest_point(self, position: Position) -> Tuple[Position, Path]:
        shortest_path: Optional[Path] = None  # Shortest path to the closest path
        closest_path: Optional[Path] = None  # The closest path itself

        for path in self.paths:
            vec: Path = position.shortest_path(path)
            if shortest_path is None or shortest_path.dist > vec.dist:
                shortest_path = vec
                closest_path = path

        closest_point = shortest_path.begin if shortest_path.begin != position else shortest_path.end
        return closest_point, closest_path
