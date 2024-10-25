#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 09:00:00 2024

@author: kale
"""

import math
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from scipy import interpolate
import subprocess                              # for .gif videos
###########################################################################
np.seterr(divide='ignore', invalid='ignore')
###########################################################################
def mean_bias_error(pred,true):
    return np.nanmean(pred-true)
def mean_relative_error(pred,true):
    return 100*(np.nanmean((pred-true)/true))
def mean_absolute_relative_error(pred,true):
    return 100*(np.nanmean(np.abs(pred-true)/true))
def root_mean_square_error(pred,true):
    return math.sqrt(np.nanmean(np.square(np.subtract(pred,true))))
def grid2gif(image_str,output_gif):
    str1 = 'magick -delay 50 -loop 0 ' + image_str  + ' ' + output_gif
    subprocess.call(str1,shell=True)
###########################################################################
# casenames = [r's0_v4', r'sn2_v2', r's0_v2', r's2_v2', r'sn4_v0', r'sn2_v0', r's0_v0', r's2_v0', r's4_v0', r'sn2_vn2', r's0_vn2', r's2_vn2', r's0_vn4']

# casenames = [r's0_v0']

casenames = [r's0_v0', r's0_v2']

disk_avg = True
contours = True
profiles = True
itqp     = True
###########################################################################
# load wrf data
print('Loading data...')

wrfles_data = []
for count, name in enumerate(casenames):
    wrfles_data.append(dict(np.load('/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/' + casenames[count]+'.npz')))

###########################################################################
# set figure layout parameters
plt.style.use('/anvil/scratch/x-smata/postprocessing/scripts/figures_layout.mplstyle')
fontsize = 24
mpl.rcParams['xtick.labelsize'] = 20 
mpl.rcParams['ytick.labelsize'] = 20 
###########################################################################
## Plotting turbine-representing circle in y-z plots
# number of points
n = 1000

# radius
r = wrfles_data[0]['diameter']/2

# locations
# c11 = rotor_yloc-0.5*dx;
c11 = wrfles_data[0]['rotor_yloc']
# c12 = z_av(k_loc_new)+0.5*dz(1, k_loc_new);
c12 = wrfles_data[0]['hub_height']

# running variable
t = np.linspace(0, 2*np.pi, n)

x11 = c11 + r*np.sin(t)
y11 = c12 + r*np.cos(t)

# calculation of the horizontal spacing:
Lx = wrfles_data[0]['Nx']*wrfles_data[0]['dx'] # Lx of the computational domain
xx = np.linspace(wrfles_data[0]['dx']/2,Lx-(wrfles_data[0]['dx']/2),wrfles_data[0]['Nx']) # Longitudinal spacing in meters
###########################################################################
# error quantification 
zmin=-1
zmax=1
nondim_r=(wrfles_data[0]['z_av']-wrfles_data[0]['hub_height'])/wrfles_data[0]['diameter'] # wrf
n=25 # required length
tdata=np.linspace(zmin,zmax,n)
###########################################################################
plt.rcParams.update({
    'text.usetex': True,
    'text.latex.preamble': r'\usepackage{amsfonts}'
})
# colors = [
#     (31/255, 119/255, 180/255), 
#     (255/255, 127/255, 14/255),
#     (44/255, 160/255, 44/255),
#     (214/255, 39/255, 40/255),
#     (148/255, 103/255, 189/255),
#     (140/255, 86/255, 75/255),
#     (227/255, 119/255, 194/255),
#     (127/255, 127/255, 127/255),
#     (188/255, 189/255, 34/255),
#     (23/255, 190/255, 207/255),
#     (255/255, 152/255, 150/255),
#     (197/255, 176/255, 213/255),
#     (219/255, 219/255, 141/255)
# ]

colors = [
    '#ffdead',  # Navajo White (light)
    '#4b0082',  # Indigo (blue shade)
    '#ff0000',  # Red
    '#008000',  # Green
    '#ff69b4',  # Hot Pink
    '#0000ff',  # Blue
    '#ffd700',  # Gold
    '#6495ed',  # Cornflower Blue
    '#8b4513',  # Saddle Brown
    '#00ff00',  # Lime
    '#2f4f4f',  # Dark Slate Gray
    '#ff00ff',  # Magenta
    '#00ffff'   # Cyan
]

###########################################################################
# disk-averaged quantities along the blade
###########################################################################

if disk_avg:

    print('Plotting disk-averaged quantities')

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(11, 5), constrained_layout=True)

    for count, name in enumerate(casenames):
        ax[0,0].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['aoam'],
                        color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[0,0].set_xlim([0,1])
        # ax[0,0].set_ylim([0,60])
        ax[0,0].set_xticks(np.arange(0,1.2,0.2));
        # ax[0,0].set_yticks(np.arange(0,80,20))
        ax[0,0].axes.xaxis.set_ticklabels([])
        ax[0,0].set_ylabel(r'$\overline{\alpha}~[^{\circ}]$')
        ax[0,0].legend(loc="upper right", fancybox=True, shadow=False, ncol=3, fontsize=8)

    for count, name in enumerate(casenames):
        ax[0,1].plot(wrfles_data[count]['rOverR'],(1.0-wrfles_data[count]['v1m_star']),
                        color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[0,1].set_xlim([0,1])
        # ax[0,1].set_ylim([0.1,0.4])
        ax[0,1].set_xticks(np.arange(0,1.2,0.2));
        # ax[0,1].set_yticks(np.arange(0.1,0.5,0.1))
        ax[0,1].axes.xaxis.set_ticklabels([])
        ax[0,1].set_ylabel(r'$\overline{a}=1-\frac{\overline{u}_{m}}{U_{\infty}}~[-]$')

    for count, name in enumerate(casenames):
        ax[1,0].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['fd_star'],
                        color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[1,0].set_xlim([0,1])
        # ax[1,0].set_ylim([0,0.01])
        ax[1,0].set_xticks(np.arange(0,1.2,0.2));
        # ax[1,0].set_yticks(np.arange(0,0.0125,0.005))
        ax[1,0].set_ylabel(r'$\overline{F}^{*}_{D}~[-]$'); ax[1,0].set_xlabel(r'$r/R~[-]$')

    for count, name in enumerate(casenames):
        ax[1,1].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['fl_star'],
                        color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[1,1].set_xlim([0,1])
        # ax[1,1].set_ylim([-0.025,0.6])
        ax[1,1].set_xticks(np.arange(0,1.2,0.2));
        # ax[1,1].set_yticks(np.arange(0.0,0.8,0.2))
        ax[1,1].set_ylabel(r'$\overline{F}^{*}_{L}~[-]$'); ax[1,1].set_xlabel(r'$r/R~[-]$')

    plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/disk_averaged_quantities.png", bbox_inches="tight", dpi=600)    

###########################################################################
# y-z wind speed profile comparison
###########################################################################

if profiles:

    print('Plotting wind speed profiles')

    fig, ax = plt.subplots(nrows=1, ncols=6, figsize=(16, 6), constrained_layout=True)

    # 0D
    for count, name in enumerate(casenames):
        ax[0].plot(wrfles_data[count]['uxyt_0D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[0].set_xlim([0.0,1.5])
        ax[0].set_ylim([-1.0,1.0])
        ax[0].set_xticks(np.linspace(0.25,1.25,3))
        ax[0].set_yticks(np.linspace(-1,1.0,5))
        ax[0].grid(True, 'major', alpha=0.2)
        ax[0].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize);
        ax[0].set_ylabel(r'$z/D~[-]$',fontsize=fontsize)
        ax[0].set_title(r'$x/D=0$')
        ax[0].legend(loc="best", fancybox=True, shadow=False, framealpha=0.5, ncol=1, fontsize=8)

    # 1D
    # for count, name in enumerate(casenames):
        ax[1].plot(wrfles_data[count]['uxyt_2D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[1].set_xlim([0.0,1.5])
        ax[1].set_ylim([-1.0,1.0])
        ax[1].set_xticks(np.linspace(0.25,1.25,3))
        ax[1].set_yticks(np.linspace(-1,1.0,5))
        ax[1].grid(True, 'major', alpha=0.2)
        ax[1].axes.yaxis.set_ticklabels([])
        ax[1].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
        ax[1].set_title(r'$x/D=2$')

    # 3D
    # for count, name in enumerate(casenames):
        ax[2].plot(wrfles_data[count]['uxyt_4D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[2].set_xlim([0.0,1.5])
        ax[2].set_ylim([-1.0,1.0])
        ax[2].set_xticks(np.linspace(0.25,1.25,3))
        ax[2].set_yticks(np.linspace(-1,1.0,5))
        ax[2].grid(True, 'major', alpha=0.2)
        ax[2].axes.yaxis.set_ticklabels([])
        ax[2].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)   
        ax[2].set_title(r'$x/D=4$')

    # 6D
    # for count, name in enumerate(casenames):
        ax[3].plot(wrfles_data[count]['uxyt_6D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[3].set_xlim([0.0,1.5])
        ax[3].set_ylim([-1.0,1.0])
        ax[3].set_xticks(np.linspace(0.25,1.25,3))
        ax[3].set_yticks(np.linspace(-1,1.0,5))
        ax[3].grid(True, 'major', alpha=0.2)
        ax[3].axes.yaxis.set_ticklabels([])
        ax[3].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
        ax[3].set_title(r'$x/D=6$')

    # 9D
    # for count, name in enumerate(casenames):
        ax[4].plot(wrfles_data[count]['uxyt_8D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[4].set_xlim([0.0,1.5])
        ax[4].set_ylim([-1.0,1.0])
        ax[4].set_xticks(np.linspace(0.25,1.25,3))
        ax[4].set_yticks(np.linspace(-1,1.0,5))
        ax[4].grid(True, 'major', alpha=0.2)
        ax[4].axes.yaxis.set_ticklabels([])
        ax[4].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
        ax[4].set_title(r'$x/D=8$')

    # 12D
    # for count, name in enumerate(casenames):
        ax[5].plot(wrfles_data[count]['uxyt_10D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[5].set_xlim([0.0,1.5])
        ax[5].set_ylim([-1.0,1.0])
        ax[5].set_xticks(np.linspace(0.25,1.25,3))
        ax[5].set_yticks(np.linspace(-1,1.0,5))
        ax[5].grid(True, 'major', alpha=0.2)
        ax[5].axes.yaxis.set_ticklabels([])
        ax[5].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
        ax[5].set_title(r'$x/D=10$')

    plt.savefig(f"/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/u_profiles.png", bbox_inches="tight", dpi=600)  


    fig, ax = plt.subplots(nrows=1, ncols=6, figsize=(16, 6), constrained_layout=True)

    # 0D
    xlims = [-1.5, 1.0]
    for count, name in enumerate(casenames):
        ax[0].plot(wrfles_data[count]['vxyt_0D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[0].set_xlim(xlims)
        ax[0].set_ylim([-1.0,1.0])
        # ax[0].set_xticks(np.linspace(0.25,1.25,3))
        ax[0].set_yticks(np.linspace(-1,1.0,5))
        ax[0].grid(True, 'major', alpha=0.2)
        ax[0].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize);
        ax[0].set_ylabel(r'$z/D~[-]$',fontsize=fontsize)
        ax[0].set_title(r'$x/D=0$')
        ax[0].legend(loc="best", fancybox=True, shadow=False, framealpha=0.5, ncol=1, fontsize=8)

    # 1D
    # for count, name in enumerate(casenames):
        ax[1].plot(wrfles_data[count]['vxyt_2D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[1].set_xlim(xlims)
        ax[1].set_ylim([-1.0,1.0])
        # ax[1].set_xticks(np.linspace(0.25,1.25,3))
        ax[1].set_yticks(np.linspace(-1,1.0,5))
        ax[1].grid(True, 'major', alpha=0.2)
        ax[1].axes.yaxis.set_ticklabels([])
        ax[1].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
        ax[1].set_title(r'$x/D=2$')

    # 3D
    # for count, name in enumerate(casenames):
        ax[2].plot(wrfles_data[count]['vxyt_4D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[2].set_xlim(xlims)
        ax[2].set_ylim([-1.0,1.0])
        # ax[2].set_xticks(np.linspace(0.25,1.25,3))
        ax[2].set_yticks(np.linspace(-1,1.0,5))
        ax[2].grid(True, 'major', alpha=0.2)
        ax[2].axes.yaxis.set_ticklabels([])
        ax[2].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)   
        ax[2].set_title(r'$x/D=4$')

    # 6D
    # for count, name in enumerate(casenames):
        ax[3].plot(wrfles_data[count]['vxyt_6D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[3].set_xlim(xlims)
        ax[3].set_ylim([-1.0,1.0])
        # ax[3].set_xticks(np.linspace(0.25,1.25,3))
        ax[3].set_yticks(np.linspace(-1,1.0,5))
        ax[3].grid(True, 'major', alpha=0.2)
        ax[3].axes.yaxis.set_ticklabels([])
        ax[3].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
        ax[3].set_title(r'$x/D=6$')

    # 9D
    # for count, name in enumerate(casenames):
        ax[4].plot(wrfles_data[count]['vxyt_8D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[4].set_xlim(xlims)
        ax[4].set_ylim([-1.0,1.0])
        # ax[4].set_xticks(np.linspace(0.25,1.25,3))
        ax[4].set_yticks(np.linspace(-1,1.0,5))
        ax[4].grid(True, 'major', alpha=0.2)
        ax[4].axes.yaxis.set_ticklabels([])
        ax[4].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
        ax[4].set_title(r'$x/D=8$')

    # 12D
    # for count, name in enumerate(casenames):
        ax[5].plot(wrfles_data[count]['vxyt_10D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
        ax[5].set_xlim(xlims)
        ax[5].set_ylim([-1.0,1.0])
        # ax[5].set_xticks(np.linspace(0.25,1.25,3))
        ax[5].set_yticks(np.linspace(-1,1.0,5))
        ax[5].grid(True, 'major', alpha=0.2)
        ax[5].axes.yaxis.set_ticklabels([])
        ax[5].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
        ax[5].set_title(r'$x/D=10$')

    plt.savefig(f"/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/v_profiles.png", bbox_inches="tight", dpi=600)  

# # ###########################################################################
# # # y-z wind speed profile comparison
# # ###########################################################################

# # fig, ax = plt.subplots(nrows=1, ncols=6, figsize=(16, 6), constrained_layout=True)

# # # 0D
# # for count, name in enumerate(casenames):
# #     ax[0].plot(wrfles_data[count]['uupxyt_0D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[0].set_xlim([0.0,1.5])
# # # ax[0].set_ylim([-1.0,1.0])
# # # ax[0].set_xticks(np.linspace(0.25,1.25,3))
# # ax[0].set_yticks(np.linspace(-1,1.0,5))
# # ax[0].grid(True, 'major', alpha=0.2)
# # ax[0].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize);
# # ax[0].set_ylabel(r'$z/D~[-]$',fontsize=fontsize)
# # ax[0].set_title(r'$x/D=0$')
# # ax[0].legend(loc="upper center", fancybox=True, shadow=False, framealpha=0.5, bbox_to_anchor=(0.675, 0.6), ncol=1, fontsize=12)

# # # 1D
# # for count, name in enumerate(casenames):
# #     ax[1].plot(wrfles_data[count]['uupxyt_1D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[1].set_xlim([0.0,1.5])
# # # ax[1].set_ylim([-1.0,1.0])
# # # ax[1].set_xticks(np.linspace(0.25,1.25,3))
# # ax[1].set_yticks(np.linspace(-1,1.0,5))
# # ax[1].grid(True, 'major', alpha=0.2)
# # ax[1].axes.yaxis.set_ticklabels([])
# # ax[1].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
# # ax[1].set_title(r'$x/D=1$')

# # # 3D
# # for count, name in enumerate(casenames):
# #     ax[2].plot(wrfles_data[count]['uupxyt_3D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[2].set_xlim([0.0,1.5])
# # # ax[2].set_ylim([-1.0,1.0])
# # # ax[2].set_xticks(np.linspace(0.25,1.25,3))
# # ax[2].set_yticks(np.linspace(-1,1.0,5))
# # ax[2].grid(True, 'major', alpha=0.2)
# # ax[2].axes.yaxis.set_ticklabels([])
# # ax[2].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)   
# # ax[2].set_title(r'$x/D=3$')

# # # 6D
# # for count, name in enumerate(casenames):
# #     ax[3].plot(wrfles_data[count]['uupxyt_6D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[3].set_xlim([0.0,1.5])
# # # ax[3].set_ylim([-1.0,1.0])
# # # ax[3].set_xticks(np.linspace(0.25,1.25,3))
# # ax[3].set_yticks(np.linspace(-1,1.0,5))
# # ax[3].grid(True, 'major', alpha=0.2)
# # ax[3].axes.yaxis.set_ticklabels([])
# # ax[3].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
# # ax[3].set_title(r'$x/D=6$')

# # # 9D
# # for count, name in enumerate(casenames):
# #     ax[4].plot(wrfles_data[count]['uupxyt_9D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[4].set_xlim([0.0,1.5])
# # # ax[4].set_ylim([-1.0,1.0])
# # # ax[4].set_xticks(np.linspace(0.25,1.25,3))
# # ax[4].set_yticks(np.linspace(-1,1.0,5))
# # ax[4].grid(True, 'major', alpha=0.2)
# # ax[4].axes.yaxis.set_ticklabels([])
# # ax[4].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
# # ax[4].set_title(r'$x/D=9$')

# # # 12D
# # for count, name in enumerate(casenames):
# #     ax[5].plot(wrfles_data[count]['uupxyt_12D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
# #                 color=colors[count],linestyle='solid',linewidth=2,label=name)
# # # ax[5].set_xlim([0.0,1.5])
# # # ax[5].set_ylim([-1.0,1.0])
# # # ax[5].set_xticks(np.linspace(0.25,1.25,3))
# # ax[5].set_yticks(np.linspace(-1,1.0,5))
# # ax[5].grid(True, 'major', alpha=0.2)
# # ax[5].axes.yaxis.set_ticklabels([])
# # ax[5].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
# # ax[5].set_title(r'$x/D=12$')

# # plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/px_z.png", bbox_inches="tight", dpi=600) 

###########################################################################
    # streamwise velocity component
    # wrfles
###########################################################################

if contours:

    print('Plotting streamwise velocity contours')

    ks = 50
    ke = 139
    js = 51
    je = 140

    levels = 255
    vmin = 0.5
    vmax = 1.0

    for count, name in enumerate(casenames):

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,6), subplot_kw={"projection": "3d"})

        ax.set_box_aspect(aspect=(40,8,8))
        cs = ax.contourf(np.mean(wrfles_data[count]['ux_0D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=0*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['ux_2D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=2*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['ux_4D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=4*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['ux_6D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=6*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['ux_8D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=8*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['ux_10D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=10*wrfles_data[count]['diameter'])
        ax.view_init(azim=225, elev=30, roll=0)
        print(f"diameter: {wrfles_data[count]['diameter']}")
        ax.set_xticks(np.arange(0, 12*wrfles_data[count]['diameter'], 2*wrfles_data[count]['diameter']))
        ax.set_xticklabels([r'$0D$', r'$2D$', r'$4D$', r'$8D$', r'$8D$', r'$10D$'], fontsize=14)
        ax.tick_params(axis='x', labelrotation=-90)
        ax.set_yticks(np.linspace(wrfles_data[count]['rotor_yloc'], wrfles_data[count]['rotor_yloc'], 1))
        ax.set_yticklabels([r'$0D$'], fontsize=14)
        ax.tick_params(axis='y', labelrotation=-30)
        ax.set_zticks(np.linspace(wrfles_data[count]['hub_height'], wrfles_data[count]['hub_height'], 1))
        ax.set_zticklabels([r'$0D$'], fontsize=14)
        ax.tick_params(axis='z', labelrotation=-90)
        ax.xaxis.labelpad=50
        ax.yaxis.labelpad=-5
        ax.zaxis.labelpad=-5
        ax.yaxis.set_tick_params(pad=-5)
        ax.zaxis.set_tick_params(pad=-1)
        ax.set(xlabel=r'$x$', ylabel=r'$y$', zlabel=r'$z$')
        ax.set_title(casenames[count], fontsize=24, y=0.85)
        # Generate colorbar with adjusted settings
        cbar = fig.colorbar(cs, ax=ax, orientation='horizontal', pad=0.2, shrink=0.7)

        # Reduce the number of colorbar ticks to avoid overlap
        cbar.set_ticks(np.linspace(vmin, vmax, 6))  # Adjust the number of ticks to avoid crowding

        # Adjust tick label size and padding
        cbar.ax.tick_params(labelsize=10)  # Adjust tick label font size
        cbar.set_label('$\\overline{u}/U_{\\infty}$ [-]', fontsize=12, labelpad=15)  # Increase label padding

        plt.savefig(f"/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/{name}_uvel_yz.png", bbox_inches="tight", dpi=800)
        plt.close()

###########################################################################
# spanwise velocity component
vmin = -0.4
vmax = 0.4
###########################################################################

if contours:

    print('Plotting lateral velocity contours')

    for count, name in enumerate(casenames):

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,8), subplot_kw={"projection": "3d"})

        ax.set_box_aspect(aspect=(40,8,8))
        ax.contourf(np.mean(wrfles_data[count]['vx_0D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=0*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['vx_2D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=3*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['vx_4D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=6*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['vx_8D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=9*wrfles_data[count]['diameter'])
        ax.contourf(np.mean(wrfles_data[count]['vx_10D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                            wrfles_data[count]['Y3'][ks:ke,js:je],
                            wrfles_data[count]['Z3'][ks:ke,js:je],
                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                            vmin=vmin, vmax=vmax, zdir='x', offset=12*wrfles_data[count]['diameter'])
        ax.view_init(azim=225, elev=30, roll=0)
        ax.set_xticks(np.arange(0, 15*wrfles_data[count]['diameter'], 3*wrfles_data[count]['diameter']))
        ax.set_xticklabels([r'$0D$', r'$3D$', r'$6D$', r'$9D$', r'$12D$'], fontsize=14)
        ax.tick_params(axis='x', labelrotation=-90)
        ax.set_yticks(np.linspace(wrfles_data[count]['rotor_yloc'], wrfles_data[count]['rotor_yloc'], 1))
        ax.set_yticklabels([r'$0D$'], fontsize=14)
        ax.tick_params(axis='y', labelrotation=-30)
        ax.set_zticks(np.linspace(wrfles_data[count]['hub_height'], wrfles_data[count]['hub_height'], 1))
        ax.set_zticklabels([r'$0D$'], fontsize=14)
        ax.tick_params(axis='z', labelrotation=-90)
        ax.xaxis.labelpad=50
        ax.yaxis.labelpad=-5
        ax.zaxis.labelpad=-5
        ax.yaxis.set_tick_params(pad=-5)
        ax.zaxis.set_tick_params(pad=-1)
        ax.set(xlabel=r'$x~[\textrm{m}]$', ylabel=r'$y~[\textrm{m}]$', zlabel=r'$z~[\textrm{m}]$')
        ax.set_title(casenames[count], fontsize=24, y=0.85)

        plt.savefig(f"/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/{name}_vvel_yz.png", bbox_inches="tight", dpi=800)
        plt.close()

###########################################################################
# spanwise velocity component
###########################################################################

if itqp:

    print('Plotting induction, power, thrust, and torque')

    # wrfles - simple controller
    # wrfles_rel_diff_power  = []
    # wrfles_rel_diff_thrust = []
    # wrfles_rel_diff_torque = []
    # wrfles_rel_diff_ind    = []
    # for count in range(len(casenames)):
    #     wrfles_rel_diff_power.append(mean_relative_error(wrfles_data[count]['power_aero'],wrfles_data[0]['power_aero']))
    #     wrfles_rel_diff_thrust.append(mean_relative_error(wrfles_data[count]['thrust'],wrfles_data[0]['thrust']))
    #     wrfles_rel_diff_torque.append(mean_relative_error(wrfles_data[count]['torque_aero'],wrfles_data[0]['torque_aero']))
    #     wrfles_rel_diff_ind.append(mean_relative_error((1.0-wrfles_data[count]['v1m_star']),(1.0-wrfles_data[0]['v1m_star'])))

    width = 0.75
    alpha = 1.0

    fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(13, 9), sharex=True, constrained_layout = True)
    ax[0].axhline(0, color='black', linestyle='solid', linewidth=1)
    ax[1].axhline(0, color='black', linestyle='solid', linewidth=1)
    ax[2].axhline(0, color='black', linestyle='solid', linewidth=1)
    ax[3].axhline(0, color='black', linestyle='solid', linewidth=1)

    ind = np.arange(len(casenames))

    for count in range(len(casenames)):

        wrfles_rel_diff_power  = []
        wrfles_rel_diff_thrust = []
        wrfles_rel_diff_torque = []
        wrfles_rel_diff_ind    = []

        wrfles_rel_diff_power.append(mean_relative_error(wrfles_data[count]['power_aero'],wrfles_data[0]['power_aero']).round(1))
        wrfles_rel_diff_thrust.append(mean_relative_error(wrfles_data[count]['thrust'],wrfles_data[0]['thrust']).round(1))
        wrfles_rel_diff_torque.append(mean_relative_error(wrfles_data[count]['torque_aero'],wrfles_data[0]['torque_aero']).round(1))
        wrfles_rel_diff_ind.append(mean_relative_error((1.0-wrfles_data[count]['v1m_star']),(1.0-wrfles_data[0]['v1m_star'])).round(1))

        # induction
        ax[0].bar(ind[count], wrfles_rel_diff_ind, color=colors[count], edgecolor='black', alpha=alpha)
        ax[0].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{a}}~[\%]$', fontsize=fontsize)
        ax[0].text(ind[count], 3, f'{wrfles_rel_diff_ind[0]}\%', ha='center', fontsize=15)

        # thrust
        ax[1].bar(ind[count], wrfles_rel_diff_thrust, color=colors[count], edgecolor='black', alpha=alpha)
        ax[1].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{T}}~[\%]$', fontsize=fontsize)
        ax[1].text(ind[count], -0.5, f'{wrfles_rel_diff_thrust[0]}\%', ha='center', fontsize=15)

        # torque
        ax[2].bar(ind[count], wrfles_rel_diff_torque, color=colors[count], edgecolor='black', alpha=alpha)
        ax[2].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{Q}}~[\%]$', fontsize=fontsize)
        ax[2].text(ind[count], -2.5, f'{wrfles_rel_diff_torque[0]}\%', ha='center', fontsize=15)

        # power
        ax[3].bar(ind[count], wrfles_rel_diff_power, color=colors[count], edgecolor='black', alpha=alpha)
        ax[3].set_xticks(ind)
        ax[3].set_xticklabels(casenames)
        ax[3].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{P}}~[\%]$', fontsize=fontsize)
        ax[3].text(ind[count], -2.5, f'{wrfles_rel_diff_power[0]}\%', ha='center', fontsize=15)

    plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/rel_err_ind_thrust_torque_power.png", bbox_inches="tight", dpi=800)
    plt.show()

# # ###########################################################################
# # # calculate total wind speed in streamwise direction:
# # ###########################################################################
# # ws_uytz_gal = np.sqrt(wrfles_data['uytz_gal']**2 + wrfles_data['vytz_gal']**2 + wrfles_data['wytz_gal']**2)
# # ws_min = 0.0
# # ws_max = 10.0
# # # ws_max = wrfles_data['uinf_gal']

# # # calculate dynamic pressure:
# # p_dyn = 0.5*wrfles_data['rho']*ws_uytz_gal**2/1000.0 # in kPa

# # # calculate pressure drop:
# # delta_p = np.max(wrfles_data['pytz_gal']) - wrfles_data['pytz_gal'][int(wrfles_data['ix_rotor'])+3]

# # # power
# # rho = wrfles_data['rho']
# # a = 1-(ws_uytz_gal[int(wrfles_data['ix_rotor'])]/wrfles_data['uinf_gal'])
# # area = np.pi*wrfles_data['diameter']**2/4
# # thrust = 2*rho*wrfles_data['uinf_gal']**2*a*(1-a)*area/1E3   # kN
# # power = 2*rho*wrfles_data['uinf_gal']**3*a*(1-a)**2*area/1E3 # kW

# # p_min = 98.940
# # p_max = 98.980

# # fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(13.5, 4), sharex=True, constrained_layout = True)

# # # velocity distribution in streamwise direction:
# # ax[0].plot(xx, ws_uytz_gal, color='black', linestyle='solid', linewidth=3, zorder=10)
# # ax[0].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [wrfles_data['uinf_gal'], wrfles_data['uinf_gal']],
# #             color='blue', linestyle='dashed', linewidth=1.5)
# # ax[0].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [ws_uytz_gal[int(wrfles_data['ix_rotor'])], ws_uytz_gal[int(wrfles_data['ix_rotor'])]],
# #             color='red', linestyle='dashdot', linewidth=1.5)
# # ax[0].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [np.min(ws_uytz_gal), np.min(ws_uytz_gal)],
# #             color='blue', linestyle='dashed', linewidth=1.5)
# # ax[0].plot([wrfles_data['rotor_xloc'],wrfles_data['rotor_xloc']], [ws_min,ws_max],
# #             color='black', linestyle='dashed', linewidth=1.5)    
# # ax[0].set_xlim([wrfles_data['rotor_xloc']-(3*wrfles_data['diameter']),
# #                 wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])])
# # ax[0].set_xticks([wrfles_data['rotor_xloc']-(3*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc'],
# #                     wrfles_data['rotor_xloc']+(5*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(10*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(15*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(20*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(25*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])])
# # ax[0].set_ylim([ws_min,ws_max])
# # ax[0].set_ylabel(r'$U~\textrm{[m~s$^{-1}$]}$', fontsize=fontsize)
# # ax[0].tick_params(direction='in', length=6)
# # ax[0].axes.xaxis.set_ticklabels([])

# # # pressure distribution in streamwise direction:
# # ax[1].plot(xx, wrfles_data['pytz_gal']/1000.0, color='black', linestyle='solid', linewidth=3, zorder=10)
# # ax[1].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [np.max(wrfles_data['pytz_gal'])/1000.0, np.max(wrfles_data['pytz_gal'])/1000.0],
# #             color='blue', linestyle='dashed', linewidth=1.5)
# # ax[1].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [wrfles_data['pytz_gal'][0]/1000.0,wrfles_data['pytz_gal'][0]/1000.0],
# #             color='red', linestyle='dashdot', linewidth=1.5)
# # ax[1].plot([xx[0], wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])],
# #             [wrfles_data['pytz_gal'][int(wrfles_data['ix_rotor'])+3]/1000.0,
# #             wrfles_data['pytz_gal'][int(wrfles_data['ix_rotor'])+3]/1000.0],
# #             color='blue', linestyle='dashed', linewidth=1.5)
# # ax[1].plot([wrfles_data['rotor_xloc'],wrfles_data['rotor_xloc']], [p_min,p_max],
# #             color='black', linestyle='dashed', linewidth=1.5)    
# # ax[1].set_xlim([wrfles_data['rotor_xloc']-(3*wrfles_data['diameter']),
# #                 wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])])
# # ax[1].set_xticks([wrfles_data['rotor_xloc']-(3*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc'],
# #                     wrfles_data['rotor_xloc']+(5*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(10*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(15*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(20*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(25*wrfles_data['diameter']),
# #                     wrfles_data['rotor_xloc']+(30*wrfles_data['diameter'])])
# # ax[1].set_ylim([p_min,p_max])
# # ax[1].set_xlabel(r'$x/D~[-]$', fontsize=fontsize) 
# # ax[1].set_ylabel(r'$P_{tot}~\textrm{[kPa]}$', fontsize=fontsize)
# # ax[1].tick_params(direction='in', length=6)
# # ax[1].axes.xaxis.set_ticklabels([r'$-3$', r'$x_{rotor}$', r'$5$', r'$10$', r'$15$', r'$20$', r'$25$', r'$30$'], fontsize=fontsize)

# # plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/wrfles_vel_pres_dist.png", bbox_inches="tight", dpi=600)
# # plt.show()

# # ###########################################################################

# # ###########################################################################

# # vmin = 0.6
# # vmax = 1.0
# # for i in range(0,len(wrfles_data['ux_0D_gal'])):
# #     print(i,'/',wrfles_data['ux_0D_gal'].shape[0]-1)
# #     fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.2, 5), constrained_layout = True)
# #     # y-z contour plot for wind speed
# #     cs0 = ax.pcolormesh(wrfles_data['Y3'], wrfles_data['Z3'], wrfles_data['ux_0D_gal'][i,:,:]/wrfles_data['uinf_gal'],
# #                         vmin=vmin, vmax=vmax, alpha=1, cmap='Spectral_r', shading='gouraud', rasterized=True)
# #     ax.plot(wrfles_data['bpy_gal'][i,:,0], wrfles_data['bpz_gal'][i,:,0], color='black', marker='o',
# #             markerfacecolor='black', markersize=1, linestyle='solid', linewidth=3)
# #     ax.plot(wrfles_data['bpy_gal'][i,:,1], wrfles_data['bpz_gal'][i,:,1], color='red', marker='o',
# #             markerfacecolor='black', markersize=1, linestyle='solid', linewidth=3)
# #     ax.plot(wrfles_data['bpy_gal'][i,:,2], wrfles_data['bpz_gal'][i,:,2], color='limegreen', marker='o',
# #             markerfacecolor='black', markersize=1, linestyle='solid', linewidth=3)
# #     # ax.set_xlim([300, 462])
# #     # ax.set_ylim([300, 460])
# #     ax.set_xticks([])
# #     ax.set_yticks([])
# #     ax.axes.xaxis.set_ticklabels([])
# #     ax.axes.yaxis.set_ticklabels([])
# #     ax.invert_xaxis()

# #     plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/u_00"+str(i)+".tif",bbox_inches="tight",dpi=100)

# #     plt.show()
# #     plt.close()

# # grid2gif('/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/rotorPlane/*.tif',
# #          '/anvil/scratch/x-smata/wrf_les_sweep/runs/[SWEEP_NAME]/figs/uvel.gif')

print('Done.')