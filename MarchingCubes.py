from copy import copy
from Point import Point
from Rect import Rect
from Configuration import Configuration
import matplotlib.pyplot as plt

from plotting import draw_configuration

DIRECTIONS = [(0,-1),(1,0),(0,1),(-1,0)]

def flatten(t):
    return [item for sublist in t for item in sublist]


def main() -> None:
    container_size = 10
    rects = [
        Rect(Point(0,0),2,2),
        Rect(Point(2,0),3,1),
        Rect(Point(1,2),1,1),
        Rect(Point(2,1),1,3),
        Rect(Point(3,1),2,2),
        Rect(Point(5,0),1,9)
    ]
    concave_corners = get_outer_corners(container_size, rects)

    C = Configuration(packed_rects=rects, concave_corners=concave_corners, remaining_rect_dims=[], container_height=container_size, container_width=container_size)
    
    _, _ = draw_configuration(C)
    plt.show()

def get_outer_corners(container_size: int, rects: list[Rect]) -> list[Point]:
    '''
    A function that takes a list of rects that allign in the way outlined in the bin packing problem
    and returns a list of all the concave corners in polygon given as points 
    
    Parameters
    ----------
    container_size: int, required
        The width and height of the container the rects lie in
    
    rects: list[Rect], required
        A list of rect objects that are all connected
    '''

    # Start at the point that is closest to (0,0)
    starting_point = min([rect.origin for rect in rects])
    current_point = copy(starting_point)

    all_points = list(set(flatten([x.corners() for x in rects])))
    edge_points = []
    offsets = []

    offset = 0
    
    while True:
        
        # Try moving in the directions given in DIRECTIONS
        for i in range(4):
            base_point = copy(current_point)
            done = False

            # Continue moving the direction for max the container size
            for _ in range(container_size):
                base_point.move(DIRECTIONS[offset % 4])
                
                # No need to keep moving that direction if we are out of bounds
                if base_point.x < 0 or container_size < base_point.x or base_point.y < 0 or container_size < base_point.y:
                    break 

                # If we hit a point break the loop and update the current point and corresponding offset for concave corners calculation
                if base_point in all_points:
                    print("----",offset, base_point)
                    offsets.append(offset)
                    edge_points.append(base_point)
                    current_point = base_point
                    offset -= 1
                    done = True
                    break
            if done:
                break
            offset += 1

        # Break the loop whenever we get back to our starting point
        if current_point == starting_point:
            break

    # Calculate which edge points are concave corners using the offset
    concave_corners = []
    n = len(edge_points)
    for i in range(n-1):
        if (offsets[i-1] < offsets[i] and offsets[i+1] < offsets[i]):
            concave_corners.append(edge_points[i])
        # elif edge_points[i].x == 0 or edge_points[i].y == 0:
        #     concave_corners.append(edge_points[i])

    return concave_corners



if __name__ == "__main__":
    main()






