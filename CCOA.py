from copy import copy
from Point import Point
from Rectangle import Rect
import numpy as np

class CCOA:
    def __init__(self, rect: Rect, origin: Point, rotated: bool) -> None:
        self.rect = rect
        self.origin = origin
        self.rotated = rotated
        if rotated:
            rect.rotate()

    def vertices(self):
        o = self.origin
        return [
            o, 
            copy(o).shift(self.rect.width,0), 
            copy(o).shift(0, self.rect.height),
            copy(o).shift(self.rect.width, self.rect.height)
        ]

    def degree(self, M):
        r = 1 # Dont know what this factor is meant to do
        dists = [min_distance(self, m) for m in M] #TODO: Add the edges of the container, excluding the ones it might be touching
        return 1 - (min(dists) / (r * (self.rect.width + self.rect.height)/2))

    def __repr__(self) -> str:
        return "CCOA({}; {}, {})".format(self.rect, self.origin, self.rotated)

def min_distance(ccoa1: CCOA, ccoa2: CCOA):
    delta1 = ccoa1.vertices()[0].coords() - ccoa2.vertices()[3].coords()
    delta2 = ccoa2.vertices()[0].coords() - ccoa1.vertices()[3].coords()
    u = np.max(np.array([np.zeros(2), delta1]), axis=0)
    v = np.max(np.array([np.zeros(2), delta2]), axis=0)
    dist = np.linalg.norm(np.concatenate([u, v]))
    return dist

# a = CCOA(Rect(0, 1, 2),Point(0,0),True)
# b = CCOA(Rect(1, 1, 1),Point(0,3),False)

# print(min_distance(a,b))