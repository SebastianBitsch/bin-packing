from copy import copy
from Point import Point
from Rect import Rect
from Configuration import Configuration
import matplotlib.pyplot as plt

from plotting import draw_configuration

DIRECTIONS = [(0,-1),(1,0),(0,1),(-1,0)]

## === Doesnt work for disjoint sets of rects === 

def flatten(t):
    return [item for sublist in t for item in sublist]


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
        # Rect(Point(9,8),1,2),
    ]

    concave_corners = get_free_corners(container_size, rects)

    C = Configuration(packed_rects=rects, concave_corners=concave_corners, remaining_rect_dims=[], container_height=container_size, container_width=container_size)
    
    _, _ = draw_configuration(C)
    plt.show()


def get_free_corners(container_size: int, rects: list[Rect]) -> list[Point]:
    """
    """
    starting_point = Point(0,0)

    edge_points = get_outside_corners(container_size, rects, starting_point)
    concave_corners = get_concave_corners(container_size, edge_points)
    concave_corners_w_corners = add_free_corner_points(container_size, concave_corners)

    return concave_corners_w_corners


def get_outside_corners(container_size: int, rects: list[Rect], starting_point) -> list[Point]:
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
    current_point = copy(starting_point)

    all_points = list(set(flatten([x.corners() for x in rects])))
    edge_points = []
    offsets = []

    offset = 0
    
    while True:
        
        # Try moving in the directions given in DIRECTIONS
        for _ in range(4):
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

    return edge_points

def get_concave_corners(container_size: int, edge_points: list[Point]) -> list[Point]:
    """
    A function that given a list of points moving counter clockwise, will find and return a
    list of the points which are concave. Uses the determinant as described in:
    https://stackoverflow.com/questions/40410743/polygon-triangulation-reflex-vertex
    Will also return points that are concave in respect to the axis, but exclude the container corners

    Parameters
    ----------
    container_size: int, required
        The width and height of the container the rects lie in
    
    edge_points: list[Point], required
        A list of outside points as outputted from the get_outside_corners() method.
    """

    concave_corners = []
    n = len(edge_points)

    for i in range(0,n):
        a = edge_points[i-1]
        b = edge_points[i]
        c = edge_points[(i+1)%n]

        # Exclude the container corners
        if (b.x,b.y) in [(0,0),(0,container_size),(container_size,0),(container_size,container_size)]:
            continue

        # Calculate the determinant
        det = (b.x - a.x) * (c.y - b.y) - (c.x - b.x) * (b.y - a.y)

        # Points are concave if the determinant is smaller than 0, or if it borders the axis
        if det < 0 or (det != 0 and (b.x == 0 or b.y == 0)):
            concave_corners.append(edge_points[i])
    
    return concave_corners


# Add the container corners that are not already filled, TODO: Quite unelegant way of doing this, but works fine
def add_free_corner_points(container_size: int, points: list[Point]) -> list[Point]:
    
    corners = [Point(0,0),Point(0,container_size),Point(container_size,0),Point(container_size,container_size)]
    for i,(x,y) in enumerate([(0,0),(0,container_size),(container_size,0),(container_size,container_size)]):
        for point in points:
            if point == Point(x,y):
                del corners[i]
                break
    
    points.extend(corners)
    return points

if __name__ == "__main__":
    example_usage()



