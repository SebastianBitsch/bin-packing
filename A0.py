from copy import copy
from operator import itemgetter

from Point import Point, PointType
from Rect import Rect
from Configuration import Configuration

from plotting import draw_configuration

container_width = 5
container_height = 5
    
def degree(i:Rect, M:list[Rect]) -> float:
    d_mins = [m.min_distance(i) for m in M]
    
    # Add the distances to the borders
    d_mins.append(i.bottom)
    d_mins.append(i.left)
    d_mins.append(container_height - i.top)
    d_mins.append(container_width - i.right)

    # Remove two smallest elements, which will be 0 - the two imediate neighbours
    assert(min(d_mins) == 0)
    d_mins.remove(min(d_mins))
    assert(min(d_mins) == 0)
    d_mins.remove(min(d_mins))

    return 1 - (min(d_mins) /((i.width + i.height)/2))


def A0(C: Configuration, L: list[Rect]):
    
    # Calculate the degrees
    degrees = [(degree(ccoa, C.packed_rects), ccoa) for ccoa in L]

    # Select the CCOA with the highest degree
    best_rect = max(degrees,key=itemgetter(0))[1]

    # Place the rect
    C.place_rect(best_rect)

    # Update L
    L = generate_possible_actions(C)

    return C, L

def benefitA1(rect: Rect, C: Configuration, L: list[Rect]):
    dC, dL = copy(C), copy(L)
    dC.place_rect(rect)
    dL = generate_possible_actions(dC)
    dC, dL = A0(dC, dL)

    if len(dC.remaining_rect_dims) == 0:
        return 1 # Successful
    else:
        return (dC.density(), rect)

def A1(C):

    # Generate all possible actions
    L = generate_possible_actions(C)

    while 0 < len(L):
        max_benefit = []
        for ccoa in L:
            d = benefitA1(ccoa, C, L)
            if d == 1:
                print("success")
                return
            else:
                max_benefit.append(d)
        
        # Select the Configuration with the highest degree
        best_rect = max(d,key=itemgetter(0))[1]
        C.place_rect(best_rect)
        L = generate_possible_actions(C)
        for l in L:
            print(l)



def generate_possible_actions(C: Configuration) -> list[Rect]:
    L = []
    for d in C.remaining_rect_dims:
        w,h = d
        origins = C.valid_origins_for_rect(Rect(Point(), w, h))
        rects = [Rect(o, w, h) for o in origins]
        L.extend(rects)
    return L

if __name__ == "__main__":

    dims = [(1,1)]

    initial_points = [
        (Point(0,0), PointType.BOTTOM_LEFT),
        (Point(container_width,0), PointType.BOTTOM_RIGHT),
        (Point(0,container_height), PointType.TOP_LEFT),
        (Point(container_width, container_height), PointType.TOP_RIGHT)
    ]

    C = Configuration(packed_rects=[], concave_corners=initial_points, remaining_rect_dims=dims, container_width=container_width, container_height=container_height)

    A1(C)
    # dims = [(1,1),(2,2)]

    # initial_points = [
    #     (Point(0,0), PointType.BOTTOM_LEFT),
    #     (Point(container_width,0), PointType.BOTTOM_RIGHT),
    #     (Point(0,container_height), PointType.TOP_LEFT),
    #     (Point(container_width, container_height), PointType.TOP_RIGHT)
    # ]

    # C = Configuration(packed_rects=[], concave_corners=initial_points, remaining_rect_dims=dims, container_width=container_width, container_height=container_height)

    # # Generate all possible actions
    # L = generate_possible_actions(C)
    # for l in L:
    #     print(l)
    # print("---")
    # # fig, ax = draw_configuration(C)
    # # plt.show()


    # C, L = A0(C, L)


