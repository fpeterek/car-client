from typing import List, Tuple

from map.vector import Vector
from map.position import Position


class Node:
    def __init__(self, pos: Position, vectors: List[Vector] = None):
        self.vectors = [] if vectors is None else vectors
        self.pos = pos

    def add_vector(self, vector: Vector):
        if vector.begin == self.pos or vector.end == self.pos:
            self.vectors.append(vector)

    def __hash__(self):
        return hash(self.pos)

    @property
    def lat(self) -> float:
        return self.pos.lat

    @property
    def lon(self) -> float:
        return self.pos.lon

    @property
    def tuple(self) -> Tuple[float, float]:
        return self.pos.tuple
