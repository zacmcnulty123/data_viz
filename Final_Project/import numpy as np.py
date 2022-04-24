# Matplotlib for drawing the court
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import animation
from matplotlib.patches import Ellipse

INPUT_DIR = './Tennis_data'
def load_data():
    return [pd.read_csv(os.path.join(INPUT_DIR, file_), index_col=0) for file_ in os.listdir(INPUT_DIR)]
        
rallies, points, events, serves = load_data()

#### Tennis data

height_court = 10.97
width_court = 11.89*2
service_box = 6.4
double_field = 1.37
baseline_serviceline = 5.5
breite_einzel = 8.23
serviceline_net = 6.4


def draw_court(hide_axes=False):
    """Sets up field
    Returns matplotlib fig and axes objects.
    """
        
    fig = plt.figure(figsize=(height_court/2, width_court/2))
    #fig = plt.figure(figsize=(9, 9))
    fig.patch.set_facecolor('#5080B0')

    axes = fig.add_subplot(1, 1, 1, facecolor='#5080B0')

    if hide_axes:
        axes.xaxis.set_visible(False)
        axes.yaxis.set_visible(False)
        axes.axis('off')

    axes = draw_patches(axes)
    
    return fig, axes

def draw_patches(axes):
    plt.xlim([-2,height_court+2])
    plt.ylim([-6.5,width_court+6.5])
    
    #net
    axes.add_line(plt.Line2D([height_court, 0],[width_court/2, width_court/2],
                    c='w'))
    
    # court outline
    y = 0
    dy = width_court
    x = 0#height_court-double_field
    dx = height_court
    axes.add_patch(plt.Rectangle((x, y), dx, dy,
                       edgecolor="white", facecolor="#5581A6", alpha=1))
    # serving rect
    y = baseline_serviceline
    dy = serviceline_net*2
    x = 0 + double_field 
    dx = breite_einzel
    axes.add_patch(plt.Rectangle((x, y), dx, dy,
                       edgecolor="white", facecolor="none", alpha=1))
    
    #?
    #net
    axes.add_line(plt.Line2D([height_court/2, height_court/2], [width_court/2 - service_box, width_court/2 + service_box],
                    c='w'))
    
    axes.add_line(plt.Line2D([height_court/2, height_court/2], [0, 0 + 0.45], 
                    c='w'))

    axes.add_line(plt.Line2D([height_court/2, height_court/2], [width_court, width_court - 0.45], 
                c='w'))
    
    axes.add_line(plt.Line2D([1.37, 1.37], [0, width_court], 
            c='w'))
    
    axes.add_line(plt.Line2D( [height_court - 1.37, height_court - 1.37], [0, width_court],
        c='w'))

    return axes

def draw_players(player_1_x, player_1_y, player_2_x, player2_y):
    colors = {'djokovic': 'gray',
              'nadal': '#00529F'}
    
    size = 2
    color='white'
    edge=colors['djokovic']                        
    
    artist1 = Ellipse((player_1_x,
                             player_1_y),
                              size,size,
                              edgecolor=edge,
                              linewidth=2,
                              facecolor=color,
                              alpha=1,
                              zorder=20)
#     artist1.text(player_1_x-0.4,player_1_y-0.2,'Dj',fontsize=14, color='black', zorder=30)
                
    
    edge=colors['nadal']
    artist2 = Ellipse((player_2_x,
                             player2_y),
                              size,size, 
                              edgecolor=edge,
                              linewidth=2,
                              facecolor=color,
                              alpha=1,
                              zorder=20)
#     artist2.text(player_2_x-0.4,player2_y-0.15,'Na',fontsize=14, color='black', zorder=30)
    
    return artist1, artist2
  
temp = events.loc[events['rallyid'] == 1]

artist1 = []
artist2 = []
for i in range(len(temp)):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    if i % 2 == 0:
        x1 = temp.loc[i, 'hitter_x']
        y1 = temp.loc[i, 'hitter_y']
        x2 = temp.loc[i, 'receiver_x']
        y2 = temp.loc[i, 'receiver_y']
    else:
        x2 = temp.loc[i, 'hitter_x']
        y2 = temp.loc[i, 'hitter_y']
        x1 = temp.loc[i, 'receiver_x']
        y1 = temp.loc[i, 'receiver_y']
    x, y = draw_players(x1, y1, x2, y2)
    artist1.append([x])

    artist2.append([y])

fig = plt.figure()
im_ani = animation.ArtistAnimation(fig, artist1, interval=1000)
plt.show() 
