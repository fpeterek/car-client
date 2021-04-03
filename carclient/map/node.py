from typing import Set, Tuple

from map.path import Path
from map.position import Position


class Node:
    def __init__(self, pos: Position, paths: Set[Path] = None):
        self.paths: Set[Path] = set() if paths is None else paths
        self.pos: Position = pos

    def add_path(self, path: Path):
        if path.begin != self.pos and path.end != self.pos:
            return

        if path in self.paths or path.reversed in self.paths:
            return

        self.paths.add(path)

    def __hash__(self):
        return hash(self.pos)

    @property
    def lat(self) -> float:
        return self.pos.lat

    @property
    def lon(self) -> float:
        return self.pos.lon

    @property
    def lonlat(self) -> Tuple[float, float]:
        return self.pos.lonlat

    @property
    def latlon(self) -> Tuple[float, float]:
        return self.lat, self.lon
