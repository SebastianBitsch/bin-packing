from copy import copy
from Point import Point, PointType, distance
from Rectangle import Rect
import numpy as np

class CCOA:
    def __init__(self, rect: Rect, origin: Point, rotated: bool, container:Rect) -> None:
        self.rect = rect
        self.rotated = rotated
        self.container = container

        if rotated:
            rect.rotate()

        self.origin = origin
        if origin.type == PointType.BOTTOM_LEFT:
            pass
        elif origin.type == PointType.BOTTOM_RIGHT:
            self.origin.shift(-self.rect.width,0)
        elif origin.type == PointType.TOP_LEFT:
            self.origin.shift(0, -self.rect.height)
        elif origin.type == PointType.TOP_RIGHT:
            self.origin.shift(-self.rect.width, -self.rect.height)


    def vertices(self):
        o = self.origin
        return [
            o, 
            copy(o).shift(self.rect.width,0), 
            copy(o).shift(0, self.rect.height),
            copy(o).shift(self.rect.width, self.rect.height)
        ]

    def bordering_boxes(self) -> list[Rect]:
        boxes = []
        top = CCOA(Rect(-1,self.container.width, 1), Point(0, self.container.height,None), False, self.container)
        bottom = CCOA(Rect(-1,self.container.width, 1), Point(0, -1,None), False, self.container)
        left = CCOA(Rect(-1, 1, self.container.height), Point(-1, 0,None), False, self.container)
        right = CCOA(Rect(-1, 1, self.container.height), Point(self.container.width, 0,None), False, self.container)
        # if self.origin.x != 0:
        #     boxes.append(bottom)
        # if self.origin.y != 0:
        #     boxes.append(left)
        # if self.origin.y + self.rect.height != top.origin:
        #     boxes.append(top)
        # if self.origin.x + self.rect.width != right.origin:
        #     boxes.append(right)
        
        # return boxes
        
        # if self.origin.x != 0:
        #     boxes.append(left)
        # if self.origin.y != 0:
        #     boxes.append(bottom)
        # if self.origin.x + self.rect.width != self.container.width:
        #     boxes.append(right)
        # if self.origin.y + self.rect.height != self.container.height:
        #     boxes.append(top)
        return [top,bottom,left,right]

    def degree(self, M):
        rects = copy(M)
        r = 1 # Dont know what this factor is meant to do
        rects.extend(self.bordering_boxes())
        dists = [min_distance(self, m) for m in rects] #TODO: Add the edges of the container, excluding the ones it might be touching
        
        # Remove two smallest elements, which will be 0 - the two imediate neighbours
        dists.remove(min(dists))
        dists.remove(min(dists))

        return 1 - (min(dists) / (r * (self.rect.width + self.rect.height)/2))

    def collides(self, other):
        return self.origin.x < other.origin.x + other.rect.width and other.origin.x < self.origin.x + self.rect.width and self.origin.x < other.origin.y + other.rect.height and other.origin.y < self.origin.y + self.rect.height

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