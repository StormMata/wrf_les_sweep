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
save_figures = True
plot_figures = True
plot_animation = False
###########################################################################
path_main = '/nobackup1c/users/bkale/postprocessing'
path_savedata = path_main+'/'+'results'
path_simdata = path_main+'/'+'simdata'
path_pythonPP = path_main+'/'+'scripts'
codename_wrfles = 'wrfles_data_10m'
codename_padeops = 'padeops_data_10m'
sim_type1 = 'controller_simple'
sim_type2 = 'controller_advanced'
sim_data = 'shear_veer'
path_data_wrfles_simple = path_simdata+'/'+sim_data+'/'+codename_wrfles+'/'+sim_type1
path_data_wrfles = path_simdata+'/'+sim_data+'/'+codename_wrfles+'/'+sim_type2
path_data_padeops = path_simdata+'/'+sim_data+'/'+codename_padeops
###########################################################################
# case names
# simnames = ['shear_00_veer_00', 'shear_01_veer_00', 'shear_02_veer_00',
#             'shear_01_veer_01', 'shear_00_veer_01', 'shear_00_veer_02']
# simnames_extra = ['shear_00_veer_00', 'shear_01_veer_00', 'shear_02_veer_00',
#                   'shear_01_veer_01', 'shear_00_veer_01', 'shear_00_veer_02',
#                   'shear_00_backing_01', 'shear_00_backing_02']
# case names in latex form for plotting
# casenames = ['s00_v00', 's01_v00', 's02_v00', 's01_v01', 's00_v01', 's00_v02']
# casenames_extra = ['s00_v00', 's01_v00', 's02_v00', 's01_v01', 's00_v01', 's00_v02',
#                    's00_b01', 's00_b02']

casenames = ['s0_v0']
###########################################################################
# load wrf data
wrfles_data = []
for count, name in enumerate(casenames):
    wrfles_data.append(dict(np.load('/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/' + casenames[count] + '/' + casenames[count]+'.npz')))
# wrfles_data = []
# for count, name in enumerate(simnames_extra):
#     wrfles_data.append(dict(np.load(path_data_wrfles+'/'+simnames_extra[count]+'/'+'gad_'+simnames_extra[count]+'.npz')))
# # load padeops data
# padeops_data = []
# for count, name in enumerate(simnames):
#     padeops_data.append(dict(np.load(path_data_padeops+'/'+simnames[count]+'/'+simnames[count]+'.npz')))
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
# for quick plotting purposes only; must update the same plot down below. #
###########################################################################
# relative difference
# wrfles - simple controller
# wrfles_simple_rel_diff_power = []
# wrfles_simple_rel_diff_thrust = []
# wrfles_simple_rel_diff_torque = []
# wrfles_simple_rel_diff_ind = []
# for count in range(len(casenames)):
#     wrfles_simple_rel_diff_power.append(mean_relative_error(wrfles_data[count]['power_aero'],wrfles_data[0]['power_aero']))
#     wrfles_simple_rel_diff_thrust.append(mean_relative_error(wrfles_data[count]['thrust'],wrfles_data[0]['thrust']))
#     wrfles_simple_rel_diff_torque.append(mean_relative_error(wrfles_data[count]['torque_aero'],wrfles_data[0]['torque_aero']))
#     wrfles_simple_rel_diff_ind.append(mean_relative_error((1.0-wrfles_data[count]['v1m_star']),(1.0-wrfles_data[0]['v1m_star'])))
# wrfles - advanced controller
wrfles_rel_diff_power = []
wrfles_rel_diff_thrust = []
wrfles_rel_diff_torque = []
wrfles_rel_diff_ind = []
for count in range(len(casenames)):
    wrfles_rel_diff_power.append(mean_relative_error(wrfles_data[count]['power_aero'],wrfles_data[0]['power_aero']))
    wrfles_rel_diff_thrust.append(mean_relative_error(wrfles_data[count]['thrust'],wrfles_data[0]['thrust']))
    wrfles_rel_diff_torque.append(mean_relative_error(wrfles_data[count]['torque_aero'],wrfles_data[0]['torque_aero']))
    wrfles_rel_diff_ind.append(mean_relative_error((1.0-wrfles_data[count]['v1m_star']),(1.0-wrfles_data[0]['v1m_star'])))
# # padeops
# padeops_rel_diff_power = []
# padeops_rel_diff_thrust = []
# padeops_rel_diff_ind = []
# for count in range(len(casenames)):
#     padeops_rel_diff_power.append(mean_relative_error(padeops_data[count]['power'][-501:-1],padeops_data[0]['power'][-501:-1]))
#     padeops_rel_diff_thrust.append(mean_relative_error(padeops_data[count]['thrust'][-501:-1],padeops_data[0]['thrust'][-501:-1]))
#     padeops_rel_diff_ind.append(mean_relative_error((1.0-(padeops_data[count]['uvel'][-501:-1]/padeops_data[count]['uinf'])),
#                                                     (1.0-(padeops_data[0]['uvel'][-501:-1]/padeops_data[0]['uinf']))))

width = 0.3

fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(9, 9), sharex=True, constrained_layout = True)
# axial induction factor (1-(u/Uinf))
# ax[0].axhline(0, color='black', linestyle='solid', linewidth=1)
# ind = np.arange(len(casenames))
# for count, name in enumerate(casenames):
#     ax1 = ax[0].bar(ind[count]-width, padeops_rel_diff_ind[count].round(1),
#                     1.*width, color=colors[count], edgecolor='black', alpha=0.6)
#     if(count!=0):
#         ax[0].bar_label(ax1, padding=3, fontsize=13)
ind = np.arange(len(casenames))
for count, name in enumerate(casenames):
    # ax2 = ax[0].bar(ind[count], wrfles_simple_rel_diff_ind[count].round(1),
    #                 1.*width, color=colors[count], edgecolor='black', hatch='..', alpha=0.6)
    ax3 = ax[0].bar(ind[count]+width, wrfles_rel_diff_ind[count].round(1),
                    1.*width, color=colors[count], edgecolor='black', hatch='///', alpha=0.6)
    if(count!=0):
        # ax[0].bar_label(ax2, padding=3, fontsize=13)
        ax[0].bar_label(ax3, padding=3, fontsize=13)
ax[0].set_yticks(np.linspace(0, 0, 1))
ax[0].set_ylim([-11, 11])
ax[0].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{a}}~[\%]$', fontsize=fontsize)
# thrust
ax[1].axhline(0, color='black', linestyle='solid', linewidth=1)
ind = np.arange(len(casenames))
# for count, name in enumerate(casenames):
#     ax1 = ax[1].bar(ind[count]-width, padeops_rel_diff_thrust[count].round(1),
#                     1.*width, color=colors[count], edgecolor='black', alpha=0.6)
#     if(count!=0):
#         ax[1].bar_label(ax1, padding=3, fontsize=13)
ind = np.arange(len(casenames))
for count, name in enumerate(casenames):
    # ax2 = ax[1].bar(ind[count], wrfles_simple_rel_diff_thrust[count].round(1),
    #                 1.*width, color=colors[count], edgecolor='black', hatch='..', alpha=0.6)
    ax3 = ax[1].bar(ind[count]+width, wrfles_rel_diff_thrust[count].round(1),
                    1.*width, color=colors[count], edgecolor='black', hatch='///', alpha=0.6)
    if(count!=0):
        # ax[1].bar_label(ax2, padding=3, fontsize=13)
        ax[1].bar_label(ax3, padding=3, fontsize=13)
ax[1].set_yticks(np.linspace(0, 0, 1))
ax[1].set_ylim([-11, 11])
ax[1].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{T}}~[\%]$', fontsize=fontsize)
# torque
ax[2].axhline(0, color='black', linestyle='solid', linewidth=1)
ind = np.arange(len(casenames))
for count, name in enumerate(casenames):
    # ax2 = ax[2].bar(ind[count], wrfles_simple_rel_diff_torque[count].round(1),
    #                 1.*width, color=colors[count], edgecolor='black', hatch='..', alpha=0.6)
    ax3 = ax[2].bar(ind[count]+width, wrfles_rel_diff_torque[count].round(1),
                    1.*width, color=colors[count], edgecolor='black', hatch='///', alpha=0.6)
    if(count!=0):
        # ax[2].bar_label(ax2, padding=3, fontsize=13)
        ax[2].bar_label(ax3, padding=3, fontsize=13)
ax[2].set_yticks(np.linspace(0, 0, 1))
ax[2].set_ylim([-11, 11])
ax[2].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{Q}}~[\%]$', fontsize=fontsize)
# power
ind = np.arange(len(casenames))
ax[3].axhline(0, color='black', linestyle='solid', linewidth=1)
# for count, name in enumerate(casenames):
    # ax1 = ax[3].bar(ind[count]-width, padeops_rel_diff_power[count].round(1),
    #                 1.*width, color=colors[count], edgecolor='black', alpha=0.6)
    # if(count!=0):
    #     ax[3].bar_label(ax1, padding=3, fontsize=13)
ind = np.arange(len(casenames))
for count, name in enumerate(casenames):
    # ax2 = ax[3].bar(ind[count], wrfles_simple_rel_diff_power[count].round(1),
    #                 1.*width, color=colors[count], edgecolor='black', hatch='..', alpha=0.6)
    ax3 = ax[3].bar(ind[count]+width, wrfles_rel_diff_power[count].round(1),
                    1.*width, color=colors[count], edgecolor='black', hatch='///', alpha=0.6)
    if(count!=0):
        # ax[3].bar_label(ax2, padding=3, fontsize=13)
        ax[3].bar_label(ax3, padding=3, fontsize=13)
ax[3].set_xticks(ind)
ax[3].set_xticklabels(casenames)
ax[3].set_yticks(np.linspace(0, 0, 1))
ax[3].set_ylim([-11, 11])
ax[3].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{P}}~[\%]$', fontsize=fontsize)

if save_figures:
    # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/rel_err_ind_thrust_torque_power.svg", bbox_inches="tight", dpi=100)
    # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/rel_err_ind_thrust_torque_power.pdf", bbox_inches="tight", dpi=300)
    plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/s0_v0/figs/rel_err_ind_thrust_torque_power.png", bbox_inches="tight", dpi=600)
