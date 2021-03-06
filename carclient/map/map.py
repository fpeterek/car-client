from typing import Set, Optional, Tuple, Dict, List

from map.path import Path
from map.node import Node
from map.position import Position


class Map:
    def __init__(self):
        self.nodes: Set[Node] = set()
        self.paths: Set[Path] = set()
        self.node_by_position: Dict[Position, Node] = dict()

    def add_node(self, node: Node):
        if node not in self.nodes:
            self.nodes.add(node)
            self.node_by_position[node.pos] = node

    def _traverse_graph(self, begin: Path, end: Path) -> Dict[Path, Path]:
        preceding_paths: Dict[Path, Path] = dict()
        current_paths: Set[Path] = {begin}

        # Traverse map
        while current_paths:
            next_paths: Set[Path] = set()
            for path in current_paths:
                neighbours = self.node_by_position[path.begin].paths | self.node_by_position[path.end].paths
                neighbours = {n for n in neighbours if n not in preceding_paths}
                for n in neighbours:
                    preceding_paths[n] = path
                    # Return upon discovering the final destination -> there's no need to advance traversal any further
                    if n == end:
                        return preceding_paths
                next_paths |= neighbours
            current_paths = next_paths

        return preceding_paths

    def find_path(self, begin: Path, end: Path) -> List[Path]:
        if begin == end:
            return [begin]

        preceding_paths = self._traverse_graph(begin, end)

        # Reconstruct path
        path = []
        current = end
        while current != begin:
            path.insert(0, current)
            current = preceding_paths[current]
        path.insert(0, begin)

        return path

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
