from copy import copy, deepcopy
import matplotlib.pyplot as plt
import cProfile

from Point import Point
from Rect import Rect
from Configuration1 import Configuration
from plotting import draw_configuration

import TestCases 

# The amount to look in each direction when determining if a corner is concave
eps = 0.001


frame_time = 0.02
test_set = deepcopy(TestCases.cat1_p3)

# class BinPacker:

#     def __init__(self, all_rects: list, container_size: Point, plot_process:bool = False) -> None:
#         self.all_rects = all_rects
#         self.size = container_size
    

def plot(C: Configuration, rects: list = [], waittime: float = 0.0):
    """
    Helper function for passing the configuration to the plotter for plotting/animation
    """
    _, _ = draw_configuration(C, test_set, rects)
    plt.show(block=False)
    plt.pause(frame_time + waittime)
    plt.close()


def argmax(lst):
    return lst.index(max(lst))

def degree(i:Rect, C: Configuration) -> float:
    """
    
    """

    d_mins = [i.min_distance(m) for m in C.packed_rects]
    
    # Add the distances to the borders
    d_mins += [i.bottom, i.left, C.size.y - i.top, C.size.x - i.right]

    # Remove two smallest elements, which will be 0 - the two imediate neighbours
    assert(min(d_mins) == 0)
    d_mins.remove(min(d_mins))
    assert(min(d_mins) == 0)
    d_mins.remove(min(d_mins))

    return 1 - (min(d_mins) /((i.width + i.height)/2))



# TODO: Make faster, gets called A LOT - cache some results
def A0(C: Configuration):
    while C.L:

        degrees = [degree(ccoa, C) for ccoa in C.L]
        best = argmax(degrees)

        C.place_rect(C.L[best])

    return C

def BenefitA1(ccoa: Rect, Cx: Configuration):

    Cx.place_rect(ccoa)

    Cx = A0(Cx)

    if Cx.is_successful():
        return Cx
    else:
        return Cx.density()

def A1(C: Configuration):

    while C.L:
        max_benefit = 0
        max_benefit_ccoa = None
        
        for ccoa in C.L:
            d = BenefitA1(ccoa, deepcopy(C))
            if type(d) is Configuration:
                print("Found successful configuration")
                return d
            else:
                if max_benefit < d:
                    max_benefit = d
                    max_benefit_ccoa = ccoa

        print(f"Placed {max_benefit_ccoa}, {len(C.unpacked_rects)} rects remaining")
        C.place_rect(max_benefit_ccoa)

    print("Stopped with failure")
    print(f"Rects remaining: {C.unpacked_rects}")
    return C


if __name__ == "__main__":
    size = Point(20,20)

    C = Configuration(size=size, all_rects= TestCases.cat3_p1)
    # plot(C, waittime=1)

    cProfile.run('C = A1(C)', sort="time")
    # C = A1(C)

    plot(C, waittime=20)

