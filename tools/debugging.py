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
casenames = ['s0_v0']
###########################################################################
# load wrf data
wrfles_data = []
for count, name in enumerate(casenames):
    wrfles_data.append(dict(np.load('/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/' + casenames[count] + '/' + casenames[count]+'.npz')))

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
colors= ['black', 'limegreen', 'gray', 'gold', 'blue', 'red', 'turquoise', 'brown']

###########################################################################
# disk-averaged quantities along the blade
###########################################################################

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(11, 5), constrained_layout=True)

for count, name in enumerate(casenames):
    ax[0,0].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['aoam'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
ax[0,0].set_xlim([0,1]);
# ax[0,0].set_ylim([0,60])
ax[0,0].set_xticks(np.arange(0,1.2,0.2)); ax[0,0].set_yticks(np.arange(0,80,20))
ax[0,0].axes.xaxis.set_ticklabels([])
ax[0,0].set_ylabel(r'$\overline{\alpha}~[^{\circ}]$')
ax[0,0].legend(loc="upper right", fancybox=True, shadow=False, bbox_to_anchor=(1.0, 1.0), ncol=2, fontsize=14)

for count, name in enumerate(casenames):
    ax[0,1].plot(wrfles_data[count]['rOverR'],(1.0-wrfles_data[count]['v1m_star']),
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
ax[0,1].set_xlim([0,1]);
# ax[0,1].set_ylim([0.1,0.4])
ax[0,1].set_xticks(np.arange(0,1.2,0.2)); ax[0,1].set_yticks(np.arange(0.1,0.5,0.1))
ax[0,1].axes.xaxis.set_ticklabels([])
ax[0,1].set_ylabel(r'$\overline{a}=1-\frac{\overline{u}_{m}}{U_{\infty}}~[-]$')

for count, name in enumerate(casenames):
    ax[1,0].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['fd_star'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
ax[1,0].set_xlim([0,1]);
# ax[1,0].set_ylim([0,0.01])
ax[1,0].set_xticks(np.arange(0,1.2,0.2)); ax[1,0].set_yticks(np.arange(0,0.0125,0.005))
ax[1,0].set_ylabel(r'$\overline{F}^{*}_{D}~[-]$'); ax[1,0].set_xlabel(r'$r/R~[-]$')

for count, name in enumerate(casenames):
    ax[1,1].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['fl_star'],
                    color=colors[count],linestyle='solid',linewidth=2,label=name)
ax[1,1].set_xlim([0,1]);
# ax[1,1].set_ylim([-0.025,0.6])
ax[1,1].set_xticks(np.arange(0,1.2,0.2)); ax[1,1].set_yticks(np.arange(0.0,0.8,0.2))
ax[1,1].set_ylabel(r'$\overline{F}^{*}_{L}~[-]$'); ax[1,1].set_xlabel(r'$r/R~[-]$')

plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/figs/disk_averaged_quantities.png", bbox_inches="tight", dpi=600)    

###########################################################################
# y-z wind speed profile comparison
###########################################################################

fig, ax = plt.subplots(nrows=1, ncols=7, figsize=(16, 6), constrained_layout=True)

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
ax[0].legend(loc="upper center", fancybox=True, shadow=False, framealpha=0.5, bbox_to_anchor=(0.675, 0.6), ncol=1, fontsize=12)

# 1D
for count, name in enumerate(casenames):
    ax[1].plot(wrfles_data[count]['uxyt_1D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                color=colors[count],linestyle='solid',linewidth=2,label=name)
ax[1].set_xlim([0.0,1.5])
ax[1].set_ylim([-1.0,1.0])
ax[1].set_xticks(np.linspace(0.25,1.25,3))
ax[1].set_yticks(np.linspace(-1,1.0,5))
ax[1].grid(True, 'major', alpha=0.2)
ax[1].axes.yaxis.set_ticklabels([])
ax[1].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
ax[1].set_title(r'$x/D=1$')

# 3D
for count, name in enumerate(casenames):
    ax[2].plot(wrfles_data[count]['uxyt_3D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                color=colors[count],linestyle='solid',linewidth=2,label=name)
ax[2].set_xlim([0.0,1.5])
ax[2].set_ylim([-1.0,1.0])
ax[2].set_xticks(np.linspace(0.25,1.25,3))
ax[2].set_yticks(np.linspace(-1,1.0,5))
ax[2].grid(True, 'major', alpha=0.2)
ax[2].axes.yaxis.set_ticklabels([])
ax[2].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)   
ax[2].set_title(r'$x/D=3$')

# 6D
for count, name in enumerate(casenames):
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
for count, name in enumerate(casenames):
    ax[4].plot(wrfles_data[count]['uxyt_9D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                color=colors[count],linestyle='solid',linewidth=2,label=name)
ax[4].set_xlim([0.0,1.5])
ax[4].set_ylim([-1.0,1.0])
ax[4].set_xticks(np.linspace(0.25,1.25,3))
ax[4].set_yticks(np.linspace(-1,1.0,5))
ax[4].grid(True, 'major', alpha=0.2)
ax[4].axes.yaxis.set_ticklabels([])
ax[4].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
ax[4].set_title(r'$x/D=9$')

# 12D
for count, name in enumerate(casenames):
    ax[5].plot(wrfles_data[count]['uxyt_12D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                color=colors[count],linestyle='solid',linewidth=2,label=name)
ax[5].set_xlim([0.0,1.5])
ax[5].set_ylim([-1.0,1.0])
ax[5].set_xticks(np.linspace(0.25,1.25,3))
ax[5].set_yticks(np.linspace(-1,1.0,5))
ax[5].grid(True, 'major', alpha=0.2)
ax[5].axes.yaxis.set_ticklabels([])
ax[5].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
ax[5].set_title(r'$x/D=12$')

plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/figs/ux_z.png", bbox_inches="tight", dpi=600)    


###########################################################################
    # streamwise velocity component
    # wrfles
###########################################################################
ks = 0
ke = 59
js = 65
je = 125

ij = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2]]

levels = 101; vmin = 0.5; vmax = 1.0

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12,8), subplot_kw={"projection": "3d"}, constrained_layout=True)

for count, name in enumerate(casenames):
    i = ij[count][0]; j = ij[count][1]
    ax[i,j].set_box_aspect(aspect=(40,8,8))
    ax[i,j].contourf(np.mean(wrfles_data[count]['ux_0D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                        wrfles_data[count]['Y3'][ks:ke,js:je],
                        wrfles_data[count]['Z3'][ks:ke,js:je],
                        levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                        vmin=vmin, vmax=vmax, zdir='x', offset=0*wrfles_data[count]['diameter'])
    ax[i,j].contourf(np.mean(wrfles_data[count]['ux_3D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                        wrfles_data[count]['Y3'][ks:ke,js:je],
                        wrfles_data[count]['Z3'][ks:ke,js:je],
                        levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                        vmin=vmin, vmax=vmax, zdir='x', offset=3*wrfles_data[count]['diameter'])
    ax[i,j].contourf(np.mean(wrfles_data[count]['ux_6D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                        wrfles_data[count]['Y3'][ks:ke,js:je],
                        wrfles_data[count]['Z3'][ks:ke,js:je],
                        levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                        vmin=vmin, vmax=vmax, zdir='x', offset=6*wrfles_data[count]['diameter'])
    ax[i,j].contourf(np.mean(wrfles_data[count]['ux_9D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                        wrfles_data[count]['Y3'][ks:ke,js:je],
                        wrfles_data[count]['Z3'][ks:ke,js:je],
                        levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                        vmin=vmin, vmax=vmax, zdir='x', offset=9*wrfles_data[count]['diameter'])
    ax[i,j].contourf(np.mean(wrfles_data[count]['ux_12D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                        wrfles_data[count]['Y3'][ks:ke,js:je],
                        wrfles_data[count]['Z3'][ks:ke,js:je],
                        levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                        vmin=vmin, vmax=vmax, zdir='x', offset=12*wrfles_data[count]['diameter'])
    # cs = ax[i,j].contourf(np.mean(wrfles_data[count]['ux_15D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
    #                       wrfles_data[count]['Y3'][ks:ke,js:je],
    #                       wrfles_data[count]['Z3'][ks:ke,js:je], 
    #                       levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                       vmin=vmin, vmax=vmax, zdir='x', offset=15*wrfles_data[count]['diameter'])
    # Set the azimuth and elevation angles
    ax[i,j].view_init(azim=225, elev=30, roll=0)
    # ax[i,j].set_xlim3d([-119, 1440])
    # ax[i,j].set_ylim3d([263.0, 501.0])
    # ax[i,j].set_zlim3d([0.0, 238.0])
    ax[i,j].set_xticks(np.arange(0, 18*wrfles_data[count]['diameter'], 3*wrfles_data[count]['diameter']))
    ax[i,j].set_xticklabels([r'$0D$', r'$3D$', r'$6D$', r'$9D$', r'$12D$', r'$15D$'], fontsize=14)
    ax[i,j].tick_params(axis='x', labelrotation=-90)
    ax[i,j].set_yticks(np.linspace(wrfles_data[count]['rotor_yloc'], wrfles_data[count]['rotor_yloc'], 1))
    ax[i,j].set_yticklabels([r'$0D$'], fontsize=14)
    ax[i,j].tick_params(axis='y', labelrotation=-30)
    ax[i,j].set_zticks(np.linspace(wrfles_data[count]['hub_height'], wrfles_data[count]['hub_height'], 1))
    ax[i,j].set_zticklabels([r'$0D$'], fontsize=14)
    ax[i,j].tick_params(axis='z', labelrotation=-90)
    ax[i,j].xaxis.labelpad=50
    ax[i,j].yaxis.labelpad=-5
    ax[i,j].zaxis.labelpad=-5
    ax[i,j].yaxis.set_tick_params(pad=-5)
    ax[i,j].zaxis.set_tick_params(pad=-1)
    ax[i,j].set(xlabel=r'$x~[\textrm{m}]$', ylabel=r'$y~[\textrm{m}]$', zlabel=r'$z~[\textrm{m}]$')
    ax[i,j].set_title(casenames[count], fontsize=24, y=0.85)
# fig.colorbar(cs, ax=[ax[0,0], ax[0,1], ax[0,2], ax[1,0], ax[1,1], ax[1,2]],
#              ticks=np.linspace(vmin,vmax,6,endpoint=True),
#              label=r'$\overline{u}/U_{\infty}~[-]$',
#              aspect=75, pad=0.02, orientation='horizontal')
# for c in cs.collections:
#     c.set_edgecolor("face")
plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/figs/wrfles_uvel_slice_yz.png", bbox_inches="tight", dpi=600)
plt.show()