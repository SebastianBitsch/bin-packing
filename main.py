import cProfile
from copy import copy

from Configuration import Configuration
from BinPacker import BinPacker
import TestCases
from util import plot_configuration, initialize_plot

if __name__ == "__main__":

    # Parameters
    rects = TestCases.cat1_p1
    plotting = False
    container_size = (20,20)


    C = Configuration(size=container_size, unpacked_rects=copy(rects), enable_plotting=plotting)
    packer = BinPacker(C)

    # For profiling     
    cProfile.run('C = packer.A1(C)', sort="time")
    # C = packer.A1(C)

    # Show final configuration
    if not plotting:
        initialize_plot(C, rects)
        plot_configuration(C, last_frame=True)
    


