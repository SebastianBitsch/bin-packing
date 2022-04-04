from math import sqrt
from numpy import array

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y
        return self

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

    def coords(self):
        return array([self.x,self.y])


def distance(a, b):
    return sqrt((a.x-b.x)**2+(a.y-b.y)**2)
