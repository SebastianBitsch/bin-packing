from copy import deepcopy
from Rect import Rect
from util import PointType, plot_configuration, initialize_plot

class Configuration:

    # The amount to look in each direction when determining if a corner is concave
    eps = 0.001

    def __init__(self, size: tuple, unpacked_rects: list, packed_rects: list[Rect] = [], enable_plotting: bool = False) -> None:
        self.size = size
        
        self.unpacked_rects = unpacked_rects
        self.packed_rects = packed_rects
        self.plotting = enable_plotting
        
        self.generate_L()

        if self.plotting:
            initialize_plot(self)
            

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def enable_plotting(self):
        self.plotting = False

    # TODO: Can be alot faster by taking the most recently placed rect as input - and only generating 
    #       new ccoas for points that are contained in the new rect
    def generate_L(self):
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
        self.concave_corners = self.get_concave_corners()

        # 2. generate ccoas for every rect
        ccoas: list[Rect] = []
        for x, y in self.unpacked_rects:
            for corner, type in self.concave_corners:
                for rotated in [False, True]:
                    ccoa = Rect(corner, x, y, type, rotated)

                    # 3. Add if it fits
                    if not self.fits(ccoa):
                        continue
                    ccoas.append(ccoa)

        self.L = ccoas

    def get_concave_corners(self) -> list[tuple[tuple,PointType]]:
        concave_corners: list[tuple(tuple,PointType)] = []

        for corner in self.get_all_corners():
            corner_type = self.get_corner_type(corner)
            if corner_type:
                concave_corners.append((corner,corner_type))

        return concave_corners

    def get_corner_type(self, p: tuple) -> bool:
        checks = self.check_boundaries(p)
        if sum(checks) == 3:
            index = [i for i, x in enumerate(checks) if not x][0]
            return PointType(index)
        return None

    def check_boundaries(self, p: tuple):
        return [
            self.contains((p[0]+self.eps, p[1]+self.eps)),
            self.contains((p[0]-self.eps, p[1]+self.eps)),
            self.contains((p[0]+self.eps, p[1]-self.eps)),
            self.contains((p[0]-self.eps, p[1]-self.eps))
        ]

    def contains(self, point: tuple) -> bool:
        # Return true if point is out of bounds
        if point[0] <= 0 or point[1] <= 0 or self.size[0] <= point[0] or self.size[1] <= point[1]:
            return True
        
        # Check if any of the packed rects contain the point
        for r in self.packed_rects:
            if r.contains(point):
                return True
        return False


    def fits(self, ccoa: Rect) -> bool:
        """
        Returns true if a given ccoa fits into the configuration without overlapping any of the rects
        or being out of bounds
        """
        # Check if the ccoa is out of bounds in any way
        if ccoa.origin[0] < 0 or ccoa.origin[1] < 0 or self.size[0] < ccoa.origin[0] + ccoa.width or self.size[1] < ccoa.origin[1] + ccoa.height:
            return False
        
        # Check if the rect overlaps any of the already packed rects
        for rect in self.packed_rects:
            if ccoa.overlaps(rect):
                return False
        return True


    def place_rect(self, rect: Rect) -> None:
        # Add rect to packed rects
        self.packed_rects.append(rect)

        # Remove the rect from unpacked rects
        if (rect.width,rect.height) in self.unpacked_rects:
            self.unpacked_rects.remove((rect.width,rect.height))
        elif (rect.height, rect.width) in self.unpacked_rects:
            self.unpacked_rects.remove((rect.height, rect.width))

        self.generate_L() # TODO: Do somehing like passing the just placed rect for more efficiency

        # Create plot
        if self.plotting:
            plot_configuration(self, self.is_successful())


    def density(self) -> float:
        """
        Return the percentage of total container area filled by packed rects
        """
        total_area = self.size[0] * self.size[1]
        occupied_area = sum([x.area for x in self.packed_rects])

        return occupied_area/total_area


    def get_all_corners(self) -> list[tuple]:
        """
        Returns a set of all unique points in the container
        """

        # The container corners
        corners = [(0,0), (0,self.size[1]), (self.size[0],0), self.size]

        # Get corners for every rect
        for rect in self.packed_rects:
            corners += [rect.corner_bot_l, rect.corner_bot_r, rect.corner_top_l, rect.corner_top_r]
        return list(set(corners))


    def is_successful(self) -> bool:
        return len(self.unpacked_rects) == 0