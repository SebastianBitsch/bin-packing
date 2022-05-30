from copy import copy, deepcopy
from Point import Point, PointType
from Rect import Rect
from Configuration1 import Configuration
from plotting import draw_configuration
import matplotlib.pyplot as plt

eps = 0.001
cat1_p1 = [
    (2,12),
    (7,12),
    (8,6),
    (3,6),
    (3,5),
    (5,5),
    (3,12),
    (3,7),
    (5,7),
    (2,6),
    (3,2),
    (4,2),
    (3,4),
    (4,4),
    (9,2),
    (11,2)
]
cat1_p2 = [
    (4,1),
    (4,5),
    (9,4),
    (3,5),
    (3,9),
    (1,4),
    (5,3),
    (4,1),
    (5,5),
    (7,2),
    (9,3),
    (3,13),
    (2,8),
    (15,4),
    (5,4),
    (10,6),
    (7,2)
]
cat1_p3 = [
    (4,14),
    (5,2),
    (2,2),
    (9,7),
    (5,5),
    (2,5),
    (7,7),
    (3,5),
    (6,5),
    (3,2),
    (6,2),
    (4,6),
    (6,3),
    (10,3),
    (6,3),
    (6,3),
    (10,3)
]

cat3_p1 = [
    (7,5),
    (14,5),
    (14,8),
    (4,8),
    (21,13),
    (7,11),
    (14,11),
    (14,5),
    (4,5),
    (18,3),
    (21,3),
    (17,11),
    (4,11),
    (7,4),
    (5,4),
    (6,7),
    (18,5),
    (3,5),
    (7,3),
    (5,3),
    (18,4),
    (3,4),
    (12,2),
    (6,2),
    (18,5),
    (21,5),
    (17,3),
    (4,3)
]

def generate_L(C: Configuration, remaining_rects: list[tuple]):
    # 1. concave corners
    concave_corners = get_concave_corners(C)

    # 2. generate ccoas for every rect
    ccoas = []
    for x, y in remaining_rects:
        for corner, type in concave_corners:
            ccoa = Rect(corner, x, y, type)
            if not C.fits(ccoa):
                continue
            ccoas.append(ccoa)

    return ccoas

        
def argmax(lst):
    return lst.index(max(lst))

def degree(i:Rect, C: Configuration) -> float:
    d_mins = [m.min_distance(i) for m in C.rects]
    
    # Add the distances to the borders
    d_mins.append(i.bottom)
    d_mins.append(i.left)
    d_mins.append(C.size.y - i.top)
    d_mins.append(C.size.x - i.right)

    # Remove two smallest elements, which will be 0 - the two imediate neighbours
    assert(min(d_mins) == 0)
    d_mins.remove(min(d_mins))
    assert(min(d_mins) == 0)
    d_mins.remove(min(d_mins))

    return 1 - (min(d_mins) /((i.width + i.height)/2))


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


def A0(C: Configuration, L: list[Rect], rects: list[Rect]):

    while 0 < len(L):

        degrees = [degree(ccoa, C) for ccoa in L]
        best = argmax(degrees)

        C.place_rect(L[best])
        rects.remove((L[best].width, L[best].height))

        L = generate_L(C, rects)
        
    return C

def BenefitA1(ccoa: Rect, C: Configuration, L: list[Rect], rects: list[Rect]):
    Cx = deepcopy(C)
    Lx = deepcopy(L)
    rectsx = deepcopy(rects)

    # Might be wrong
    Cx.place_rect(ccoa)
    rectsx.remove((ccoa.width,ccoa.height))
    Lx = generate_L(Cx, rectsx)

    # if Cx.is_successful():
    #     return Cx

    Cx = A0(Cx, Lx, rectsx)

    if Cx.is_successful():
        return Cx
    else:
        return Cx.density()

def A1(container_size: Point, rects: list[Rect]):
    
    C = Configuration(size=container_size, max_rects=len(rects))
    L = generate_L(C, rects)

    while 0 < len(L):
        max_benefit = 0
        max_benefit_ccoa = None

        for ccoa in L:
            d = BenefitA1(ccoa, C, L, rects)
            if type(d) is Configuration:
                return d
            else:
                if max_benefit < d:
                    max_benefit = d
                    max_benefit_ccoa = ccoa
        

        C.place_rect(max_benefit_ccoa)
        rects.remove((max_benefit_ccoa.width, max_benefit_ccoa.height))
        L = generate_L(C, rects)

        corners = get_concave_corners(C)
        corners = [x[0] for x in corners]
        _, _ = draw_configuration(C,corners)
        print(rects)
        plt.show()

    return None



if __name__ == "__main__":
    size = Point(60,30)

    C = A1(container_size = size, rects = cat3_p1)

    if C:
        print("Found successful configuration")
        
        _, _ = draw_configuration(C)
        plt.show()
    else:
        print("Stopped with failure")

