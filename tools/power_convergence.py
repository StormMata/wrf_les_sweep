#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

[GENERATED_TIMESTAMP]

Turbine: [TURBINE_NAME]
Model:   [MODEL_NAME]
Cases:   [NUM_CASES]

"""

import gc
import os
import wrf
import netCDF4
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec

from rich.console import Console
from rich.table import Table

#============================================================================================================
# Inputs
#============================================================================================================

np.seterr(divide='ignore',invalid='ignore')

save_data = True

save_period = 10.0 # in seconds
remove_data = 0.0

casenames = [SHEAR_COMBINATIONS]

diameter  = [T_DIAMETER]

#============================================================================================================
# Main logic [generally no edits beyond this point]
#============================================================================================================

for case in casenames:

    print(f'Loading data for {case}...')

    file2read = netCDF4.Dataset(f'/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/{case}/wrfout_d02_0001-01-01_00_00_00','r',mmap=False) # type: ignore # Read Netcdf-type WRF output file
    file2read.variables.keys()

    timeidx = wrf.extract_times(file2read, timeidx=wrf.ALL_TIMES, meta=False)
    times={}
    for i in range(0,len(timeidx)):
        times[i] = pd.to_datetime(str(timeidx[i])).strftime('%Y-%m-%d %H:%M:%S')

    print(f'Calculating variables for {case}...')

    # Field variables
    dx = file2read.getncattr('DX')
    dy = file2read.getncattr('DY')
    dt = file2read.getncattr('DT')
    Nx = file2read.getncattr('WEST-EAST_PATCH_END_UNSTAG')
    Ny = file2read.getncattr('SOUTH-NORTH_PATCH_END_UNSTAG')
    Nz = file2read.getncattr('BOTTOM-TOP_PATCH_END_UNSTAG')
    Nt = file2read.variables['Times'].shape[0]

    print(f'Getting save period for {case}...')

    process_period  = Nt - int(save_period) # consider only xxx timesteps in analysis

    Ts = Nt - int(process_period)
    Te = Nt
    Nt = Te - Ts

    downstreamDist = int(np.floor(1 * diameter / dx))

    print(f'Getting wind turbine variables for {case}...')

    # Wind turbine variables
    thrust      = file2read.variables['WTP_THRUST'      ][Ts:Te,:]
    power_aero  = file2read.variables['WTP_POWER'       ][Ts:Te,:]
    power_mech  = file2read.variables['WTP_POWER_MECH'  ][Ts:Te,:]
    power_gen   = file2read.variables['WTP_POWER_GEN'   ][Ts:Te,:]
    torque_aero = file2read.variables['WTP_TORQUE'      ][Ts:Te,:]
    ct          = file2read.variables['WTP_THRUST_COEFF'][Ts:Te,:]
    cp          = file2read.variables['WTP_POWER_COEFF' ][Ts:Te,:]
    v0          = file2read.variables['WTP_V0_FST_AVE'  ][Ts:Te,:]
    rotspeed    = file2read.variables['WTP_OMEGA'       ][Ts:Te,:] * (30.0 / np.pi) # convert rad/s to rpm
    rotorApex_x = file2read.variables['WTP_ROTORAPEX_X' ][Ts:Te,:]
    rotorApex_y = file2read.variables['WTP_ROTORAPEX_Y' ][Ts:Te,:]
    rotorApex_z = file2read.variables['WTP_ROTORAPEX_Z' ][Ts:Te,:]

    print(f'Plotting timeseries for {case}...')

    timeseries = np.arange(len(thrust)) * save_period / 60

    # fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(11, 11), constrained_layout=True, sharex=True)

    # ax[0,0].plot(timeseries,thrust / 1000,linestyle='solid',linewidth=2)
    # ax[0,0].set_ylabel(r'Thrust [kN]')

    # ax[0,1].plot(timeseries,torque_aero / 1000,linestyle='solid',linewidth=2)
    # ax[0,1].set_ylabel(r'Torque [kN m]')

    # ax[0,2].plot(timeseries,power_aero / 1000,linestyle='solid',linewidth=2,label='aero')
    # ax[0,2].plot(timeseries,power_mech / 1000,linestyle='solid',linewidth=2,label='mech')
    # ax[0,2].set_ylabel(r'Power [kW]')
    # ax[0,2].legend(loc="upper right", fancybox=True, shadow=False, ncol=3, fontsize=8)
    
    # ax[1,0].plot(timeseries,v0,linestyle='solid',linewidth=2)
    # ax[1,0].set_ylabel(r'$V_0$ [m/s]')
    # ax[1,0].set_xlabel(r'Time [min]')

    # ax[1,1].plot(timeseries,ct,linestyle='solid',linewidth=2)
    # ax[1,1].set_ylabel(r'$C_T$ [-]')
    # ax[1,1].set_xlabel(r'Time [min]')

    # ax[1,2].plot(timeseries,cp,linestyle='solid',linewidth=2)
    # ax[1,2].set_ylabel(r'$C_P$ [-]')
    # ax[1,2].set_xlabel(r'Time [min]')

    fig = plt.figure(figsize=(16, 11))

    gs = GridSpec(4, 3, width_ratios=[1, 1, 1], height_ratios=[2,1,2,1])
    ax1  = fig.add_subplot(gs[0, 0])
    ax2  = fig.add_subplot(gs[0, 1])
    ax3  = fig.add_subplot(gs[0, 2])
    ax4  = fig.add_subplot(gs[1, 0], sharex=ax1)
    ax5  = fig.add_subplot(gs[1, 1], sharex=ax2)
    ax6  = fig.add_subplot(gs[1, 2], sharex=ax3)
    ax7  = fig.add_subplot(gs[2, 0], sharex=ax1)
    ax8  = fig.add_subplot(gs[2, 1], sharex=ax2)
    ax9  = fig.add_subplot(gs[2, 2], sharex=ax3)
    ax10 = fig.add_subplot(gs[3, 0], sharex=ax1)
    ax11 = fig.add_subplot(gs[3, 1], sharex=ax2)
    ax12 = fig.add_subplot(gs[3, 2], sharex=ax3)

    ax1.plot(timeseries,thrust / 1000,linestyle='solid',linewidth=2)
    ax1.set_ylabel(r'Thrust [kN]')

    ax2.plot(timeseries,torque_aero / 1000,linestyle='solid',linewidth=2)
    ax2.set_ylabel(r'Torque [kN m]')

    ax3.plot(timeseries,power_aero / 1000,linestyle='solid',linewidth=2,label='aero')
    ax3.plot(timeseries,power_mech / 1000,linestyle='solid',linewidth=2,label='mech')
    ax3.set_ylabel(r'Power [kW]')
    ax3.legend(loc="upper right", fancybox=True, shadow=False, ncol=3, fontsize=8)
    
    error = np.zeros(len(thrust) - 1)
    for i in range(len(thrust) - 1):
        error[i] = np.abs(thrust[i] - thrust[i + 1]) / np.abs(thrust[i])

    ax4.plot(timeseries[:-1],error,linestyle='solid',linewidth=2)
    ax4.set_yscale('log')
    ax4.set_ylabel(r'relative change [-]')

    error = np.zeros(len(torque_aero) - 1)
    for i in range(len(torque_aero) - 1):
        error[i] = np.abs(torque_aero[i] - torque_aero[i + 1]) / np.abs(torque_aero[i])

    ax5.plot(timeseries[:-1],error,linestyle='solid',linewidth=2)
    ax5.set_yscale('log')
    # ax5.set_ylabel(r'relative change [-]')

    error_a = np.zeros(len(power_aero) - 1)
    error_m = np.zeros(len(power_mech) - 1)
    for i in range(len(power_aero) - 1):
        error_a[i] = np.abs(power_aero[i] - power_aero[i + 1]) / np.abs(power_aero[i])
        error_m[i] = np.abs(power_mech[i] - power_mech[i + 1]) / np.abs(power_mech[i])

    # ax6.plot(timeseries[:-1],error_a,linestyle='-',linewidth=2, marker='.')
    # ax6.plot(timeseries[:-1],error_m,linestyle='-',linewidth=2, marker='x')
    ax6.plot(timeseries[:-1],error_a,linestyle='-',linewidth=2)
    ax6.plot(timeseries[:-1],error_m,linestyle='-',linewidth=2)
    ax6.set_yscale('log')
    # ax6.set_ylabel(r'relative change [-]')

    ax7.plot(timeseries,v0,linestyle='solid',linewidth=2)
    ax7.set_ylabel(r'$V_0$ [m/s]')
    ax7.set_xlabel(r'Time [min]')
    ax7.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.4f'))

    ax8.plot(timeseries,ct,linestyle='solid',linewidth=2)
    ax8.set_ylabel(r'$C_T$ [-]')
    ax8.set_xlabel(r'Time [min]')

    ax9.plot(timeseries,cp,linestyle='solid',linewidth=2)
    ax9.set_ylabel(r'$C_P$ [-]')
    ax9.set_xlabel(r'Time [min]')
    ax9.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.3f'))

    error = np.zeros(len(v0) - 1)
    for i in range(len(v0) - 1):
        error[i] = np.abs(v0[i] - v0[i + 1]) / np.abs(v0[i])

    ax10.plot(timeseries[:-1],error,linestyle='solid',linewidth=2)
    ax10.set_yscale('log')
    ax10.set_ylabel(r'relative change [-]')

    error = np.zeros(len(ct) - 1)
    for i in range(len(ct) - 1):
        error[i] = np.abs(ct[i] - ct[i + 1]) / np.abs(ct[i])

    ax11.plot(timeseries[:-1],error,linestyle='solid',linewidth=2)
    ax11.set_yscale('log')
    # ax8.set_ylabel(r'relative change [-]')

    error = np.zeros(len(cp) - 1)
    for i in range(len(cp) - 1):
        error[i] = np.abs(cp[i] - cp[i + 1]) / np.abs(cp[i])

    ax12.plot(timeseries[:-1],error,linestyle='solid',linewidth=2)
    ax12.set_yscale('log')
    # ax8.set_ylabel(r'relative change [-]')

    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.setp(ax3.get_xticklabels(), visible=False)
    plt.setp(ax4.get_xticklabels(), visible=False)
    plt.setp(ax5.get_xticklabels(), visible=False)
    plt.setp(ax6.get_xticklabels(), visible=False)
    plt.setp(ax7.get_xticklabels(), visible=False)
    plt.setp(ax8.get_xticklabels(), visible=False)
    plt.setp(ax9.get_xticklabels(), visible=False)

    plt.savefig(f"/anvil/scratch/x-smata/wrf_les_sweep/runs/gad_sweep/power_convergence/convergence_{case}.png", bbox_inches="tight", dpi=600)  
