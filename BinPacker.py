from copy import deepcopy

from Rect import Rect
from Configuration import Configuration

from util import argmax


class BinPacker:

    def __init__(self, configuration: Configuration) -> None:
        self.C = configuration

    def _degree(self, i:Rect, C: Configuration) -> float:
        d_mins = [i.min_distance(m) for m in C.packed_rects]
        
        # Add the distances to the borders
        d_mins += [i.bottom, i.left, C.size[1] - i.top, C.size[0] - i.right]

        # Remove two smallest elements, which will be 0 - the two imediate neighbours
        assert(min(d_mins) == 0)
        d_mins.remove(min(d_mins))
        assert(min(d_mins) == 0)
        d_mins.remove(min(d_mins))

        return 1 - (min(d_mins) /((i.width + i.height)/2))


    def _A0(self, C: Configuration):
        while C.L:

            degrees = [self._degree(ccoa, C) for ccoa in C.L]
            best = argmax(degrees)

            C.place_rect(C.L[best])
        return C


    def _BenefitA1(self, ccoa: Rect, Cx: Configuration):

        Cx.place_rect(ccoa)

        Cx = self._A0(Cx)

        if Cx.is_successful():
            return Cx
        else:
            return Cx.density()


    def PackConfiguration(self, C: Configuration):
        """ The method called A1 in the paper """

        while C.L:
            max_benefit = 0
            max_benefit_ccoa = None
            
            for ccoa in C.L:
                d = self._BenefitA1(ccoa, deepcopy(C))
                if type(d) is Configuration:
                    print("Found successful configuration")
                    return d
                else:
                    if max_benefit < d:
                        max_benefit = d
                        max_benefit_ccoa = ccoa

            print(f"Placed {max_benefit_ccoa}, {len(C.unpacked_rects)} rects remaining")
            C.place_rect(max_benefit_ccoa)

        if C.is_successful():
            print("Found successful configuration")
        else:
            print("Stopped with failure")
            print(f"Rects remaining: {C.unpacked_rects}")
        return C

