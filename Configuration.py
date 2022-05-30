from copy import copy
from Point import Point, PointType
from Rect import Rect

class Configuration:

    def __init__(self, packed_rects: list[Rect], concave_corners: list[tuple[Rect, PointType]], remaining_rect_dims: list[tuple[int,int]], container_width: int, container_height: int) -> None:
        self.packed_rects = packed_rects
        self.concave_corners = concave_corners
        self.remaining_rect_dims = remaining_rect_dims

        self.container_width = container_width
        self.container_height = container_height

    def density(self) -> float:
        total_area = self.container_height * self.container_width
        occupied_area = sum([x.area() for x in self.packed_rects])
        return occupied_area/total_area

    def contains(self, point:Point) -> bool:
        if point.x <= 0 or point.y <= 0 or self.container_width <= point.x or self.container_height <= point.y:
            return True
        for p in self.packed_rects:
            if p.contains(point):
                return True
        return False

    def rect_placement_valid(self, rect: Rect) -> bool:
        """
        Returns true if the input rect doesnt overlap any of the rects in the configuration
        """
        return all([rect.overlaps(x) for x in self.packed_rects])


    def place_rect(self, rect: Rect) -> None:
        self.packed_rects.append(rect)
        self.remaining_rect_dims.remove((rect.width,rect.height))

        overlapping_corners = []
        new_corners = []

        # Find the corner(s) that the new rect and existing rects share
        for corner in iter(rect):
            for point, type in self.concave_corners:
                if not corner == point:
                    continue
                overlapping_corners.append((point,type))
                # Add the new corners
                self.concave_corners.remove((point,type))
        
        for corner, type in overlapping_corners:
            if type == PointType.BOTTOM_LEFT:
                new_corners.append((rect.corner_bot_r,PointType.BOTTOM_RIGHT))
                new_corners.append((rect.corner_top_l,PointType.TOP_LEFT))
            if type == PointType.TOP_LEFT:
                new_corners.append((rect.corner_bot_l,PointType.BOTTOM_LEFT))
                new_corners.append((rect.corner_top_r,PointType.TOP_RIGHT))
            elif type == PointType.TOP_RIGHT:
                new_corners.append((rect.corner_bot_r,PointType.BOTTOM_RIGHT))
                new_corners.append((rect.corner_top_l,PointType.TOP_LEFT))
            elif type == PointType.BOTTOM_RIGHT:
                new_corners.append((rect.corner_bot_l,PointType.BOTTOM_LEFT))
                new_corners.append((rect.corner_top_r,PointType.TOP_RIGHT))

        for corner, _ in new_corners:
            for point, _ in self.concave_corners:
                if corner == point:
                    new_corners.remove((corner,type))

        self.concave_corners.extend(new_corners)


    def valid_origins_for_rect(self, rect: Rect) -> list[Point]:
        origins = []
        for point, type in self.concave_corners:
            p = copy(point)

            if type == PointType.TOP_LEFT:
                p.shift(0,-rect.height)

            elif type == PointType.TOP_RIGHT:
                p.shift(-rect.width,-rect.height)

            elif type == PointType.BOTTOM_RIGHT:
                p.shift(-rect.width,0)

            if self.rect_placement_valid(Rect(p,rect.width,rect.height,rect.rotated)):
                origins.append(p)
        
        return origins