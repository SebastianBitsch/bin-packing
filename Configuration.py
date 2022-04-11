from Point import Point
from CCOA import CCOA
from Rectangle import Rect

class Configuration:
    packed_rects: list[CCOA]
    succeded: bool = False
    failed: bool = False

    def num_rects_packed(self):
        return len(self.packed_rects)

    def __init__(self, packed_rects: list[CCOA], possible_origins: list[Point]) -> None:
        self.packed_rects = packed_rects
        self.possible_origins = possible_origins

    def place_rect(self, rect: CCOA):
        self.packed_rects.append(rect)
        #rect.origin.type
        self.possible_origins.remove(rect.origin)

    # def set_possible_actions(self, points: list[Point]) -> None:
    #     self.possible_actions = points

    def __eq__(self, other):
        pass
        # return (self.width == other.width) and (self.height == other.height)

    def possible_ccoas_for_rect(self, rect: Rect) -> list[CCOA]:
        possible_ccoas = []
        for origin in self.possible_origins:
            for rotation in [True,False]:
                new_ccoa = CCOA(rect=rect, origin=origin, rotated=rotation)
                for other in self.packed_rects:
                    if not new_ccoa.collides(other):
                        possible_ccoas.append(new_ccoa)
        return possible_ccoas