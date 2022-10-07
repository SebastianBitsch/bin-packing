
class Node():
    def __init__(self, origin:tuple, size:tuple) -> None:

        self.used = False        
        self.down = None
        self.right = None

        self.origin = origin
        self.x, self.y = origin
        self.w, self.h = size

    def __repr__(self) -> str:
        return f"Node(size: {self.w, self.h}, origin: {self.origin})"


class Rect():
    def __init__(self, size:tuple) -> None:
        assert len(size) == 2
        self.w, self.h = size
        self.fit = None
        self.inbounds = True

    def __repr__(self) -> str:
        return f"Rect(size: {self.w, self.h}, fit: {self.fit}, in bounds: {self.inbounds})"
