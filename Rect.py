from math import sqrt
from Point import Point, PointType

class Rect:

    def __init__(self, origin: Point, width, height, origin_type: PointType = PointType.BOTTOM_LEFT, rotated:bool = False) -> None:
        
        assert(0 < width and 0 < height)

        if rotated:
            temp = height
            height = width
            width = temp

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


    def area(self) -> int:
        return self.width * self.height

    # @property
    # def bottom(self):
    #     """
    #     Rectangle bottom edge y coordinate
    #     """
    #     return self.origin.y

    # @property
    # def top(self):
    #     """
    #     Rectangle top edge y coordiante
    #     """
    #     return self.origin.y+self.height

    # @property
    # def left(self):
    #     """
    #     Rectangle left ednge x coordinate
    #     """
    #     return self.origin.x

    # @property
    # def right(self):
    #     """
    #     Rectangle right edge x coordinate
    #     """
    #     return self.origin.x+self.width

    # @property
    # def corner_bot_l(self):
    #     return Point(self.left, self.bottom)

    # @property
    # def corner_top_l(self):
    #     return Point(self.left, self.top)

    # @property
    # def corner_top_r(self):
    #     return Point(self.right, self.top)

    # @property
    # def corner_bot_r(self):
    #     return Point(self.right, self.bottom)

    def move(self, point):
        self.origin = point

    def contains(self, point: Point) -> bool:
        return self.corner_bot_l.x <= point.x and self.corner_bot_l.y <= point.y and point.x <= self.corner_top_r.x and point.y <= self.corner_top_r.y

    def rotate(self):
        temp = self.width
        self.width = self.height
        self.height = temp

    def min_distance(self, other) -> float:
        outer_left = min(self.left, other.left)
        outer_right = max(self.right, other.right)
        outer_bottom = min(self.bottom, other.bottom)
        outer_top = max(self.top, other.top)

        # outer_left = min(self.corner_bot_l.x, other.corner_bot_l.x)
        # outer_right = max(self.corner_bot_r.x, other.corner_bot_r.x)
        # outer_bottom = min(self.corner_bot_l.y, other.corner_bot_l.y)
        # outer_top = max(self.corner_top_l.y, other.corner_top_l.y)

        outer_width = outer_right - outer_left
        outer_height = outer_top - outer_bottom

        inner_width = max(0, outer_width - self.width - other.width)
        inner_height = max(0, outer_height - self.height - other.height)

        # TODO: Might be able to remove a sqrt here, not sure
        return sqrt(inner_width**2 + inner_height**2)


    def overlaps(self, other) -> bool:
        if self.right <= other.left or other.right <= self.left:
            return False
        if self.top <= other.bottom or other.top <= self.bottom:
            return False
        return True
        # if self.corner_bot_r.x <= other.corner_bot_l.x or other.corner_bot_r.x <= self.corner_bot_l.x:
        #     return False
        # if self.corner_top_l.y <= other.corner_bot_l.y or other.corner_top_l.y <= self.corner_bot_l.y:
        #     return False
        # return True

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