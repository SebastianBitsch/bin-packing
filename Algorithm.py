from cmath import rect
from copy import copy
from Point import Point, PointType
from Rect import Rect
from Configuration1 import Configuration
from plotting import draw_configuration
import matplotlib.pyplot as plt

eps = 0.001


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
        
        # _, _ = draw_configuration(C)
        # plt.show()
    return C

def BenefitA1(ccoa: Rect, C: Configuration, L: list[Rect], rects: list[Rect]):
    Cx = copy(C)
    Lx = copy(L)
    rectsx = copy(rects)

    # Might be wrong
    Cx.place_rect(ccoa)
    rectsx.remove((ccoa.width,ccoa.height))
    Lx = generate_L(Cx, rectsx)
    if Cx.is_successful():
        return Cx
    elif len(Lx) == 0:
        return Cx.density()

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
                return C
            else:
                if max_benefit < d:
                    max_benefit = d
                    max_benefit_ccoa = ccoa
                # if 1.0 <= max_benefit:
                #     return None
        
        C.place_rect(max_benefit_ccoa)
        rects.remove(max_benefit_ccoa)
        L = generate_L(C, rects)

    return None



if __name__ == "__main__":
    rects = [
        (4,1),
        (2,2)
    ]

    C = A1(container_size = Point(5,4), rects = rects)

    if C:
        print("Found successful configuration")
        _, _ = draw_configuration(C)
        plt.show()
    else:
        print("Stopped with failure")

