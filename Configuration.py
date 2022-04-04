from os import posix_spawn
from tty import CC
from Point import Point
from CCOA import CCOA

class Configuration:
    packed_rects: list[CCOA]
    succeded: bool = False
    failed: bool = False

    def num_rects_packed(self):
        return len(self.packed_rects)

    def __init__(self, packed_rects: list[CCOA]) -> None:
        self.packed_rects = packed_rects

    # def set_possible_actions(self, points: list[Point]) -> None:
    #     self.possible_actions = points

    def __eq__(self, other):
        pass
        # return (self.width == other.width) and (self.height == other.height)
