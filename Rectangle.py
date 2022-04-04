
class Rect:
    def __init__(self, id: int, width: int, height: int) -> None:
        self.id = id
        self.width = width
        self.height = height

    def rotate(self):
        temp = self.width
        self.width = self.height
        self.height = temp

    def area(self):
        return self.width * self.height

    def __repr__(self) -> str:
        return "Rect(id={}, w={}, h={})".format(self.id, self.width, self.height)