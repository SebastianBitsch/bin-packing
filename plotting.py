import matplotlib.pyplot as plt
import numpy as np
from Point import Point

from Rect import Rect
from Configuration1 import Configuration
from matplotlib.patches import Rectangle

def draw_configuration(configuration:Configuration, corners: list[Point] = [], background_color='lightblue', edge_color='black',alpha=0.5):

    fig, ax = plt.subplots(1,figsize=(6,6))
    plt.locator_params(axis="both", integer=True, tight=True)
    plt.xlim([0,configuration.size.x])
    plt.ylim([0,configuration.size.y])

    for rect in configuration.rects:
        draw_rect(ax, rect,background_color,edge_color, alpha)

    draw_points(ax, corners)

    return fig, ax

def draw_points(ax, corners: list[Point], color='red', marker='x'):
    x = [i.x for i in corners]
    y = [i.y for i in corners]
    ax.scatter(x, y, c=color, marker=marker)


def draw_rect(ax, rect:Rect, background_color, edge_color, alpha):
    box = Rectangle(rect.origin.tuple(), rect.width, rect.height, fc=background_color,ec=edge_color,alpha=alpha)
    ax.add_patch(box)
