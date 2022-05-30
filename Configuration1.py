from Rect import Rect
from Point import Point

class Configuration:

    def __init__(self, size: Point, max_rects: int, rects: list[Rect] = []) -> None:
        self.size = size
        self.max_rects = max_rects
        self.rects = rects

    def contains(self, point: Point) -> bool:
        if point.x <= 0 or point.y <= 0 or self.size.x <= point.x or self.size.y <= point.y:
            return True
        
        for r in self.rects:
            if r.contains(point):
                return True
        return False

    def fits(self, ccoa: Rect):
        if ccoa.origin.x < 0 or ccoa.origin.y < 0 or self.size.x < ccoa.origin.x + ccoa.width or self.size.y < ccoa.origin.y + ccoa.height:
            return False
        
        return sum([ccoa.overlaps(x) for x in self.rects]) == 0

    def place_rect(self, rect: Rect) -> None:
        self.rects.append(rect)

    def density(self) -> float:
        total_area = self.size.x * self.size.y
        occupied_area = sum([x.area() for x in self.rects])
        return occupied_area/total_area


    def is_successful(self) -> bool:
        return len(self.rects) == self.max_rects