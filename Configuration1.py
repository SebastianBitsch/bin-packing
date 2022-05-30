from Rect import Rect
from Point import Point

class Configuration:

    def __init__(self, size: Point, rects: list[Rect] = []) -> None:
        self.rects = rects
        self.size = size

    def contains(self, point: Point) -> bool:
        if point.x <= 0 or point.y <= 0 or self.size.x <= point.x or self.size.y <= point.y:
            return True
        
        for r in self.rects:
            if r.contains(point):
                return True
        return False
