from copy import deepcopy
from math import sqrt
from util import PointType

class Rect:

    def __init__(self, origin: tuple, width:float, height:float, origin_type: PointType = PointType.BOTTOM_LEFT, rotated:bool = False) -> None:
        """
        A container class and data structure for a rect representing a box to be packed. 
        Main functionality consists of wrapping and data and checking if rects overlap contain points etc.

        Parameters
        ----------
        origin, tuple
            a tuple of (x,y) coordinates containing the ogigin point of the box. Can be either of corners depending on the case

        width, float
            the width of the rect

        height, float
            the height of the rect

        origin_type, PointType
            an enum value determining which of the four corners is the origin point

        rotated, bool
            boolean value indicating whether the rect is rotated
        """        

        assert(0 < width and 0 < height)

        if rotated:
            temp = height
            height = width
            width = temp

        # Shift origin to bottom left corner depending on what type of point was given
        if origin_type == PointType.BOTTOM_LEFT:
            self.origin = origin
        if origin_type == PointType.TOP_LEFT:
            self.origin = (origin[0], origin[1] - height)
        if origin_type == PointType.BOTTOM_RIGHT:
            self.origin = (origin[0] - width, origin[1])
        if origin_type == PointType.TOP_RIGHT:
            self.origin = (origin[0] - width, origin[1] - height)
        
        self.width = width
        self.height = height
        self.rotated = rotated

        self.bottom = self.origin[1]
        self.top = self.origin[1]+self.height
        self.left = self.origin[0]
        self.right = self.origin[0]+self.width

        self.corner_bot_l = (self.left, self.bottom)
        self.corner_top_l = (self.left, self.top)
        self.corner_top_r = (self.right, self.top)
        self.corner_bot_r = (self.right, self.bottom)


    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result


    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


    @property
    def area(self) -> float:
        return self.width * self.height


    def contains(self, point: tuple) -> bool:
        """ Return whether the rect contains a given point (x,y) """
        return self.corner_bot_l[0] <= point[0] and self.corner_bot_l[1] <= point[1] and point[0] <= self.corner_top_r[0] and point[1] <= self.corner_top_r[1]


    def min_distance(self, other) -> float:
        """
        Returns the minumum distance between two Rects (AABBs), using an outer Rect method as described
        in: https://gamedev.stackexchange.com/questions/154036/efficient-minimum-distance-between-two-axis-aligned-squares
        """
        outer_left = min(self.left, other.left)
        outer_right = max(self.right, other.right)
        outer_bottom = min(self.bottom, other.bottom)
        outer_top = max(self.top, other.top)

        outer_width = outer_right - outer_left
        outer_height = outer_top - outer_bottom

        inner_width = max(0, outer_width - self.width - other.width)
        inner_height = max(0, outer_height - self.height - other.height)

        # TODO: Might be able to remove a sqrt here, not sure
        return sqrt(inner_width**2 + inner_height**2)


    def overlaps(self, other) -> bool:
        """
        Returns wether two Rects overlap
        """
        if self.right <= other.left or other.right <= self.left:
            return False
        if self.top <= other.bottom or other.top <= self.bottom:
            return False
        return True
        

    def __iter__(self):
        """
        Iterate through rectangle corners
        """
        yield self.corner_bot_l
        yield self.corner_top_l
        yield self.corner_top_r
        yield self.corner_bot_r

    def __repr__(self):
        return "R = (({}, {}), w={}, h={},r={})".format(self.origin[0], self.origin[1], self.width, self.height,self.rotated)