plt.show()
###########################################################################
###########################################################################
###########################################################################
# plot figures
if(plot_figures):
###########################################################################
    # disk-averaged quantities along the blade
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(11, 5), constrained_layout=True)
    
    for count, name in enumerate(casenames):
        ax[0,0].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['aoam'],
                     color=colors[count],linestyle='solid',linewidth=2,label=name)
    ax[0,0].set_xlim([0,1]); ax[0,0].set_ylim([0,60])
    ax[0,0].set_xticks(np.arange(0,1.2,0.2)); ax[0,0].set_yticks(np.arange(0,80,20))
    ax[0,0].axes.xaxis.set_ticklabels([])
    ax[0,0].set_ylabel(r'$\overline{\alpha}~[^{\circ}]$')
    ax[0,0].legend(loc="upper right", fancybox=True, shadow=False, bbox_to_anchor=(1.0, 1.0), ncol=2, fontsize=14)

    for count, name in enumerate(casenames):
        ax[0,1].plot(wrfles_data[count]['rOverR'],(1.0-wrfles_data[count]['v1m_star']),
                     color=colors[count],linestyle='solid',linewidth=2,label=name)
    ax[0,1].set_xlim([0,1]); ax[0,1].set_ylim([0.1,0.4])
    ax[0,1].set_xticks(np.arange(0,1.2,0.2)); ax[0,1].set_yticks(np.arange(0.1,0.5,0.1))
    ax[0,1].axes.xaxis.set_ticklabels([])
    ax[0,1].set_ylabel(r'$\overline{a}=1-\frac{\overline{u}_{m}}{U_{\infty}}~[-]$')
    
    for count, name in enumerate(casenames):
        ax[1,0].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['fd_star'],
                     color=colors[count],linestyle='solid',linewidth=2,label=name)
    ax[1,0].set_xlim([0,1]); ax[1,0].set_ylim([0,0.01])
    ax[1,0].set_xticks(np.arange(0,1.2,0.2)); ax[1,0].set_yticks(np.arange(0,0.0125,0.005))
    ax[1,0].set_ylabel(r'$\overline{F}^{*}_{D}~[-]$'); ax[1,0].set_xlabel(r'$r/R~[-]$')
    
    for count, name in enumerate(casenames):
        ax[1,1].plot(wrfles_data[count]['rOverR'],wrfles_data[count]['fl_star'],
                     color=colors[count],linestyle='solid',linewidth=2,label=name)
    ax[1,1].set_xlim([0,1]); ax[1,1].set_ylim([-0.025,0.6])
    ax[1,1].set_xticks(np.arange(0,1.2,0.2)); ax[1,1].set_yticks(np.arange(0.0,0.8,0.2))
    ax[1,1].set_ylabel(r'$\overline{F}^{*}_{L}~[-]$'); ax[1,1].set_xlabel(r'$r/R~[-]$')

    if save_figures:
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/disk_averaged_quantities.svg", bbox_inches="tight", dpi=100)
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/disk_averaged_quantities.pdf", bbox_inches="tight", dpi=300)
        plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/s0_v0/figs/disk_averaged_quantities.png", bbox_inches="tight", dpi=600)    
    plt.show()
