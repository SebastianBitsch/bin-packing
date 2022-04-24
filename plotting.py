import matplotlib.pyplot as plt
from Rect import Rect
from Configuration import Configuration
from matplotlib.patches import Rectangle

def draw_configuration(configuration:Configuration, background_color='lightblue', edge_color='black',alpha=0.5):

    fig, ax = plt.subplots(1,figsize=(6,6))

    plt.xlim([0,configuration.container_height])
    plt.ylim([0,configuration.container_width])

    for rect in configuration.packed_rects:
        draw_rect(ax, rect,background_color,edge_color, alpha)
    
    return fig, ax

def draw_rect(ax, rect:Rect, background_color, edge_color, alpha):
    box = Rectangle(rect.origin.tuple(), rect.width, rect.height, fc=background_color,ec=edge_color,alpha=alpha)
    ax.add_patch(box)