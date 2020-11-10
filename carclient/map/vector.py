from geopy import distance

from map.position import Position


class Vector:
    def __init__(self, begin: Position, end: Position):
        self.begin = begin
        self.end = end
        self.dist = distance.distance(begin.tuple, end.tuple).m
