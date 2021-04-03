from typing import Set, Dict

from map.path import Path
from map.node import Node


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
