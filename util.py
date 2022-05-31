from copy import copy
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from Point import Point
from Rect import Rect

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

def initialize_plot(C, frame_time: float = 0.02, start_time: float = 1, end_time: float = 10, fig_size = (12,6)):
    global frametime, starttime, endtime
    global figsize, max_width
    global all_rects

    frametime = frame_time
    starttime = start_time
    endtime = end_time
    figsize = fig_size
    max_width = len(C.unpacked_rects) * 2.2 #TODO: Find better way of doing this
    all_rects = copy(C.unpacked_rects)


def plot_configuration(C):
    _, axs = plt.subplots(nrows=1, ncols=2,figsize=(12,6))

    # TODO: Find way to set this in init instead of every time plot is updated
    # Set the ticks for the main plot
    axs[0].set_xlim([0,C.size.x])
    axs[0].set_ylim([0,C.size.y])
    axs[0].set_xticks(range(0, C.size.x+1, 5))
    axs[0].set_yticks(range(0, C.size.y+1, 5))
    
    # Hide ticks for secondary ploty
    axs[1].set_xticks([])
    axs[1].set_yticks([])
    axs[1].set_xlim([0,max_width])
    axs[1].set_ylim([0,max_width])


    # Draw the placed rects in main plot
    for rect in C.packed_rects:
        draw_rect(axs[0], rect, placed_rect_color, edge_color, alpha)
    
    # Draw the possible ccoas main plot
    for rect in C.L:
        draw_rect(axs[0], rect, ghost_rect_color, edge_color, 0.05)
    
    draw_points(axs[0], C.concave_corners)

    # Draw secondary plot
    draw_unplaced_rects(axs[1], all_rects, C.unpacked_rects)
    
    plt.show(block=False)
    plt.pause(frametime)
    plt.close()

def draw_points(ax, corners: list[tuple], color='red', marker='x'):
    x = [i[0].x for i in corners]
    y = [i[0].y for i in corners]
    ax.scatter(x, y, c=color, marker=marker)


def draw_unplaced_rects(ax, all_rects: list, unplaced_rects: list):

    tallest = 0
    current_pos = Point(1,1)

    for w,h in all_rects:
        unplaced: bool = (w,h) in unplaced_rects
        color = unplaced_rect_color if unplaced else placed_rect_color
        tallest = max(tallest, h)
        
        rect = Rect(origin=current_pos, width=w, height=h)
        draw_rect(ax, rect = rect, background_color=color, edge_color=edge_color,alpha=alpha)
     
        current_pos = Point(current_pos.x + w + 1, current_pos.y)
        
        if max_width < current_pos.x + w + 1:
            current_pos.x = 1
            current_pos.y += tallest + 1
            tallest = 0


def draw_rect(ax, rect:Rect, background_color, edge_color, alpha):
    box = Rectangle((rect.origin.x,rect.origin.y), rect.width, rect.height, fc=background_color,ec=edge_color,alpha=alpha)
    ax.add_patch(box)

