from typing import List, Dict

from map.vector import Vector
from map.node import Node


class Map:
    def __init__(self):
        self.nodes: Dict[Node, Node] = {}
        self.vectors: List[Vector] = []

    def add_node(self, node: Node):
        if node not in self.nodes:
            self.nodes[node] = node

    def add_vector(self, vector):
        if vector.begin in self.nodes:
            self.nodes[vector.begin].add_vector(vector)
        if vector.end in self.nodes:
            self.nodes[vector.end].add_vector(vector)

        self.vectors.append(vector)
