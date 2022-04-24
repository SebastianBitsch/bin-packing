from Point import Point, PointType
from Rect import Rect

class Configuration:

    def __init__(self, packed_rects: list[Rect], possible_points: list[tuple[Rect, PointType]], container_width: int, container_height: int) -> None:
        self.packed_rects = packed_rects
        self.possible_points = possible_points

        self.container_width = container_width
        self.container_height = container_height


    def place_rect(self, rect: Rect) -> None:
        self.packed_rects.append(rect)

    def possible_origins(self, rect: Rect) -> list[Point]:
        O = []
        for point, type in self.possible_points:
            if type == PointType.
                ## offset the points so the origins match the given rect