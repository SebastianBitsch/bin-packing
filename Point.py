from math import sqrt
from enum import Enum

class PointType(Enum):
    BOTTOM_LEFT = 0
    BOTTOM_RIGHT = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def tuple(self) -> tuple[int,int]:
        return (self.x,self.y)

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __repr__(self):
        return "P = ({}, {})".format(self.x, self.y)

    def distance(self, point):
        """
        Calculate distance to another point
        """
        return sqrt((self.x-point.x)**2+(self.y-point.y)**2)
