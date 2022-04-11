from enum import Enum
from math import sqrt
from numpy import array

class PointType(Enum):
    BOTTOM_LEFT = 0
    BOTTOM_RIGHT = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3

class Point:
    def __init__(self,x_init,y_init, type: PointType):
        self.x = x_init
        self.y = y_init
        self.type = type

    def shift(self, x, y):
        self.x += x
        self.y += y
        return self

    def __repr__(self):
        return "Point({}, {}, {}".format(self.x, self.y, self.type)

    def coords(self):
        return array([self.x,self.y])


def distance(a, b):
    return sqrt((a.x-b.x)**2+(a.y-b.y)**2)
