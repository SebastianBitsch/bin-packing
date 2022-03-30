from dataclasses import dataclass, field
import itertools
from functools import total_ordering

@total_ordering
@dataclass
class Box:
    width: int
    height: int
    origin: tuple[int, int] = (0,0)
    id: int = field(default_factory=itertools.count().__next__, init=False)

    def coords(self) -> list:
        return [
            self.origin, 
            (self.origin[0] + self.width, self.origin[1]), 
            (self.origin[0], self.origin[1] + self.height),
            (self.origin[0] + self.width, self.origin[1] + self.height)
        ]

    def area(self) -> int:
        return self.width * self.height

    def __eq__(self, other):
        return (self.width == other.width) and (self.height == other.height)

    def __lt__(self, other):
        return self.area() < other.area()