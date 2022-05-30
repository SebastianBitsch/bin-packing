from math import sqrt
from Point import Point

class Rect:

    def __init__(self, origin: Point, width, height, rotated:bool = False) -> None:
        
        if rotated:
            temp = height
            height = width
            width = temp

        assert(0 < width and 0 < height)

        self.origin = origin
        self.width = width
        self.height = height
        self.rotated = rotated

    def area(self) -> int:
        return self.width * self.height

    def corners(self) -> list[Point]:
        return [p for p in self]

    @property
    def bottom(self):
        """
        Rectangle bottom edge y coordinate
        """
        return self.origin.y

    @property
    def top(self):
        """
        Rectangle top edge y coordiante
        """
        return self.origin.y+self.height

    @property
    def left(self):
        """
        Rectangle left ednge x coordinate
        """
        return self.origin.x

    @property
    def right(self):
        """
        Rectangle right edge x coordinate
        """
        return self.origin.x+self.width

    @property
    def corner_bot_l(self):
        return Point(self.left, self.bottom)

    @property
    def corner_top_l(self):
        return Point(self.left, self.top)

    @property
    def corner_top_r(self):
        return Point(self.right, self.top)

    @property
    def corner_bot_r(self):
        return Point(self.right, self.bottom)

    def move(self, point):
        self.origin = point

    # TODO: Mistakenly returns true for negative points
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

        outer_width = outer_right - outer_left
        outer_height = outer_top - outer_bottom

        inner_width = max(0, outer_width - self.width - other.width)
        inner_height = max(0, outer_height - self.height - other.height)

        return sqrt(inner_width^2 + inner_height^2)

    def overlaps(self, other) -> bool:
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