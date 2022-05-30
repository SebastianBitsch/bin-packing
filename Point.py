from functools import total_ordering
from enum import Enum

class PointType(Enum):
    BOTTOM_LEFT = 0
    BOTTOM_RIGHT = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3

@total_ordering
class Point:
    def __init__(self, x=0, y=0) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __repr__(self):
        return "P = ({}, {})".format(self.x, self.y)

    def __lt__(self, other):
        '''
        Return the point which is closest to (0,0)
        '''
        return self.distance(Point()) < other.distance(Point())
    
    def __hash__(self):
        return hash(str(self))
