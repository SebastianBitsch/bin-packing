from copy import copy
from enum import Enum
from tracemalloc import start
from Point import Point, PointType
from Rect import Rect
from Configuration import Configuration

from plotting import draw_configuration

#DIR_FLOW = ['RIGHT','UP','LEFT','DOWN']
# class DIRECTIONS(Enum):
#     RIGHT = (1,0)
#     UP = (0,1)
#     LEFT = (-1,0)
#     DOWN = (0,-1)

DIRECTIONS = [(1,0),(0,1),(-1,0),(0,-1)]

def flatten(t):
    return [item for sublist in t for item in sublist]



def main() -> None:
    rects = [
        Rect(Point(0,0),2,2),
        Rect(Point(2,0),3,1),
        Rect(Point(1,2),1,1),
        Rect(Point(2,1),1,3)
    ]
    get_outer_corners(rects)

def get_outer_corners(rects: list[Rect]) -> list[Point]:
    
    starting_point = min([rect.origin for rect in rects])
    current_point = copy(starting_point)

    all_points = list(set(flatten([x.corners() for x in rects])))
    edge_points = [starting_point]

    direction = 0
    current_point.move(DIRECTIONS[direction])
    
    while current_point != starting_point:
        print(current_point)
        
        direction -= 1

        for dir in range(direction, direction+3):
            base_point = copy(current_point)
            done = False

            for _ in range(10):
                base_point.move(DIRECTIONS[dir])
                print(base_point)
                if base_point in all_points:
                    edge_points.append(base_point)
                    done = True
                    break
            if done:
                break

        break

        
        

if __name__ == "__main__":
    main()