###########################################################################
    # y-z wind speed profile comparison
    fig, ax = plt.subplots(nrows=1, ncols=7, figsize=(16, 6), constrained_layout=True)
    
    # 0D
    for count, name in enumerate(casenames):
        ax[0].plot(wrfles_data[count]['uxyt_0D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[0].plot(padeops_data[count]['uxyt_0D'],(padeops_data[count]['z_av']-padeops_data[count]['hub_height'])/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label=r'_nolegend_')
    ax[0].set_xlim([0.0,1.5]); ax[0].set_ylim([-1.0,1.0])
    ax[0].set_xticks(np.linspace(0.25,1.25,3)); ax[0].set_yticks(np.linspace(-1,1.0,5))
    ax[0].grid(True, 'major', alpha=0.2)
    ax[0].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize); ax[0].set_ylabel(r'$z/D~[-]$',fontsize=fontsize)
    ax[0].set_title(r'$x/D=0$')
    ax[0].legend(loc="upper center", fancybox=True, shadow=False, framealpha=0.5, bbox_to_anchor=(0.675, 0.6), ncol=1, fontsize=12)
    
    # 1D
    for count, name in enumerate(casenames):
        ax[1].plot(wrfles_data[count]['uxyt_1D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[1].plot(padeops_data[count]['uxyt_1D'],(padeops_data[count]['z_av']-padeops_data[count]['hub_height'])/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label=r'_nolegend_')
    ax[1].set_xlim([0.0,1.5]); ax[1].set_ylim([-1.0,1.0])
    ax[1].set_xticks(np.linspace(0.25,1.25,3)); ax[1].set_yticks(np.linspace(-1,1.0,5))
    ax[1].grid(True, 'major', alpha=0.2)
    ax[1].axes.yaxis.set_ticklabels([])
    ax[1].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
    ax[1].set_title(r'$x/D=1$')
    
    # 3D
    for count, name in enumerate(casenames):
        ax[2].plot(wrfles_data[count]['uxyt_3D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[2].plot(padeops_data[count]['uxyt_3D'],(padeops_data[count]['z_av']-padeops_data[count]['hub_height'])/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label=r'_nolegend_')
    ax[2].set_xlim([0.0,1.5]); ax[2].set_ylim([-1.0,1.0])
    ax[2].set_xticks(np.linspace(0.25,1.25,3)); ax[2].set_yticks(np.linspace(-1,1.0,5))
    ax[2].grid(True, 'major', alpha=0.2)
    ax[2].axes.yaxis.set_ticklabels([])
    ax[2].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)   
    ax[2].set_title(r'$x/D=3$')
    
    # 6D
    for count, name in enumerate(casenames):
        ax[3].plot(wrfles_data[count]['uxyt_6D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[3].plot(padeops_data[count]['uxyt_6D'],(padeops_data[count]['z_av']-padeops_data[count]['hub_height'])/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label=r'_nolegend_')
    ax[3].set_xlim([0.0,1.5]); ax[3].set_ylim([-1.0,1.0])
    ax[3].set_xticks(np.linspace(0.25,1.25,3)); ax[3].set_yticks(np.linspace(-1,1.0,5))
    ax[3].grid(True, 'major', alpha=0.2)
    ax[3].axes.yaxis.set_ticklabels([])
    ax[3].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)  
    ax[3].set_title(r'$x/D=6$')
    
    # 9D
    for count, name in enumerate(casenames):
        ax[4].plot(wrfles_data[count]['uxyt_9D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[4].plot(padeops_data[count]['uxyt_9D'],(padeops_data[count]['z_av']-padeops_data[count]['hub_height'])/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label=r'_nolegend_')
    ax[4].set_xlim([0.0,1.5]); ax[4].set_ylim([-1.0,1.0])
    ax[4].set_xticks(np.linspace(0.25,1.25,3)); ax[4].set_yticks(np.linspace(-1,1.0,5))
    ax[4].grid(True, 'major', alpha=0.2)
    ax[4].axes.yaxis.set_ticklabels([])
    ax[4].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
    ax[4].set_title(r'$x/D=9$')
    
    # 12D
    for count, name in enumerate(casenames):
        ax[5].plot(wrfles_data[count]['uxyt_12D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[5].plot(padeops_data[count]['uxyt_12D'],(padeops_data[count]['z_av']-padeops_data[count]['hub_height'])/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label=r'_nolegend_')
    ax[5].set_xlim([0.0,1.5]); ax[5].set_ylim([-1.0,1.0])
    ax[5].set_xticks(np.linspace(0.25,1.25,3)); ax[5].set_yticks(np.linspace(-1,1.0,5))
    ax[5].grid(True, 'major', alpha=0.2)
    ax[5].axes.yaxis.set_ticklabels([])
    ax[5].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize) 
    ax[5].set_title(r'$x/D=12$')
    
    # # 15D
    # for count, name in enumerate(casenames):
    #     ax[6].plot(wrfles_data[count]['uxyt_15D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
    #                color=colors[count],linestyle='solid',linewidth=2,label=name)
    #     ax[6].plot(padeops_data[count]['uxyt_15D'],(padeops_data[count]['z_av']-padeops_data[count]['hub_height'])/padeops_data[count]['diameter'],
    #                color=colors[count],linestyle='dashed',linewidth=2,label=r'_nolegend_')
    # ax[6].set_xlim([0.0,1.5]); ax[6].set_ylim([-1.0,1.0])
    # ax[6].set_xticks(np.linspace(0.25,1.25,3)); ax[6].set_yticks(np.linspace(-1,1.0,5))
    # ax[6].grid(True, 'major', alpha=0.2)
    # ax[6].axes.yaxis.set_ticklabels([])
    # ax[6].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize)    
    # ax[6].set_title(r'$x/D=15$')

    if save_figures:
    #     plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/ux_z.svg", bbox_inches="tight", dpi=100)
    #     plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/ux_z.pdf", bbox_inches="tight", dpi=300)
        plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/s0_v0/figs/ux_z.png", bbox_inches="tight", dpi=600)    
    plt.show()
###########################################################################
    # x-y wind speed profile comparison
    ycorr=-5.0
    fig, ax = plt.subplots(nrows=1, ncols=7, figsize=(16, 6), constrained_layout=True)
    
    # 0D
    for count, name in enumerate(casenames):
        ax[0].plot(wrfles_data[count]['uxzt_0D'],(wrfles_data[count]['Y2'][:,0]-wrfles_data[count]['rotor_yloc'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[0].plot(padeops_data[count]['uxzt_0D'],(padeops_data[count]['Y2'][:,0]-padeops_data[count]['rotor_yloc']+ycorr)/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label='_nolegend_')
    ax[0].set_xlim([0.0,1.5]); ax[0].set_ylim([-1.0,1.0])
    ax[0].set_xticks(np.linspace(0.25,1.25,3)); ax[0].set_yticks(np.linspace(-1,1.0,5))
    ax[0].grid(True, 'major', alpha=0.2)
    ax[0].set_xlabel(r'$\overline{u}/U_{\infty}~[-]$',fontsize=fontsize); ax[0].set_ylabel(r'$y/D~[-]$',fontsize=fontsize)
    ax[0].set_title(r'$x/D=0$')
    # ax[0].legend(loc="upper center", fancybox=True, shadow=False, framealpha=0.5, bbox_to_anchor=(0.675, 0.6), ncol=1, fontsize=12)
    
    # 1D
    for count, name in enumerate(casenames):
        ax[1].plot(wrfles_data[count]['uxzt_1D'],(wrfles_data[count]['Y2'][:,0]-wrfles_data[count]['rotor_yloc'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[1].plot(padeops_data[count]['uxzt_1D'],(padeops_data[count]['Y2'][:,0]-padeops_data[count]['rotor_yloc']+ycorr)/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label='_nolegend_')
    ax[1].set_xlim([0.0,1.5]); ax[1].set_ylim([-1.0,1.0])
    ax[1].set_xticks(np.linspace(0.25,1.25,3)); ax[1].set_yticks(np.linspace(-1,1.0,5))
    ax[1].grid(True, 'major', alpha=0.2)
    ax[1].axes.yaxis.set_ticklabels([])
    ax[1].set_xlabel(r'$\overline{u}/\overline{U}_{\infty}~[-]$',fontsize=fontsize)  
    ax[1].set_title(r'$x/D=1$')
    
    # 3D
    for count, name in enumerate(casenames):
        ax[2].plot(wrfles_data[count]['uxzt_3D'],(wrfles_data[count]['Y2'][:,0]-wrfles_data[count]['rotor_yloc'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[2].plot(padeops_data[count]['uxzt_3D'],(padeops_data[count]['Y2'][:,0]-padeops_data[count]['rotor_yloc']+ycorr)/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label='_nolegend_')
    ax[2].set_xlim([0.25,1.75]); ax[2].set_ylim([-1.0,1.0])
    ax[2].set_xticks(np.linspace(0.5,1.5,3)); ax[2].set_yticks(np.linspace(-1,1.0,5))
    ax[2].grid(True, 'major', alpha=0.2)
    ax[2].axes.yaxis.set_ticklabels([])
    ax[2].set_xlabel(r'$\overline{u}/\overline{U}_{\infty}~[-]$',fontsize=fontsize)   
    ax[2].set_title(r'$x/D=3$')
    
    # 6D
    for count, name in enumerate(casenames):
        ax[3].plot(wrfles_data[count]['uxzt_6D'],(wrfles_data[count]['Y2'][:,0]-wrfles_data[count]['rotor_yloc'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[3].plot(padeops_data[count]['uxzt_6D'],(padeops_data[count]['Y2'][:,0]-padeops_data[count]['rotor_yloc']+ycorr)/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label='_nolegend_')
    ax[3].set_xlim([0.0,1.5]); ax[3].set_ylim([-1.0,1.0])
    ax[3].set_xticks(np.linspace(0.25,1.25,3)); ax[3].set_yticks(np.linspace(-1,1.0,5))
    ax[3].grid(True, 'major', alpha=0.2)
    ax[3].axes.yaxis.set_ticklabels([])
    ax[3].set_xlabel(r'$\overline{u}/\overline{U}_{\infty}~[-]$',fontsize=fontsize)  
    ax[3].set_title(r'$x/D=6$')
    
    # 9D
    for count, name in enumerate(casenames):
        ax[4].plot(wrfles_data[count]['uxzt_9D'],(wrfles_data[count]['Y2'][:,0]-wrfles_data[count]['rotor_yloc'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[4].plot(padeops_data[count]['uxzt_9D'],(padeops_data[count]['Y2'][:,0]-padeops_data[count]['rotor_yloc']+ycorr)/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label='_nolegend_')
    ax[4].set_xlim([0.0,1.5]); ax[4].set_ylim([-1.0,1.0])
    ax[4].set_xticks(np.linspace(0.25,1.25,3)); ax[4].set_yticks(np.linspace(-1,1.0,5))
    ax[4].grid(True, 'major', alpha=0.2)
    ax[4].axes.yaxis.set_ticklabels([])
    ax[4].set_xlabel(r'$\overline{u}/\overline{U}_{\infty}~[-]$',fontsize=fontsize) 
    ax[4].set_title(r'$x/D=9$')
    
    # 12D
    for count, name in enumerate(casenames):
        ax[5].plot(wrfles_data[count]['uxzt_12D'],(wrfles_data[count]['Y2'][:,0]-wrfles_data[count]['rotor_yloc'])/wrfles_data[count]['diameter'],
                   color=colors[count],linestyle='solid',linewidth=2,label=name)
        # ax[5].plot(padeops_data[count]['uxzt_12D'],(padeops_data[count]['Y2'][:,0]-padeops_data[count]['rotor_yloc']+ycorr)/padeops_data[count]['diameter'],
        #            color=colors[count],linestyle='dashed',linewidth=2,label='_nolegend_')
    ax[5].set_xlim([0.0,1.5]); ax[5].set_ylim([-1.0,1.0])
    ax[5].set_xticks(np.linspace(0.25,1.25,3)); ax[5].set_yticks(np.linspace(-1,1.0,5))
    ax[5].grid(True, 'major', alpha=0.2)
    ax[5].axes.yaxis.set_ticklabels([])
    ax[5].set_xlabel(r'$\overline{u}/\overline{U}_{\infty}~[-]$',fontsize=fontsize) 
    ax[5].set_title(r'$x/D=12$')
    
    # 15D
    # for count, name in enumerate(casenames):
    #     ax[6].plot(wrfles_data[count]['uxzt_15D'],(wrfles_data[count]['Y2'][:,0]-wrfles_data[count]['rotor_yloc'])/wrfles_data[count]['diameter'],
    #                color=colors[count],linestyle='solid',linewidth=2,label=name)
    #     # ax[6].plot(padeops_data[count]['uxzt_15D'],(padeops_data[count]['Y2'][:,0]-padeops_data[count]['rotor_yloc']+ycorr)/padeops_data[count]['diameter'],
    #     #            color=colors[count],linestyle='dashed',linewidth=2,label='_nolegend_')
    # ax[6].set_xlim([0.0,1.5]); ax[6].set_ylim([-1.0,1.0])
    # ax[6].set_xticks(np.linspace(0.25,1.25,3)); ax[6].set_yticks(np.linspace(-1,1.0,5))
    # ax[6].grid(True, 'major', alpha=0.2)
    # ax[6].axes.yaxis.set_ticklabels([])
    # ax[6].set_xlabel(r'$\overline{u}/\overline{U}_{\infty}~[-]$',fontsize=fontsize)    
    # ax[6].set_title(r'$x/D=15$')
    
    if save_figures:
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/uy_z.svg", bbox_inches="tight", dpi=100)
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/uy_z.pdf", bbox_inches="tight", dpi=300)
        plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/s0_v0/figs/uy_z.png", bbox_inches="tight", dpi=600)
    plt.show()
###########################################################################
    # longitudinal component of reynolds stress comparison
    fig, ax = plt.subplots(nrows=1, ncols=7, figsize=(16, 6), constrained_layout=True)
    
    # 0D
    for count, name in enumerate(casenames):
        ax[0].semilogx(wrfles_data[count]['uupxyt_0D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                       color=colors[count],linestyle='solid',linewidth=2,label=name)
    ax[0].set_xlim([1E-12,1E0]); ax[0].set_ylim([-0.75,0.75])
    ax[0].set_xticks(np.logspace(-10,-2,3)); ax[0].set_yticks(np.linspace(-0.5,0.5,3))
    ax[0].set_xlabel(r'$\overline{u^{\prime}u^{\prime}}/U^{2}_{\infty}~[-]$',fontsize=fontsize); ax[0].set_ylabel(r'$z/D~[-]$',fontsize=fontsize)
    ax[0].set_title(r'$x/D=0$')
    
    # 1D
    for count, name in enumerate(casenames):
        ax[1].semilogx(wrfles_data[count]['uupxyt_1D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                       color=colors[count],linestyle='solid',linewidth=2,label=name)
    ax[1].set_xlim([1E-12,1E0]); ax[1].set_ylim([-0.75,0.75])
    ax[1].set_xticks(np.logspace(-10,-2,3)); ax[1].set_yticks(np.linspace(-0.5,0.5,3))
    ax[1].axes.yaxis.set_ticklabels([])
    ax[1].set_xlabel(r'$\overline{u^{\prime}u^{\prime}}/U^{2}_{\infty}~[-]$',fontsize=fontsize)  
    ax[1].set_title(r'$x/D=1$')
    
    # 3D
    for count, name in enumerate(casenames):
        ax[2].semilogx(wrfles_data[count]['uupxyt_3D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                       color=colors[count],linestyle='solid',linewidth=2,label=name)
    ax[2].set_xlim([1E-12,1E0]); ax[2].set_ylim([-0.75,0.75])
    ax[2].set_xticks(np.logspace(-10,-2,3)); ax[2].set_yticks(np.linspace(-0.5,0.5,3))
    ax[2].axes.yaxis.set_ticklabels([])
    ax[2].set_xlabel(r'$\overline{u^{\prime}u^{\prime}}/U^{2}_{\infty}~[-]$',fontsize=fontsize)   
    ax[2].set_title(r'$x/D=3$')
    
    # 6D
    for count, name in enumerate(casenames):
        ax[3].semilogx(wrfles_data[count]['uupxyt_6D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                       color=colors[count],linestyle='solid',linewidth=2,label=name)
    ax[3].set_xlim([1E-12,1E0]); ax[3].set_ylim([-0.75,0.75])
    ax[3].set_xticks(np.logspace(-10,-2,3)); ax[3].set_yticks(np.linspace(-0.5,0.5,3))
    ax[3].axes.yaxis.set_ticklabels([])
    ax[3].set_xlabel(r'$\overline{u^{\prime}u^{\prime}}/U^{2}_{\infty}~[-]$',fontsize=fontsize)  
    ax[3].set_title(r'$x/D=6$')
    
    # 9D
    for count, name in enumerate(casenames):
        ax[4].semilogx(wrfles_data[count]['uupxyt_9D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                       color=colors[count],linestyle='solid',linewidth=2,label=name)
    ax[4].set_xlim([1E-12,1E0]); ax[4].set_ylim([-0.75,0.75])
    ax[4].set_xticks(np.logspace(-10,-2,3)); ax[4].set_yticks(np.linspace(-0.5,0.5,3))
    ax[4].axes.yaxis.set_ticklabels([])
    ax[4].set_xlabel(r'$\overline{u^{\prime}u^{\prime}}/U^{2}_{\infty}~[-]$',fontsize=fontsize) 
    ax[4].set_title(r'$x/D=9$')
    
    # 12D
    for count, name in enumerate(casenames):
        ax[5].semilogx(wrfles_data[count]['uupxyt_12D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
                       color=colors[count],linestyle='solid',linewidth=2,label=name)
    ax[5].set_xlim([1E-10,1E0]); ax[5].set_ylim([-0.75,0.75])
    ax[5].set_xticks(np.logspace(-8,-2,3)); ax[5].set_yticks(np.linspace(-0.5,0.5,3))
    ax[5].axes.yaxis.set_ticklabels([])
    ax[5].set_xlabel(r'$\overline{u^{\prime}u^{\prime}}/U^{2}_{\infty}~[-]$',fontsize=fontsize) 
    ax[5].set_title(r'$x/D=12$')
    
    # 15D
    # for count, name in enumerate(casenames):
    #     ax[6].semilogx(wrfles_data[count]['uupxyt_15D'],(wrfles_data[count]['z_av']-wrfles_data[count]['hub_height'])/wrfles_data[count]['diameter'],
    #                    color=colors[count],linestyle='solid',linewidth=2,label=name)
    # ax[6].set_xlim([1E-10,1E0]); ax[6].set_ylim([-0.75,0.75])
    # ax[6].set_xticks(np.logspace(-8,-2,3)); ax[6].set_yticks(np.linspace(-0.5,0.5,3))
    # ax[6].axes.yaxis.set_ticklabels([])
    # ax[6].set_xlabel(r'$\overline{u^{\prime}u^{\prime}}/U^{2}_{\infty}~[-]$',fontsize=fontsize)    
    # ax[6].set_title(r'$x/D=15$')
    
    if save_figures:
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/upup_rs_z.svg", bbox_inches="tight", dpi=100)
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/upup_rs_z.pdf", bbox_inches="tight", dpi=300)
        plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/s0_v0/figs/upup_rs_z.png", bbox_inches="tight", dpi=600)
    plt.show()
###########################################################################
    # # relative difference
    # # wrfles - simple controller
    # wrfles_simple_rel_diff_power = []
    # wrfles_simple_rel_diff_thrust = []
    # wrfles_simple_rel_diff_torque = []
    # wrfles_simple_rel_diff_ind = []
    # for count in range(len(casenames)):
    #     wrfles_simple_rel_diff_power.append(mean_relative_error(wrfles_data_simple[count]['power_aero'],wrfles_data_simple[0]['power_aero']))
    #     wrfles_simple_rel_diff_thrust.append(mean_relative_error(wrfles_data_simple[count]['thrust'],wrfles_data_simple[0]['thrust']))
    #     wrfles_simple_rel_diff_torque.append(mean_relative_error(wrfles_data_simple[count]['torque_aero'],wrfles_data_simple[0]['torque_aero']))
    #     wrfles_simple_rel_diff_ind.append(mean_relative_error((1.0-wrfles_data_simple[count]['v1m_star']),(1.0-wrfles_data_simple[0]['v1m_star'])))
    # # wrfles - advanced controller
    # wrfles_rel_diff_power = []
    # wrfles_rel_diff_thrust = []
    # wrfles_rel_diff_torque = []
    # wrfles_rel_diff_ind = []
    # for count in range(len(casenames)):
    #     wrfles_rel_diff_power.append(mean_relative_error(wrfles_data[count]['power_aero'],wrfles_data[0]['power_aero']))
    #     wrfles_rel_diff_thrust.append(mean_relative_error(wrfles_data[count]['thrust'],wrfles_data[0]['thrust']))
    #     wrfles_rel_diff_torque.append(mean_relative_error(wrfles_data[count]['torque_aero'],wrfles_data[0]['torque_aero']))
    #     wrfles_rel_diff_ind.append(mean_relative_error((1.0-wrfles_data[count]['v1m_star']),(1.0-wrfles_data[0]['v1m_star'])))
    # # padeops
    # padeops_rel_diff_power = []
    # padeops_rel_diff_thrust = []
    # padeops_rel_diff_ind = []
    # for count in range(len(casenames)):
    #     padeops_rel_diff_power.append(mean_relative_error(padeops_data[count]['power'][-501:-1],padeops_data[0]['power'][-501:-1]))
    #     padeops_rel_diff_thrust.append(mean_relative_error(padeops_data[count]['thrust'][-501:-1],padeops_data[0]['thrust'][-501:-1]))
    #     padeops_rel_diff_ind.append(mean_relative_error((1.0-(padeops_data[count]['uvel'][-501:-1]/padeops_data[count]['uinf'])),
    #                                                     (1.0-(padeops_data[0]['uvel'][-501:-1]/padeops_data[0]['uinf']))))
    
    ind = np.arange(len(casenames))
    width = 0.3

    fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(8, 9), sharex=True, constrained_layout = True)
    # axial induction factor (1-(u/Uinf))
    ax[0].axhline(0, color='black', linestyle='solid', linewidth=1)
    for count, name in enumerate(casenames):
        # ax1 = ax[0].bar(ind[count]-width, padeops_rel_diff_ind[count].round(1),
        #                 1.*width, color=colors[count], edgecolor='black', alpha=0.6)
        # ax2 = ax[0].bar(ind[count], wrfles_simple_rel_diff_ind[count].round(1),
        #                 1.*width, color=colors[count], edgecolor='black', hatch='..', alpha=0.6)
        ax3 = ax[0].bar(ind[count]+width, wrfles_rel_diff_ind[count].round(1),
                        1.*width, color=colors[count], edgecolor='black', hatch='///', alpha=0.6)
        if(count!=0):
            ax[0].bar_label(ax1, padding=3, fontsize=13)
            ax[0].bar_label(ax2, padding=3, fontsize=13)
            ax[0].bar_label(ax3, padding=3, fontsize=13)
    ax[0].set_yticks(np.linspace(0, 0, 1))
    ax[0].set_ylim([-11, 11])
    ax[0].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{a}}~[\%]$', fontsize=fontsize)
    # thrust
    ax[1].axhline(0, color='black', linestyle='solid', linewidth=1)
    for count, name in enumerate(casenames):
        # ax1 = ax[1].bar(ind[count]-width, padeops_rel_diff_thrust[count].round(1),
        #                 1.*width, color=colors[count], edgecolor='black', alpha=0.6)
        # ax2 = ax[1].bar(ind[count], wrfles_simple_rel_diff_thrust[count].round(1),
        #                 1.*width, color=colors[count], edgecolor='black', hatch='..', alpha=0.6)
        ax3 = ax[1].bar(ind[count]+width, wrfles_rel_diff_thrust[count].round(1),
                        1.*width, color=colors[count], edgecolor='black', hatch='///', alpha=0.6)
        if(count!=0):
            ax[1].bar_label(ax1, padding=3, fontsize=13)
            ax[1].bar_label(ax2, padding=3, fontsize=13)
            ax[1].bar_label(ax3, padding=3, fontsize=13)
    ax[1].set_yticks(np.linspace(0, 0, 1))
    ax[1].set_ylim([-11, 11])
    ax[1].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{T}}~[\%]$', fontsize=fontsize)
    # torque
    ax[2].axhline(0, color='black', linestyle='solid', linewidth=1)
    for count, name in enumerate(casenames):
        # ax2 = ax[2].bar(ind[count], wrfles_simple_rel_diff_torque[count].round(1),
        #                 1.*width, color=colors[count], edgecolor='black', hatch='..', alpha=0.6)
        ax3 = ax[2].bar(ind[count]+width, wrfles_rel_diff_torque[count].round(1),
                        1.*width, color=colors[count], edgecolor='black', hatch='///', alpha=0.6)
        if(count!=0):
            ax[2].bar_label(ax2, padding=3, fontsize=13)
            ax[2].bar_label(ax3, padding=3, fontsize=13)
    ax[2].set_yticks(np.linspace(0, 0, 1))
    ax[2].set_ylim([-11, 11])
    ax[2].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{Q}}~[\%]$', fontsize=fontsize)
    # power
    ax[3].axhline(0, color='black', linestyle='solid', linewidth=1)
    for count, name in enumerate(casenames):
        # ax1 = ax[3].bar(ind[count]-width, padeops_rel_diff_power[count].round(1),
        #                 1.*width, color=colors[count], edgecolor='black', alpha=0.6)
        # ax2 = ax[3].bar(ind[count], wrfles_simple_rel_diff_power[count].round(1),
        #                 1.*width, color=colors[count], edgecolor='black', hatch='..', alpha=0.6)
        ax3 = ax[3].bar(ind[count]+width, wrfles_rel_diff_power[count].round(1),
                        1.*width, color=colors[count], edgecolor='black', hatch='///', alpha=0.6)
        if(count!=0):
            ax[3].bar_label(ax1, padding=3, fontsize=13)
            ax[3].bar_label(ax2, padding=3, fontsize=13)
            ax[3].bar_label(ax3, padding=3, fontsize=13)
    ax[3].set_xticks(ind)
    ax[3].set_xticklabels(casenames)
    ax[3].set_yticks(np.linspace(0, 0, 1))
    ax[3].set_ylim([-11, 11])
    ax[3].set_ylabel(r'$\mathrm{\mathbb{E}}_{\overline{P}}~[\%]$', fontsize=fontsize)
    
    if save_figures:
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/rel_err_ind_thrust_torque_power.svg", bbox_inches="tight", dpi=100)
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/rel_err_ind_thrust_torque_power.pdf", bbox_inches="tight", dpi=300)
        plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/s0_v0/figs/rel_err_ind_thrust_torque_power.png", bbox_inches="tight", dpi=600)
    plt.show()
###########################################################################
    ks = 35
    ke = 65
    js = 75
    je = 125
    
    ij = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2]]
    
    levels = 101; vmin = 0.5; vmax = 1.0
###########################################################################
    # streamwise velocity component
    # wrfles
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
        ax[i,j].set_xlim3d([-100, 2000])
        ax[i,j].set_ylim3d([750.0, 1250.0])
        ax[i,j].set_zlim3d([350.0, 650.0])
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
    if save_figures:
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/wrfles_uvel_slice_yz.svg", bbox_inches="tight", dpi=100)
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/wrfles_uvel_slice_yz.pdf", bbox_inches="tight", dpi=300)
        plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/s0_v0/figs/wrfles_uvel_slice_yz.png", bbox_inches="tight", dpi=600)
    plt.show()
    
    # # padeops
    # fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12,8), subplot_kw={"projection": "3d"}, constrained_layout=True)

    # for count, name in enumerate(casenames):
    #     i = ij[count][0]; j = ij[count][1]
    #     ax[i,j].set_box_aspect(aspect=(40,8,8))
    #     ax[i,j].contourf(padeops_data[count]['ux_0D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                      padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                      padeops_data[count]['Z3'].transpose()[js:je,ks:ke],
    #                      levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                      vmin=vmin, vmax=vmax, zdir='x', offset=0*padeops_data[count]['diameter'])
    #     ax[i,j].contourf(padeops_data[count]['ux_3D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                      padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                      padeops_data[count]['Z3'].transpose()[js:je,ks:ke],
    #                      levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                      vmin=vmin, vmax=vmax, zdir='x', offset=3*padeops_data[count]['diameter'])
    #     ax[i,j].contourf(padeops_data[count]['ux_6D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                      padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                      padeops_data[count]['Z3'].transpose()[js:je,ks:ke],
    #                      levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                      vmin=vmin, vmax=vmax, zdir='x', offset=6*padeops_data[count]['diameter'])
    #     ax[i,j].contourf(padeops_data[count]['ux_9D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                      padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                      padeops_data[count]['Z3'].transpose()[js:je,ks:ke],
    #                      levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                      vmin=vmin, vmax=vmax, zdir='x', offset=9*padeops_data[count]['diameter'])
    #     ax[i,j].contourf(padeops_data[count]['ux_12D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                      padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                      padeops_data[count]['Z3'].transpose()[js:je,ks:ke],
    #                      levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                      vmin=vmin, vmax=vmax, zdir='x', offset=12*padeops_data[count]['diameter'])
    #     cs = ax[i,j].contourf(padeops_data[count]['ux_15D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                           padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                           padeops_data[count]['Z3'].transpose()[js:je,ks:ke], 
    #                           levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                           vmin=vmin, vmax=vmax, zdir='x', offset=15*padeops_data[count]['diameter'])
    #     # Set the azimuth and elevation angles
    #     ax[i,j].view_init(azim=225, elev=30, roll=0)
    #     ax[i,j].set_xlim3d([-100, 2000])
    #     ax[i,j].set_ylim3d([750.0, 1250.0])
    #     ax[i,j].set_zlim3d([350.0, 650.0])
    #     ax[i,j].set_xticks(np.arange(0, 18*wrfles_data[count]['diameter'], 3*wrfles_data[count]['diameter']))
    #     ax[i,j].set_xticklabels([r'$0D$', r'$3D$', r'$6D$', r'$9D$', r'$12D$', r'$15D$'], fontsize=14)
    #     ax[i,j].tick_params(axis='x', labelrotation=-90)
    #     ax[i,j].set_yticks(np.linspace(wrfles_data[count]['rotor_yloc'], wrfles_data[count]['rotor_yloc'], 1))
    #     ax[i,j].set_yticklabels([r'$0D$'], fontsize=14)
    #     ax[i,j].tick_params(axis='y', labelrotation=-30)
    #     ax[i,j].set_zticks(np.linspace(wrfles_data[count]['hub_height'], wrfles_data[count]['hub_height'], 1))
    #     ax[i,j].set_zticklabels([r'$0D$'], fontsize=14)
    #     ax[i,j].tick_params(axis='z', labelrotation=-90)
    #     ax[i,j].xaxis.labelpad=50
    #     ax[i,j].yaxis.labelpad=-5
    #     ax[i,j].zaxis.labelpad=-5
    #     ax[i,j].yaxis.set_tick_params(pad=-5)
    #     ax[i,j].zaxis.set_tick_params(pad=-1)
    #     ax[i,j].set(xlabel=r'$x~[\textrm{m}]$', ylabel=r'$y~[\textrm{m}]$', zlabel=r'$z~[\textrm{m}]$')
    #     ax[i,j].set_title(casenames[count], fontsize=24, y=0.85)
    # fig.colorbar(cs, ax=[ax[0,0], ax[0,1], ax[0,2], ax[1,0], ax[1,1], ax[1,2]],
    #              ticks=np.linspace(vmin,vmax,6,endpoint=True),
    #              label=r'$\overline{u}/U_{\infty}~[-]$',
    #              aspect=75, pad=0.02, orientation='horizontal')
    # # for c in cs.collections:
    # #     c.set_edgecolor("face")
    # if save_figures:
    #     plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/padeops_uvel_slice_yz.svg", bbox_inches="tight", dpi=100)
    #     plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/padeops_uvel_slice_yz.pdf", bbox_inches="tight", dpi=300)
    #     plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/png/padeops_uvel_slice_yz.png", bbox_inches="tight", dpi=600)
    # plt.show()
###########################################################################
    # spanwise velocity component
    ij = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2]]
    
    levels = 101; vmin_s = -0.08; vmax_s = 0.08; vmin_v = -0.4; vmax_v = 0.4
###########################################################################
    # wrfles
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(11,8), subplot_kw={"projection": "3d"}, constrained_layout=True)

    for count, name in enumerate(casenames):
        if(count<3):
            vmin = vmin_s; vmax = vmax_s
        else:
            vmin = vmin_v; vmax = vmax_v
        i = ij[count][0]; j = ij[count][1]
        ax[i,j].set_box_aspect(aspect=(40,8,8))
        ax[i,j].contourf(np.mean(wrfles_data[count]['vx_0D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                         wrfles_data[count]['Y3'][ks:ke,js:je],
                         wrfles_data[count]['Z3'][ks:ke,js:je],
                         levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                         vmin=vmin, vmax=vmax, zdir='x', offset=0*wrfles_data[count]['diameter'])
        ax[i,j].contourf(np.mean(wrfles_data[count]['vx_3D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                         wrfles_data[count]['Y3'][ks:ke,js:je],
                         wrfles_data[count]['Z3'][ks:ke,js:je],
                         levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                         vmin=vmin, vmax=vmax, zdir='x', offset=3*wrfles_data[count]['diameter'])
        cs1 = ax[i,j].contourf(np.mean(wrfles_data[count]['vx_6D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                               wrfles_data[count]['Y3'][ks:ke,js:je],
                               wrfles_data[count]['Z3'][ks:ke,js:je],
                               levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                               vmin=vmin, vmax=vmax, zdir='x', offset=6*wrfles_data[count]['diameter'])
        ax[i,j].contourf(np.mean(wrfles_data[count]['vx_9D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                         wrfles_data[count]['Y3'][ks:ke,js:je],
                         wrfles_data[count]['Z3'][ks:ke,js:je],
                         levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                         vmin=vmin, vmax=vmax, zdir='x', offset=9*wrfles_data[count]['diameter'])
        ax[i,j].contourf(np.mean(wrfles_data[count]['vx_12D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                         wrfles_data[count]['Y3'][ks:ke,js:je],
                         wrfles_data[count]['Z3'][ks:ke,js:je],
                         levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                         vmin=vmin, vmax=vmax, zdir='x', offset=12*wrfles_data[count]['diameter'])
        cs2 = ax[i,j].contourf(np.mean(wrfles_data[count]['vx_15D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'],
                               wrfles_data[count]['Y3'][ks:ke,js:je],
                               wrfles_data[count]['Z3'][ks:ke,js:je], 
                               levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
                               vmin=vmin, vmax=vmax, zdir='x', offset=15*wrfles_data[count]['diameter'])
        # Set the azimuth and elevation angles
        ax[i,j].view_init(azim=225, elev=30, roll=0)
        ax[i,j].set_xlim3d([-100, 2000])
        ax[i,j].set_ylim3d([750.0, 1250.0])
        ax[i,j].set_zlim3d([178.0, 578.0])
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
        if(count==2):
            fig.colorbar(cs1, ax=[ax[0,0], ax[0,1], ax[0,2]],
                        ticks=np.linspace(vmin_s,vmax_s,5,endpoint=True),
                        label=r'$\overline{v}/U_{\infty}~[-]$',
                        aspect=75, pad=0.02, orientation='horizontal')
        if(count==5):
            fig.colorbar(cs2, ax=[ax[1,0], ax[1,1], ax[1,2]],
                        ticks=np.linspace(vmin_v,vmax_v,5,endpoint=True),
                        label=r'$\overline{v}/U_{\infty}~[-]$',
                        aspect=75, pad=0.02, orientation='horizontal')
    # for c in cs.collections:
    #     c.set_edgecolor("face")
    if save_figures:
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/wrfles_vvel_slice_yz.svg", bbox_inches="tight", dpi=100)
        # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/wrfles_vvel_slice_yz.pdf", bbox_inches="tight", dpi=300)
        plt.savefig("/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/s0_v0/figs/wrfles_vvel_slice_yz.png", bbox_inches="tight", dpi=600)
    plt.show()
    
    # # padeops
    # fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(11,8), subplot_kw={"projection": "3d"}, constrained_layout=True)

    # for count, name in enumerate(casenames):
    #     if(count<3):
    #         vmin = vmin_s; vmax = vmax_s
    #     else:
    #         vmin = vmin_v; vmax = vmax_v
    #     i = ij[count][0]; j = ij[count][1]
    #     ax[i,j].set_box_aspect(aspect=(40,8,8))
    #     ax[i,j].contourf(padeops_data[count]['vx_0D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                      padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                      padeops_data[count]['Z3'].transpose()[js:je,ks:ke],
    #                      levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                      vmin=vmin, vmax=vmax, zdir='x', offset=0*padeops_data[count]['diameter'])
    #     ax[i,j].contourf(padeops_data[count]['vx_3D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                      padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                      padeops_data[count]['Z3'].transpose()[js:je,ks:ke],
    #                      levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                      vmin=vmin, vmax=vmax, zdir='x', offset=3*padeops_data[count]['diameter'])
    #     cs1 = ax[i,j].contourf(padeops_data[count]['vx_6D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                            padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                            padeops_data[count]['Z3'].transpose()[js:je,ks:ke],
    #                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                            vmin=vmin, vmax=vmax, zdir='x', offset=6*padeops_data[count]['diameter'])
    #     ax[i,j].contourf(padeops_data[count]['vx_9D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                      padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                      padeops_data[count]['Z3'].transpose()[js:je,ks:ke],
    #                      levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                      vmin=vmin, vmax=vmax, zdir='x', offset=9*padeops_data[count]['diameter'])
    #     ax[i,j].contourf(padeops_data[count]['vx_12D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                      padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                      padeops_data[count]['Z3'].transpose()[js:je,ks:ke],
    #                      levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                      vmin=vmin, vmax=vmax, zdir='x', offset=12*padeops_data[count]['diameter'])
    #     cs2 = ax[i,j].contourf(padeops_data[count]['vx_15D'][js:je,ks:ke]/padeops_data[count]['uinf'],
    #                            padeops_data[count]['Y3'].transpose()[js:je,ks:ke],
    #                            padeops_data[count]['Z3'].transpose()[js:je,ks:ke], 
    #                            levels=np.linspace(vmin, vmax, levels, endpoint=True), extend='both',
    #                            vmin=vmin, vmax=vmax, zdir='x', offset=15*padeops_data[count]['diameter'])
    #     # Set the azimuth and elevation angles
    #     ax[i,j].view_init(azim=225, elev=30, roll=0)
    #     ax[i,j].set_xlim3d([-100, 2000])
    #     ax[i,j].set_ylim3d([750.0, 1250.0])
    #     ax[i,j].set_zlim3d([350.0, 650.0])
    #     ax[i,j].set_xticks(np.arange(0, 18*wrfles_data[count]['diameter'], 3*wrfles_data[count]['diameter']))
    #     ax[i,j].set_xticklabels([r'$0D$', r'$3D$', r'$6D$', r'$9D$', r'$12D$', r'$15D$'], fontsize=14)
    #     ax[i,j].tick_params(axis='x', labelrotation=-90)
    #     ax[i,j].set_yticks(np.linspace(wrfles_data[count]['rotor_yloc'], wrfles_data[count]['rotor_yloc'], 1))
    #     ax[i,j].set_yticklabels([r'$0D$'], fontsize=14)
    #     ax[i,j].tick_params(axis='y', labelrotation=-30)
    #     ax[i,j].set_zticks(np.linspace(wrfles_data[count]['hub_height'], wrfles_data[count]['hub_height'], 1))
    #     ax[i,j].set_zticklabels([r'$0D$'], fontsize=14)
    #     ax[i,j].tick_params(axis='z', labelrotation=-90)
    #     ax[i,j].xaxis.labelpad=50
    #     ax[i,j].yaxis.labelpad=-5
    #     ax[i,j].zaxis.labelpad=-5
    #     ax[i,j].yaxis.set_tick_params(pad=-5)
    #     ax[i,j].zaxis.set_tick_params(pad=-1)
    #     ax[i,j].set(xlabel=r'$x~[\textrm{m}]$', ylabel=r'$y~[\textrm{m}]$', zlabel=r'$z~[\textrm{m}]$')
    #     ax[i,j].set_title(casenames[count], fontsize=24, y=0.85)
    #     if(count==2):
    #         fig.colorbar(cs1, ax=[ax[0,0], ax[0,1], ax[0,2]],
    #                     ticks=np.linspace(vmin_s,vmax_s,5,endpoint=True),
    #                     label=r'$\overline{v}/U_{\infty}~[-]$',
    #                     aspect=75, pad=0.02, orientation='horizontal')
    #     if(count==5):
    #         fig.colorbar(cs2, ax=[ax[1,0], ax[1,1], ax[1,2]],
    #                     ticks=np.linspace(vmin_v,vmax_v,5,endpoint=True),
    #                     label=r'$\overline{v}/U_{\infty}~[-]$',
    #                     aspect=75, pad=0.02, orientation='horizontal')
    # # for c in cs.collections:
    # #     c.set_edgecolor("face")
    # if save_figures:
    #     plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/padeops_vvel_slice_yz.svg", bbox_inches="tight", dpi=100)
    #     plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/padeops_vvel_slice_yz.pdf", bbox_inches="tight", dpi=300)
    #     plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/png/padeops_vvel_slice_yz.png", bbox_inches="tight", dpi=600)
    # plt.show()
    
    # # plot surface
    # fig, ax = plt.subplots(figsize=(10,10), subplot_kw={"projection": "3d"})
    # ax.set_box_aspect(aspect=(45,5,5))

    # for count, name in enumerate(casenames):
    #     if(count==0):
    #         ax.scatter(0*wrfles_data[count]['diameter'], wrfles_data[count]['Y3'][ks:ke,js:je], wrfles_data[count]['Z3'][ks:ke,js:je], 
    #                         c=np.mean(wrfles_data[count]['ux_0D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'])
    #         # ax.scatter(1*wrfles_data[count]['diameter'], wrfles_data[count]['Y3'][ks:ke,js:je], wrfles_data[count]['Z3'][ks:ke,js:je], 
    #         #                 c=np.mean(wrfles_data[count]['ux_1D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'])
    #         ax.scatter(3*wrfles_data[count]['diameter'], wrfles_data[count]['Y3'][ks:ke,js:je], wrfles_data[count]['Z3'][ks:ke,js:je],    
    #                         c=np.mean(wrfles_data[count]['ux_3D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'])
    #         ax.scatter(6*wrfles_data[count]['diameter'], wrfles_data[count]['Y3'][ks:ke,js:je], wrfles_data[count]['Z3'][ks:ke,js:je], 
    #                         c=np.mean(wrfles_data[count]['ux_6D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'])
    #         ax.scatter(9*wrfles_data[count]['diameter'], wrfles_data[count]['Y3'][ks:ke,js:je], wrfles_data[count]['Z3'][ks:ke,js:je], 
    #                         c=np.mean(wrfles_data[count]['ux_9D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'])
    #         ax.scatter(12*wrfles_data[count]['diameter'], wrfles_data[count]['Y3'][ks:ke,js:je], wrfles_data[count]['Z3'][ks:ke,js:je], 
    #                         c=np.mean(wrfles_data[count]['ux_12D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'])
    #         ax.scatter(15*wrfles_data[count]['diameter'], wrfles_data[count]['Y3'][ks:ke,js:je], wrfles_data[count]['Z3'][ks:ke,js:je], 
    #                         c=np.mean(wrfles_data[count]['ux_15D'],axis=0)[ks:ke,js:je]/wrfles_data[count]['uinf'])
    # # Set the azimuth and elevation angles
    # ax.view_init(azim=225, elev=20, roll=0)
    # # ax.plot(x11, y11, color='black', linestyle='dashed', linewidth=1.5)
    # ax.set_xlim3d([-100, 2000])
    # ax.set_ylim3d([800.0, 1200.0])
    # ax.set_zlim3d([400.0, 600.0])
    # ax.set_yticks(np.linspace(1000, 1200, 1))
    # ax.set_zticks(np.linspace(500, 600, 1))
    # if save_figures:
    #     # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/wrfles_uvel_slice_yz.svg", bbox_inches="tight", dpi=100)
    #     # plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/wrfles_uvel_slice_yz.pdf", bbox_inches="tight", dpi=300)
    #     plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/png/wrfles_uvel_slice_yz.png", bbox_inches="tight", dpi=600)
    # plt.show()


    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), constrained_layout = True)
    
    # y-z contour plot for wind speed
    for count, name in enumerate(casenames):
        cs0 = ax.pcolormesh(wrfles_data[count]['Y3'], wrfles_data[count]['Z3'],
                            np.mean(wrfles_data[count]['ux_0D'],axis=0)/wrfles_data[count]['uinf'],
                            vmin=0.6,vmax=1.0, alpha=1, cmap='viridis', shading='gouraud', rasterized=True)
        ax.plot(wrfles_data[count]['trb_y'], wrfles_data[count]['trb_z'],
                color='black', marker='o', markersize=5, linestyle='none', linewidth=1.5)
    ax.plot(x11, y11, color='black', linestyle='dashed', linewidth=1.5)
    ax.axis('equal')
    ax.set_xlim([900.0, 1100.0])
    ax.set_ylim([400.0, 600.0])
    ax.invert_xaxis()
    
###########################################################################
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), constrained_layout = True)
    
    # y-z contour plot for wind speed
    cs0 = ax.pcolormesh(np.mean(data_s00_v00['bpy'],axis=0), np.mean(data_s00_v00['bpz'],axis=0), np.mean(data_s00_v00['v1'],axis=0),
                        vmin=5,vmax=6, alpha=1, cmap='viridis', shading='auto', rasterized=True)
    ax.plot(x11, y11, color='black', linestyle='dashed', linewidth=1.5)
    ax.plot(data_s00_v00['trb_y'], data_s00_v00['trb_z'], color='black', marker='o', markersize=5, linestyle='none', linewidth=1.5)
    ax.axis('equal')
    ax.set_xlim([900.0, 1100.0])
    ax.set_ylim([400.0, 600.0])
    ax.invert_xaxis()
    
    ax.plot([data_gal['rotor_xloc'], data_gal['rotor_xloc']],
            [(data_gal['hub_height']-(data_gal['diameter']/2)),
             (data_gal['hub_height']+(data_gal['diameter']/2))],
            color='black', linestyle='solid', linewidth=3)    
    ax.set_xlim([data_gal['rotor_xloc']-(1*data_gal['diameter']),
                 data_gal['rotor_xloc']+(18*data_gal['diameter'])])
    ax.set_xticks([data_gal['rotor_xloc'], data_gal['rotor_xloc']+(5*data_gal['diameter']),
                   data_gal['rotor_xloc']+(10*data_gal['diameter']),
                   data_gal['rotor_xloc']+(15*data_gal['diameter'])])
    ax.set_ylim([data_gal['hub_height']-(1*data_gal['diameter']),
                 data_gal['hub_height']+(1*data_gal['diameter'])])
    ax.set_yticks([data_gal['hub_height']-(1*data_gal['diameter']),
                   data_gal['hub_height'], data_gal['hub_height']+(1*data_gal['diameter'])])
    # ax.set_xlabel(r'$x/D~[-]$', fontsize=fontsize) 
    # ax.set_ylabel(r'$z/D~[-]$', fontsize=fontsize)
    # ax.set_ylabel(r'$z/D$', fontsize=fontsize)
    ax.tick_params(direction='in', length=6)
    # ax.axes.xaxis.set_ticklabels([r'$0$', r'$5$', r'$10$', r'$15$'], fontsize=fontsize)
    # ax.axes.yaxis.set_ticklabels([r'$-1$', r'$0$', r'$1$'], fontsize=fontsize)
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])

    if save_figures:
        plt.savefig(path_savedata + "figures/svg/wspd_z_contour_gal.svg", bbox_inches="tight", dpi=100)
        plt.savefig(path_savedata + "figures/pdf/wspd_z_contour_gal.pdf", bbox_inches="tight", dpi=300)
        plt.savefig(path_savedata + "figures/png/wspd_z_contour_gal.png", bbox_inches="tight", dpi=600)
    
    plt.show()
###########################################################################
    # calculate total wind speed in streamwise direction:
    ws_uytz_gal = np.sqrt(data_gal['uytz_gal']**2 + data_gal['vytz_gal']**2 + data_gal['wytz_gal']**2)
    ws_min = 0.0
    ws_max = 10.0
    # ws_max = data_gal['uinf_gal']
    
    # calculate dynamic pressure:
    p_dyn = 0.5*data_gal['rho']*ws_uytz_gal**2/1000.0 # in kPa
    
    # calculate pressure drop:
    delta_p = np.max(data_gal['pytz_gal']) - data_gal['pytz_gal'][int(data_gal['ix_rotor'])+3]
    
    # power
    rho = data_gal['rho']
    a = 1-(ws_uytz_gal[int(data_gal['ix_rotor'])]/data_gal['uinf_gal'])
    area = np.pi*data_gal['diameter']**2/4
    thrust = 2*rho*data_gal['uinf_gal']**2*a*(1-a)*area/1E3   # kN
    power = 2*rho*data_gal['uinf_gal']**3*a*(1-a)**2*area/1E3 # kW
    
    p_min = 98.940
    p_max = 98.980
    
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(13.5, 4), sharex=True, constrained_layout = True)

    # velocity distribution in streamwise direction:
    ax[0].plot(xx, ws_uytz_gal, color='black', linestyle='solid', linewidth=3, zorder=10)
    ax[0].plot([xx[0], data_gal['rotor_xloc']+(30*data_gal['diameter'])],
               [data_gal['uinf_gal'], data_gal['uinf_gal']],
               color='blue', linestyle='dashed', linewidth=1.5)
    ax[0].plot([xx[0], data_gal['rotor_xloc']+(30*data_gal['diameter'])],
               [ws_uytz_gal[int(data_gal['ix_rotor'])], ws_uytz_gal[int(data_gal['ix_rotor'])]],
               color='red', linestyle='dashdot', linewidth=1.5)
    ax[0].plot([xx[0], data_gal['rotor_xloc']+(30*data_gal['diameter'])],
               [np.min(ws_uytz_gal), np.min(ws_uytz_gal)],
               color='blue', linestyle='dashed', linewidth=1.5)
    ax[0].plot([data_gal['rotor_xloc'],data_gal['rotor_xloc']], [ws_min,ws_max],
               color='black', linestyle='dashed', linewidth=1.5)    
    ax[0].set_xlim([data_gal['rotor_xloc']-(3*data_gal['diameter']),
                    data_gal['rotor_xloc']+(30*data_gal['diameter'])])
    ax[0].set_xticks([data_gal['rotor_xloc']-(3*data_gal['diameter']),
                      data_gal['rotor_xloc'],
                      data_gal['rotor_xloc']+(5*data_gal['diameter']),
                      data_gal['rotor_xloc']+(10*data_gal['diameter']),
                      data_gal['rotor_xloc']+(15*data_gal['diameter']),
                      data_gal['rotor_xloc']+(20*data_gal['diameter']),
                      data_gal['rotor_xloc']+(25*data_gal['diameter']),
                      data_gal['rotor_xloc']+(30*data_gal['diameter'])])
    ax[0].set_ylim([ws_min,ws_max])
    #ax.set_ylim([data_gal['hub_height']-(1*data_gal['diameter']),data_gal['hub_height']+(1*data_gal['diameter'])])
    #ax.set_yticks([data_gal['hub_height']-(1*data_gal['diameter']), data_gal['hub_height'], data_gal['hub_height']+(1*data_gal['diameter'])])
    ax[0].set_ylabel(r'$U~\textrm{[m~s$^{-1}$]}$', fontsize=fontsize)
    ax[0].tick_params(direction='in', length=6)
    ax[0].axes.xaxis.set_ticklabels([])
    #ax.axes.yaxis.set_ticklabels([r'$-1$', r'$0$', r'$1$'], fontsize=fontsize)
    
    # pressure distribution in streamwise direction:
    ax[1].plot(xx, data_gal['pytz_gal']/1000.0, color='black', linestyle='solid', linewidth=3, zorder=10)
    ax[1].plot([xx[0], data_gal['rotor_xloc']+(30*data_gal['diameter'])],
               [np.max(data_gal['pytz_gal'])/1000.0, np.max(data_gal['pytz_gal'])/1000.0],
               color='blue', linestyle='dashed', linewidth=1.5)
    ax[1].plot([xx[0], data_gal['rotor_xloc']+(30*data_gal['diameter'])],
               [data_gal['pytz_gal'][0]/1000.0,data_gal['pytz_gal'][0]/1000.0],
               color='red', linestyle='dashdot', linewidth=1.5)
    ax[1].plot([xx[0], data_gal['rotor_xloc']+(30*data_gal['diameter'])],
               [data_gal['pytz_gal'][int(data_gal['ix_rotor'])+3]/1000.0,
                data_gal['pytz_gal'][int(data_gal['ix_rotor'])+3]/1000.0],
               color='blue', linestyle='dashed', linewidth=1.5)
    ax[1].plot([data_gal['rotor_xloc'],data_gal['rotor_xloc']], [p_min,p_max],
               color='black', linestyle='dashed', linewidth=1.5)    
    ax[1].set_xlim([data_gal['rotor_xloc']-(3*data_gal['diameter']),
                    data_gal['rotor_xloc']+(30*data_gal['diameter'])])
    ax[1].set_xticks([data_gal['rotor_xloc']-(3*data_gal['diameter']),
                      data_gal['rotor_xloc'],
                      data_gal['rotor_xloc']+(5*data_gal['diameter']),
                      data_gal['rotor_xloc']+(10*data_gal['diameter']),
                      data_gal['rotor_xloc']+(15*data_gal['diameter']),
                      data_gal['rotor_xloc']+(20*data_gal['diameter']),
                      data_gal['rotor_xloc']+(25*data_gal['diameter']),
                      data_gal['rotor_xloc']+(30*data_gal['diameter'])])
    #ax.set_ylim([data_gal['hub_height']-(1*data_gal['diameter']),data_gal['hub_height']+(1*data_gal['diameter'])])
    #ax.set_yticks([data_gal['hub_height']-(1*data_gal['diameter']), data_gal['hub_height'], data_gal['hub_height']+(1*data_gal['diameter'])])
    ax[1].set_ylim([p_min,p_max])
    ax[1].set_xlabel(r'$x/D~[-]$', fontsize=fontsize) 
    ax[1].set_ylabel(r'$P_{tot}~\textrm{[kPa]}$', fontsize=fontsize)
    ax[1].tick_params(direction='in', length=6)
    ax[1].axes.xaxis.set_ticklabels([r'$-3$', r'$x_{rotor}$', r'$5$', r'$10$', r'$15$', r'$20$', r'$25$', r'$30$'], fontsize=fontsize)
    #ax.axes.yaxis.set_ticklabels([r'$-1$', r'$0$', r'$1$'], fontsize=fontsize)

    if save_figures:
        plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/comparison_1D_mom_theory.svg", bbox_inches="tight", dpi=100)
        plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/comparison_1D_mom_theory.pdf", bbox_inches="tight", dpi=300)
        plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/png/comparison_1D_mom_theory.png", bbox_inches="tight", dpi=600)
    
    plt.show()
###########################################################################
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(13.5, 2), constrained_layout = True)
    
    # y-z contour plot for wind speed
    cs0 = ax.pcolormesh(data_s02_v00['X3'], data_s02_v00['Z2'], np.mean(data_s02_v00['uhy'],axis=0)/data_s02_v00['uinf'],
                        vmin=0.4,vmax=1.0, alpha=1, cmap='viridis', shading='gouraud', rasterized=True)
    # cb1 = fig.colorbar(cs0, ticks=np.linspace(0.4, 1.0, 3), label='$\overline{u}/\overline{U}_{\infty}~[-]$', aspect=6, pad=0.01)
    ax.plot([data_s02_v00['rotor_xloc'], data_s02_v00['rotor_xloc']],
            [(data_s02_v00['hub_height']-(data_s02_v00['diameter']/2)),
             (data_s02_v00['hub_height']+(data_s02_v00['diameter']/2))],
            color='black', linestyle='solid', linewidth=3)    
    ax.set_xlim([data_s02_v00['rotor_xloc']-(1*data_s02_v00['diameter']),
                 data_s02_v00['rotor_xloc']+(18*data_s02_v00['diameter'])])
    ax.set_xticks([data_s02_v00['rotor_xloc'], data_s02_v00['rotor_xloc']+(5*data_s02_v00['diameter']),
                   data_s02_v00['rotor_xloc']+(10*data_s02_v00['diameter']),
                   data_s02_v00['rotor_xloc']+(15*data_s02_v00['diameter'])])
    ax.set_ylim([data_s02_v00['hub_height']-(1*data_s02_v00['diameter']),
                 data_s02_v00['hub_height']+(1*data_s02_v00['diameter'])])
    ax.set_yticks([data_s02_v00['hub_height']-(1*data_s02_v00['diameter']),
                   data_s02_v00['hub_height'], data_s02_v00['hub_height']+(1*data_s02_v00['diameter'])])
    # ax.set_xlabel(r'$x/D~[-]$', fontsize=fontsize) 
    # ax.set_ylabel(r'$z/D~[-]$', fontsize=fontsize)
    # ax.set_ylabel(r'$z/D$', fontsize=fontsize)
    ax.tick_params(direction='in', length=6)
    # ax.axes.xaxis.set_ticklabels([r'$0$', r'$5$', r'$10$', r'$15$'], fontsize=fontsize)
    # ax.axes.yaxis.set_ticklabels([r'$-1$', r'$0$', r'$1$'], fontsize=fontsize)
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])

    if save_figures:
        plt.savefig(path_savedata + "figures/svg/wspd_z_contour_gal.svg", bbox_inches="tight", dpi=100)
        plt.savefig(path_savedata + "figures/pdf/wspd_z_contour_gal.pdf", bbox_inches="tight", dpi=300)
        plt.savefig(path_savedata + "figures/png/wspd_z_contour_gal.png", bbox_inches="tight", dpi=600)
    
    plt.show()
###########################################################################
    # streamwise component of the Reynolds stress tensor (<u'u'>/Uinf**2)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(13.5, 2), constrained_layout = True)
    
    # x-y contour plot for wind speed
    cs0 = ax.contourf(data_gal['X3'], data_gal['Z2'], data_gal['uy_var_gal']/data_gal['uinf_gal']**2,
                      levels=np.linspace(0.0, 0.02, 101),extend='both', alpha=1, cmap='plasma')
    # cb1 = fig.colorbar(cs0, ticks=np.linspace(0.0, 0.02, 3), label=r'$\overline{u^{\prime}u^{\prime}}/\overline{U}^{2}_{\infty}~[-]$', aspect=6, pad=0.01)
    ax.plot([data_gal['rotor_xloc'], data_gal['rotor_xloc']],
            [(data_gal['hub_height']-(data_gal['diameter']/2)),
             (data_gal['hub_height']+(data_gal['diameter']/2))],
            color='black', linestyle='solid', linewidth=3)    
    ax.set_xlim([data_gal['rotor_xloc']-(1*data_gal['diameter']),
                 data_gal['rotor_xloc']+(18*data_gal['diameter'])])
    ax.set_xticks([data_gal['rotor_xloc'], data_gal['rotor_xloc']+(5*data_gal['diameter']),
                   data_gal['rotor_xloc']+(10*data_gal['diameter']),
                   data_gal['rotor_xloc']+(15*data_gal['diameter'])])
    ax.set_ylim([data_gal['hub_height']-(1*data_gal['diameter']),
                 data_gal['hub_height']+(1*data_gal['diameter'])])
    ax.set_yticks([data_gal['hub_height']-(1*data_gal['diameter']),
                   data_gal['hub_height'],data_gal['hub_height']+(1*data_gal['diameter'])])
    ax.tick_params(direction='in', length=6)
    # ax.set_xlabel(r'$x/D~[-]$'); ax.set_ylabel(r'$z/D~[-]$')
    # ax.axes.xaxis.set_ticklabels([r'$0$', r'$5$', r'$10$', r'$15$'])
    # ax.axes.yaxis.set_ticklabels([r'$-1.0$', r'$0.0$', r'$1.0$'])
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])

    for c in cs0.collections:
        c.set_edgecolor("face")

    if save_figures:
        plt.savefig(path_savedata + "figures/svg/rs_z_contour_gal.svg", bbox_inches="tight", dpi=100)
        plt.savefig(path_savedata + "figures/pdf/rs_z_contour_gal.pdf", bbox_inches="tight", dpi=300)
        plt.savefig(path_savedata + "figures/png/rs_z_contour_gal.png", bbox_inches="tight", dpi=600)
    
    plt.show()
###########################################################################
    # for padeops only
    ## Plotting turbine-representing circle in y-z plots
    # number of points
    n = 1000

    # radius
    r = wrfles_data[0]['diameter']/2

    # locations
    c11 = wrfles_data[0]['rotor_yloc'] # for wrfles
    # c11 = padeops_data[0]['rotor_yloc']+0.5*padeops_data[0]['dy'] # for padeops
    c12 = wrfles_data[0]['hub_height']

    # running variable
    t = np.linspace(0, 2*np.pi, n)

    x11 = c11 + r*np.sin(t)
    y11 = c12 + r*np.cos(t)

    vmin = 0.6
    vmax = 1.0
    levels = 101
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.2, 5), constrained_layout = True)
    # cs0 = ax.pcolormesh(padeops_data[0]['Y3'].transpose(), padeops_data[0]['Z3'].transpose(),
    #                     padeops_data[0]['ux_0D']/padeops_data[0]['uinf'],
    #                     vmin=vmin, vmax=vmax, alpha=1,
    #                     cmap='Spectral_r', shading='gouraud', rasterized=True)
    # cs0 = ax.pcolormesh(wrfles_data[0]['Y3'], wrfles_data[0]['Z3'],
    #                     np.mean(wrfles_data[0]['ux_0D'],axis=0)/wrfles_data[0]['uinf'],
    #                     vmin=vmin, vmax=vmax, alpha=1,
    #                     cmap='Spectral_r', shading='gouraud', rasterized=True)
    cs0 = ax.contourf(wrfles_data[0]['Y3'], wrfles_data[0]['Z3'],
                      np.mean(wrfles_data[0]['ux_0D'],axis=0)/wrfles_data[0]['uinf'],
                      levels=np.linspace(vmin, vmax, levels), extend='both', cmap='Spectral_r')
    # cs0 = ax.contourf(padeops_data[0]['Y3'].transpose(), padeops_data[0]['Z3'].transpose(),
    #                   padeops_data[0]['ux_0D']/padeops_data[0]['uinf'],
    #                   levels=np.linspace(vmin, vmax, levels), extend='both', cmap='Spectral_r')
    ax.plot(x11, y11, linestyle='solid', linewidth=3)
    # ax.set_xlim([925+(0.5*padeops_data[0]['dy']), 1075+(0.5*padeops_data[0]['dy'])])
    ax.set_xlim([925, 1075])
    ax.set_ylim([425, 575])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axes.xaxis.set_ticklabels([])
    ax.axes.yaxis.set_ticklabels([])
    ax.invert_xaxis()
    
    for c in cs0.collections:
        c.set_edgecolor("face")
    
    if save_figures:
        plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/svg/wrfles_u.svg",bbox_inches="tight",dpi=100)
        plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/pdf/wrfles_u.pdf",bbox_inches="tight",dpi=300)
        plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/png/wrfles_u.png",bbox_inches="tight",dpi=600)
    plt.show()
###########################################################################
# create animated GIFs
###########################################################################
    if(plot_animation):
        vmin = 0.4
        vmax = 1.0
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14, 2), constrained_layout = True)
        cs0 = ax.pcolormesh(data_gal['X3'], data_gal['Z2'], data_gal['uhy_gal'][0,:,:]/data_gal['uinf_gal'],
                            vmin=vmin, vmax=vmax, alpha=1, cmap='viridis', shading='gouraud', rasterized=True)
        fig.colorbar(cs0, ticks=np.linspace(vmin, vmax, 3), label=r'$\overline{u}/U_{\infty}~[-]$', cmap='viridis', aspect=6, pad=0.01)
        
        def animate(i):
            ax.clear()
            # y-z contour plot for wind speed
            cs0 = ax.pcolormesh(data_gal['X3'], data_gal['Z2'], data_gal['uhy_gal'][i,:,:]/data_gal['uinf_gal'],
                              vmin=vmin, vmax=vmax, alpha=1, cmap='viridis', shading='gouraud', rasterized=True)
            ax.plot([data_gal['rotor_xloc'], data_gal['rotor_xloc']],
                    [(data_gal['hub_height']-(data_gal['diameter']/2)),
                     (data_gal['hub_height']+(data_gal['diameter']/2))],
                    color='black', linestyle='solid', linewidth=3)    
            ax.set_xlim([data_gal['rotor_xloc']-(1*data_gal['diameter']),
                         data_gal['rotor_xloc']+(18*data_gal['diameter'])])
            ax.set_xticks([data_gal['rotor_xloc'],data_gal['rotor_xloc']+(5*data_gal['diameter']),
                           data_gal['rotor_xloc']+(10*data_gal['diameter']),
                           data_gal['rotor_xloc']+(15*data_gal['diameter'])])
            ax.set_ylim([data_gal['hub_height']-(1*data_gal['diameter']),
                         data_gal['hub_height']+(1*data_gal['diameter'])])
            ax.set_yticks([data_gal['hub_height']-(1*data_gal['diameter']),
                           data_gal['hub_height'],data_gal['hub_height']+(1*data_gal['diameter'])])
            ax.set_xlabel(r'$x/D~[-]$'); ax.set_ylabel(r'$z/D~[-]$')
            ax.axes.xaxis.set_ticklabels([r'$0$', r'$5$', r'$10$', r'$15$'])
            ax.axes.yaxis.set_ticklabels([r'$-1.0$', r'$0.0$', r'$1.0$'])
                
            print(i)
        ani = FuncAnimation(fig, animate, np.arange(0, data_gal['uhy_gal'].shape[0]), interval=0.01, repeat = False, blit=False)
        #
        ani.save('test_gif.gif', writer='pillow', fps=5)
        # ani.save('gif33.mp4', writer = 'ffmpeg', fps = 2)
###########################################################################
    if(plot_animation):
        vmin = 0.6
        vmax = 1.0
        for i in range(0,len(data_gal['ux_0D_gal'])):
            print(i,'/',data_gal['ux_0D_gal'].shape[0]-1)
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.2, 5), constrained_layout = True)
            # y-z contour plot for wind speed
            cs0 = ax.pcolormesh(data_gal['Y3'], data_gal['Z3'], data_gal['ux_0D_gal'][i,:,:]/data_gal['uinf_gal'],
                                vmin=vmin, vmax=vmax, alpha=1, cmap='Spectral_r', shading='gouraud', rasterized=True)
            ax.plot(data_gal['bpy_gal'][i,:,0], data_gal['bpz_gal'][i,:,0], color='black', marker='o',
                    markerfacecolor='black', markersize=1, linestyle='solid', linewidth=3)
            ax.plot(data_gal['bpy_gal'][i,:,1], data_gal['bpz_gal'][i,:,1], color='red', marker='o',
                    markerfacecolor='black', markersize=1, linestyle='solid', linewidth=3)
            ax.plot(data_gal['bpy_gal'][i,:,2], data_gal['bpz_gal'][i,:,2], color='limegreen', marker='o',
                    markerfacecolor='black', markersize=1, linestyle='solid', linewidth=3)
            # ax.set_xlim([300, 462])
            # ax.set_ylim([300, 460])
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axes.xaxis.set_ticklabels([])
            ax.axes.yaxis.set_ticklabels([])
            ax.invert_xaxis()
    
            if save_figures:
                if( i < 10):
                    plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/tif/rotorPlane/u_00"+str(i)+".tif",bbox_inches="tight",dpi=100)
                elif( i >= 10 and i < 100):
                    plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/tif/rotorPlane/u_0"+str(i)+".tif",bbox_inches="tight",dpi=100)
                else:
                    plt.savefig(path_savedata + '/' + sim_data + '/' + "figures/tif/rotorPlane/u_"+str(i)+".tif",bbox_inches="tight",dpi=100)
            plt.show()
            plt.close()
        grid2gif(path_savedata + '/' + sim_data + '/' + 'figures/tif/rotorPlane/*.tif',
                 path_savedata + '/' + sim_data + '/' + 'figures/gif/uvel.gif')
