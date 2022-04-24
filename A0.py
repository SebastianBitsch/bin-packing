from operator import itemgetter
import matplotlib.pyplot as plt

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
    degrees = []
    
    # Calculate the degrees
    for ccoa in L:
        d = degree(ccoa, C.packed_rects)
        degrees.append((d, ccoa))

    # Select the CCOA with the highest degree
    _, best_rect = max(degrees,key=itemgetter(0))
    C.place_rect(best_rect)


if __name__ == "__main__":
    # all_rects = [(1,2)]
    # C = Configuration(packed_rects=[Rect(Point(0,0),2,2)])

    # L = [
    #     Rect(Point(0,2),1,2),
    #     Rect(Point(2,0),1,2),
    #     Rect(Point(0,3),1,2),
    #     Rect(Point(4,0),1,2),
    #     Rect(Point(4,3),1,2),
    #     Rect(Point(0,2),1,2,True),
    #     Rect(Point(2,0),1,2,True),
    #     Rect(Point(0,4),1,2,True),
    #     Rect(Point(3,0),1,2,True),
    #     Rect(Point(3,4),1,2,True)
    # ]
    
    points = [
        (Point(0,0), PointType.BOTTOM_LEFT),
        (Point(container_width,0), PointType.BOTTOM_RIGHT),
        (Point(0,container_height), PointType.TOP_LEFT),
        (Point(container_width, container_height), PointType.TOP_RIGHT)
    ]

    C = Configuration(packed_rects=[], possible_points=points, container_width=container_width, container_height=container_height)

    # Generate all possible actions
    L = []
    dims = [(1,2)]
    for d in dims:
        x,y = d
        
    # L = [
    #     Rect(Point(0,0),1,2),
    #     Rect(Point(0,3),1,2),
    #     Rect(Point(4,1),1,2),
    #     Rect(Point(4,3),1,2),
    # ]

    # C = Configuration(packed_rects=L, container_width=container_width, container_height=container_height)

    # L = [
    #     Rect(Point(0,0),1,2),
    #     Rect(Point(0,3),1,2),
    #     Rect(Point(4,0),1,2),
    #     Rect(Point(4,3),1,2),
    #     Rect(Point(0,0),1,2,True),
    #     Rect(Point(0,4),1,2,True),
    #     Rect(Point(3,0),1,2,True),
    #     Rect(Point(3,4),1,2,True)
    # ]
    # a = Rect(Point(0,0),2,2)
    # b = Rect(Point(2,0),1,1)
    # print(a.min_distance(b))

    fig, ax = draw_configuration(C)
    
    plt.show()

    A0(C, L)
