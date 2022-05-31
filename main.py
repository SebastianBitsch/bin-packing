import cProfile

from Point import Point
from Configuration import Configuration
from BinPacker import BinPacker
import TestCases

if __name__ == "__main__":
    size = Point(20,20)

    C = Configuration(size=size, unpacked_rects=TestCases.cat1_p1, enable_plotting=True)
    packer = BinPacker(C)

    # For profiling     
    # cProfile.run('C = packer.A1(C)', sort="time")
    C = packer.A1(C)

