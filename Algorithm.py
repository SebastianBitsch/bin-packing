from Point import Point, PointType
from Rect import Rect
from Configuration1 import Configuration

eps = 0.001

rects = [
    (1,1)
]

def generate_L(C: Configuration):
    # 1. concave corners
    c = get_concave_corners(C)
    print(c)
    # 2. generate ccoas
    for d in rects:
        pass


    pass


def get_concave_corners(C: Configuration):
    concave_corners: list[tuple(Point,PointType)] = []

    # Check the 4 vertices of all packed rects, not the most optimal - alot of duplicate verts
    for rect in C.rects:
        for corner in rect:
            corner_type = get_corner_type(C, corner)
            if corner_type:
                concave_corners.append((corner,corner_type))

    # Check the four container corners
    for corner in [Point(0,0), Point(0,C.size.y), Point(C.size.x,0), C.size]:
        corner_type = get_corner_type(C, corner)
        if corner_type:
            concave_corners.append((corner,corner_type))

    return concave_corners


def get_corner_type(C: Configuration, p: Point) -> bool:
    checks = check_boundaries(C, p)
    if sum(checks) == 3:
        index = [i for i, x in enumerate(checks) if not x][0]
        return PointType(index)
    return None


def check_boundaries(C: Configuration, p: Point):
    return [
        C.contains(Point(p.x+eps, p.y+eps)),
        C.contains(Point(p.x-eps, p.y+eps)),
        C.contains(Point(p.x+eps, p.y-eps)),
        C.contains(Point(p.x-eps, p.y-eps))
    ]


def A0():
    pass

if __name__ == "__main__":
    
    C = Configuration(size=Point(10,10), rects=[])
    ccoas = generate_L(C)
