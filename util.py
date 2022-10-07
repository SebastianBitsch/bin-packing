from enum import Enum
from copy import copy
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class PointType(Enum):
    BOTTOM_LEFT = 0
    BOTTOM_RIGHT = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3

# Plot settings
figsize = (12,6)
placed_rect_color = 'lightblue'
unplaced_rect_color = 'grey'
ghost_rect_color = 'lightgrey'
edge_color = 'black'
alpha = 0.5

# Time settings
frametime = 0.02
starttime = 1
endtime = 10

all_rects = []
max_width = 0


def argmax(lst):
    return lst.index(max(lst))

def initialize_plot(C, rects = None, frame_time: float = 0.02, start_time: float = 4, end_time: float = 20, fig_size = (12,6)):
    global frametime, starttime, endtime
    global figsize, max_width
    global all_rects

    frametime = frame_time
    starttime = start_time
    endtime = end_time
    figsize = fig_size
    
    # Used for showing custom rects when late initializing plot
    if rects == None:
        all_rects = copy(C.unpacked_rects)
    else:
        all_rects = rects
    max_width = sum([r[0] for r in rects]) + 1 + len(rects)#TODO: Find better way of doing this


def plot_configuration(C, last_frame: bool):
    _, axs = plt.subplots(nrows=1, ncols=2,figsize=(12,6))

    # TODO: Find way to set this in init instead of every time plot is updated
    # Set the ticks for the main plot
    axs[0].set_xlim([0,C.size[0]])
    axs[0].set_ylim([0,C.size[1]])
    axs[0].set_xticks(range(0, C.size[0]+1, 5))
    axs[0].set_yticks(range(0, C.size[1]+1, 5))
    
    # Hide ticks for secondary ploty
    axs[1].set_xticks([])
    axs[1].set_yticks([])
    axs[1].set_xlim([0,max_width])
    axs[1].set_ylim([0,max_width])


    # Draw the placed rects in main plot
    for rect in C.packed_rects:
        draw_rect(axs[0], rect.origin, rect.width, rect.height, placed_rect_color, edge_color, alpha)
    
    # Draw the possible ccoas main plot
    for rect in C.L:
        draw_rect(axs[0], rect.origin, rect.width, rect.height, ghost_rect_color, edge_color, 0.05)
    
    draw_points(axs[0], C.concave_corners)

    # Draw secondary plot
    draw_rects_overview(axs[1], all_rects, C.unpacked_rects)
    
    
    final_time = endtime if last_frame else 0
    plt.show(block=False)
    plt.pause(frametime + final_time)
    plt.close()


def draw_points(ax, corners: list[tuple], color='red', marker='x'):
    """
    Plot points given on the format [Point, Pointtype]
    """
    x = [i[0][0] for i in corners]
    y = [i[0][1] for i in corners]
    ax.scatter(x, y, c=color, marker=marker)


def draw_rects_overview(ax, all_rects: list, unplaced_rects: list):
    tallest = 0
    current_pos = (1,1)

    for w,h in all_rects:
        unplaced: bool = ((w,h) or (h,w)) in unplaced_rects
        color = unplaced_rect_color if unplaced else placed_rect_color
        tallest = max(tallest, h)
        
        draw_rect(ax, current_pos, w, h, background_color=color, edge_color=edge_color,alpha=alpha)
     
        current_pos = (current_pos[0] + w + 1, current_pos[1])
        
        if max_width < current_pos[0] + w + 1:
            current_pos = (1, current_pos[1] + tallest + 1)
            tallest = 0


def draw_rect(ax, origin, w, h, background_color, edge_color, alpha):
    box = Rectangle(origin, w, h, fc=background_color,ec=edge_color,alpha=alpha)
    ax.add_patch(box)

