from Rect import Rect
from Point import Point

class Configuration:

    def __init__(self, size: Point, max_rects: int, rects: list[Rect] = []) -> None:
        self.size = size
        self.max_rects = max_rects
        self.rects = rects

    def contains(self, point: Point) -> bool:
        # Return true if point is out of bounds
        if point.x <= 0 or point.y <= 0 or self.size.x <= point.x or self.size.y <= point.y:
            return True
        
        # Check if any of the packed rects contain the point
        for r in self.rects:
            if r.contains(point):
                return True
        return False


    def fits(self, ccoa: Rect):
        # Check if the ccoa is out of bounds in any way
        if ccoa.origin.x < 0 or ccoa.origin.y < 0 or self.size.x < ccoa.origin.x + ccoa.width or self.size.y < ccoa.origin.y + ccoa.height:
            return False
        
        # Check if the rect overlaps any of the already packed rects
        for rect in self.rects:
            if ccoa.overlaps(rect):
                return False
        return True


    def place_rect(self, rect: Rect) -> None:
        self.rects.append(rect)


    def density(self) -> float:
        total_area = self.size.x * self.size.y
        occupied_area = sum([x.area() for x in self.rects])

        return occupied_area/total_area

    def get_all_corners(self) -> list[Point]:
        corners = [Point(0,0), Point(0,self.size.y), Point(self.size.x,0), self.size]
        for rect in self.rects:
            corners += [rect.corner_bot_l, rect.corner_bot_r, rect.corner_top_l, rect.corner_top_r]
        return list(set(corners))

    def is_successful(self) -> bool:
        return len(self.rects) == self.max_rects