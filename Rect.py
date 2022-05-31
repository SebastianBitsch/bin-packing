from copy import deepcopy
from math import sqrt
from Point import Point, PointType

class Rect:

    def __init__(self, origin: Point, width, height, origin_type: PointType = PointType.BOTTOM_LEFT, rotated:bool = False) -> None:        
        assert(0 < width and 0 < height)

        if rotated:
            temp = height
            height = width
            width = temp

        # Shift origin to bottom left corner depending on what type of point was given
        if origin_type == PointType.BOTTOM_LEFT:
            self.origin = origin
        if origin_type == PointType.TOP_LEFT:
            self.origin = Point(origin.x, origin.y - height)
        if origin_type == PointType.BOTTOM_RIGHT:
            self.origin = Point(origin.x - width, origin.y)
        if origin_type == PointType.TOP_RIGHT:
            self.origin = Point(origin.x - width, origin.y - height)
        
        self.width = width
        self.height = height
        self.rotated = rotated

        self.bottom = self.origin.y
        self.top = self.origin.y+self.height
        self.left = self.origin.x
        self.right = self.origin.x+self.width

        self.corner_bot_l = Point(self.left, self.bottom)
        self.corner_top_l = Point(self.left, self.top)
        self.corner_top_r = Point(self.right, self.top)
        self.corner_bot_r = Point(self.right, self.bottom)


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


    def contains(self, point: Point) -> bool:
        return self.corner_bot_l.x <= point.x and self.corner_bot_l.y <= point.y and point.x <= self.corner_top_r.x and point.y <= self.corner_top_r.y


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
        return "R = (({}, {}), w={}, h={},r={})".format(self.origin.x, self.origin.y, self.width, self.height,self.rotated)