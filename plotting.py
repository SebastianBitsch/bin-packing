import matplotlib.pyplot as plt
import numpy as np
from Point import Point

from Rect import Rect
from Configuration1 import Configuration
from matplotlib.patches import Rectangle

def draw_configuration(C: Configuration, unplaced_rects: list[Rect], corners: list[Point] = [], background_color='lightblue', edge_color='black',alpha=0.5):
    
    fig, axs = plt.subplots(nrows=1, ncols=2,figsize=(12,6))
    
    # Set the ticks for the main plot
    axs[0].set_xlim([0,C.size.x])
    axs[0].set_ylim([0,C.size.y])
    axs[0].set_xticks(range(0, C.size.x+1, 5))
    axs[0].set_yticks(range(0, C.size.y+1, 5))
    
    # Hide ticks for secondary plot
    axs[1].set_xticks([])
    axs[1].set_yticks([])

    # Draw the rects in main plot
    for rect in C.rects:
        draw_rect(axs[0], rect,background_color,edge_color, alpha)

    draw_points(axs[0], corners)
    draw_unplaced_rects(axs[1], C, unplaced_rects)

    return fig, axs

def draw_points(ax, corners: list[Point], color='red', marker='x'):
    x = [i.x for i in corners]
    y = [i.y for i in corners]
    ax.scatter(x, y, c=color, marker=marker)


def draw_unplaced_rects(ax, C: Configuration, unplaced_rects: list[Rect]):

    max_width = max(C.size.x,C.size.y) * 2
    ax.set_xlim([0,max_width])
    ax.set_ylim([0,max_width])

    tallest = 0
    current_pos = Point(1,1)

    for w,h in unplaced_rects:
   
        tallest = max(tallest, h)
        
        rect = Rect(origin=current_pos, width=w, height=h)
        draw_rect(ax, rect = rect, background_color='lightblue', edge_color='black',alpha=0.5)
     
        current_pos = Point(current_pos.x + w + 1, current_pos.y)
        
        if max_width < current_pos.x + w + 1:
            current_pos.x = 1
            current_pos.y += tallest + 1
            tallest = 0

def draw_rect(ax, rect:Rect, background_color, edge_color, alpha):
    box = Rectangle((rect.origin.x,rect.origin.y), rect.width, rect.height, fc=background_color,ec=edge_color,alpha=alpha)
    ax.add_patch(box)

if __name__ == "__main__":
    
    rects = [
        (7,5),
        (14,5),
        (14,8),
        (4,8),
        (21,13),
        (7,11),
        (14,11),
        (14,5),
        (4,5),
        (18,3),
        (21,3),
        (17,11),
        (4,11),
        (7,4),
        (5,4),
        (6,7),
        (18,5),
        (3,5),
        (7,3),
        (5,3),
        (18,4),
        (3,4),
        (12,2),
        (6,2),
        (18,5),
        (21,5),
        (17,3),
        (4,3)
    ]
    fig, ax = plt.subplots(1,figsize=(6,6))

    max_width = 60

    plt.xlim([0,max_width])
    plt.ylim([0,max_width])

    tallest = 0
    current_pos = Point(1,1)

    for w,h in rects:
   
        tallest = max(tallest, h)
        
        rect = Rect(origin=current_pos, width=w, height=h)
        draw_rect(ax, rect = rect, background_color='lightblue', edge_color='black',alpha=0.5)
     
        current_pos = Point(current_pos.x + w + 1, current_pos.y)
        
        if max_width < current_pos.x + w:
            current_pos.x = 1
            current_pos.y += tallest + 1
            tallest = 0



    plt.show()


