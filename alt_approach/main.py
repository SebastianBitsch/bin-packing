import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from TestCases import all_cases
from Packers import SimplePacker, AdvancedPacker
from Node import Rect


sort_types = {"width":0, "height":1, "max":2, "area":3}    

def sort(rects:list[tuple], sort_attr:str='width') -> list[tuple]:
    """ Function for sorting a list of rects using a given sorting method """

    if sort_attr == 'none':
        return rects

    # Add attributes to the rects to use for sorting parameters; 
    # r = (w, h, max(w,h), w*h)
    attr = [r + (max(r), r[0]*r[1]) for r in rects]
    
    # Get the index of the inputted sorting type, if invalid width is used (0=width)
    sort_attr_index = sort_types.get(sort_attr, 0)

    # Sort attributes and return only the original rect dims
    attr.sort(key=lambda x: x[sort_attr_index], reverse=True)
    return [x[:2] for x in attr]


def plot(rects:list[Rect], figsize:tuple=(7,7)) -> None:
    """ Plot a collection of rects """
    _, ax = plt.subplots(figsize=figsize)

    ax.set_xlim([0,rects[0].fit.w])
    ax.set_ylim([0,rects[0].fit.h])
    plt.locator_params(axis="both", integer=True, tight=True)

    for r in rects:
        if not r.fit:
            continue
        draw_rect(ax, r)

    plt.show()


def draw_rect(ax, rect: Rect) -> None:
    """ Draw a single rect object """
    box = Rectangle(rect.fit.origin, rect.w, rect.h, fc='lightblue',ec='black',alpha=1.0)
    ax.add_patch(box)


if __name__ == "__main__":
    
    dims = all_cases[2]
    size = (20, 20)

    dims = sort(dims, sort_attr="max")
    rects = [Rect(d) for d in dims]

    #p = SimplePacker(*size)
    p = AdvancedPacker(*size)
    
    rects = p.fit(rects, auto_bounds=True)
    plot(rects)

