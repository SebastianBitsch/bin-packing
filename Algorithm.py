from copy import deepcopy
from Point import Point, PointType
from Rect import Rect
from Configuration1 import Configuration
from plotting import draw_configuration
import matplotlib.pyplot as plt
import TestCases 

import cProfile

eps = 0.001


frame_time = 0.02
test_set = deepcopy(TestCases.cat1_p3)


def plot(C: Configuration, rects: list = [], waittime: float = 0.0):
    """
    Helper function for passing the configuration to the plotter for plotting/animation
    """
    _, _ = draw_configuration(C, test_set, rects)
    plt.show(block=False)
    plt.pause(frame_time + waittime)
    plt.close()


def generate_L(C: Configuration, remaining_rects: list[tuple]) -> list[Rect]:
    """
    A function that takes the current configuration, all the remaining rects and returns all
    possible CCOAs that can be fitted to the configuration

    Parameters
    ----------
    C: Configuration, required
        The current configuration
    
    remaining_rects: list[tuple], required:
        The dimensions of the rects yet to be packed. On the format: (w,h)
    """
    # 1. concave corners
    concave_corners = get_concave_corners(C)

    # 2. generate ccoas for every rect
    ccoas: list[Rect] = []
    for x, y in remaining_rects:
        for corner, type in concave_corners:
            for rotated in [False, True]:
                ccoa = Rect(corner, x, y, type, rotated)

                # 3. Add if it fits
                if not C.fits(ccoa):
                    continue
                ccoas.append(ccoa)

    return ccoas

        
def argmax(lst):
    return lst.index(max(lst))

def degree(i:Rect, C: Configuration) -> float:
    """
    
    """

    d_mins = [i.min_distance(m) for m in C.rects]
    
    # Add the distances to the borders
    d_mins += [i.bottom, i.left, C.size.y - i.top, C.size.x - i.right]

    # Remove two smallest elements, which will be 0 - the two imediate neighbours
    assert(min(d_mins) == 0)
    d_mins.remove(min(d_mins))
    assert(min(d_mins) == 0)
    d_mins.remove(min(d_mins))

    return 1 - (min(d_mins) /((i.width + i.height)/2))


def get_concave_corners(C: Configuration) -> list[tuple[Point,PointType]]:
    concave_corners: list[tuple(Point,PointType)] = []

    for corner in C.get_all_corners():
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
        rects = remove_rect(L[best].width, L[best].height, rects)
        L = generate_L(C, rects)

        plot(C, rects)

    return C

def remove_rect(w, h, r) -> list[Rect]:
    if (w,h) in r:
        r.remove((w,h))
    elif (h,w) in r:
        r.remove((h,w))
    return r

def BenefitA1(ccoa: Rect, Cx: Configuration, Lx: list[Rect], rectsx: list[Rect]):

    Cx.place_rect(ccoa)
    rectsx = remove_rect(ccoa.width,ccoa.height, rectsx)
    plot(Cx, rectsx)

    Lx = generate_L(Cx, rectsx)

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
            d = BenefitA1(ccoa, deepcopy(C), deepcopy(L), deepcopy(rects))
            if type(d) is Configuration:
                print("Found successful configuration")
                return d
            else:
                if max_benefit < d:
                    max_benefit = d
                    max_benefit_ccoa = ccoa

        print(f"Placed {max_benefit_ccoa}, {len(rects)} rects remaining")
        C.place_rect(max_benefit_ccoa)
        rects = remove_rect(max_benefit_ccoa.width, max_benefit_ccoa.height, rects)
        
        L = generate_L(C, rects)
        plot(C,rects)

    print("Stopped with failure")
    print(f"Rects remaining: {rects}")
    return C


if __name__ == "__main__":
    size = Point(20,20)

    C = Configuration(size=size, max_rects=TestCases.cat1_p3)
    plot(C, waittime=4)

    # cProfile.run('C = A1(container_size = size, rects = tests.cat1_p1)', sort="time")
    C = A1(container_size = size, rects = TestCases.cat1_p3)

    plot(C, waittime=20)

