from Point import Point, PointType
from Rect import Rect
from Configuration import Configuration
import matplotlib.pyplot as plt

from plotting import draw_configuration

eps = 0.001

def example_usage() -> None:
    container_size = 10
    rects = [
        Rect(Point(0,0),2,2),
        Rect(Point(1,2),1,1),
        Rect(Point(2,1),1,3),
        Rect(Point(3,1),2,2),
        Rect(Point(5,0),1,9),
        Rect(Point(6,0),3,3),
        Rect(Point(2,0),3,1),
        Rect(Point(0,2),1,5),
        Rect(Point(8,8),2,2),
        Rect(Point(7,8),1,2),
        Rect(Point(0,9),1,1),
        Rect(Point(0,7),1,2),
        Rect(Point(1,8),2,2)
    ]


    C = Configuration(packed_rects=rects, concave_corners=[], remaining_rect_dims=[], container_height=container_size, container_width=container_size)

    concave_corners = []
    for rect in rects:
        for corner in rect:
            corner_type = get_corner_type(C, corner)
            if corner_type:
                concave_corners.append(corner)
    
    C = Configuration(packed_rects=rects, concave_corners=concave_corners, remaining_rect_dims=[], container_height=container_size, container_width=container_size)

    _, _ = draw_configuration(C)
    plt.show()


def get_corner_type(C: Configuration, p: Point) -> bool:
    checks = check_boundaries(C, p)
    if sum(checks) != 3:
        return None
    index = [i for i, x in enumerate(checks) if not x][0]
    return PointType(index)


def check_boundaries(C: Configuration, p: Point):
    bot_l = C.contains(Point(p.x-eps, p.y-eps))
    bot_r = C.contains(Point(p.x+eps, p.y-eps))
    top_l = C.contains(Point(p.x-eps, p.y+eps))
    top_r = C.contains(Point(p.x+eps, p.y+eps))
    return [top_r, top_l, bot_r, bot_l]

if __name__ == "__main__":
    example_usage()