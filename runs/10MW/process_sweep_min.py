#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Generated on Tue Nov 05 14:54:59 2024

Turbine: iea10MW
Model:   GAD
Cases:   1

"""

import os
import numpy as np
import netCDF4
import pandas as pd

#============================================================================================================
# Inputs
#============================================================================================================

np.seterr(divide='ignore',invalid='ignore')

save_data = True

save_period = 10.0 # in seconds
remove_data = 10.0 # in minutes;  discard first xxx minutes (e.g., ~2 flow-through times)

# casenames = [
# r'sn030151_vn402010',
# r'sn030151_vn351759',
# r'sn030151_vn301508',
# r'sn030151_vn251256',
# r'sn030151_vn201005',
# r'sn030151_vn150754',
# r'sn030151_vn100503',
# r'sn030151_vn050251',
# r'sn030151_v000000',
# r'sn030151_v050251',
# r'sn030151_v100503',
# r'sn030151_v150754',
# r'sn030151_v201005',
# r'sn030151_v251256',
# r'sn030151_v301508',
# r'sn030151_v351759',
# r'sn030151_v402010',
# r'sn020101_vn402010',
# r'sn020101_vn351759',
# r'sn020101_vn301508',
# r'sn020101_vn251256',
# r'sn020101_vn201005',
# r'sn020101_vn150754',
# r'sn020101_vn100503',
# r'sn020101_vn050251',
# r'sn020101_v000000',
# r'sn020101_v050251',
# r'sn020101_v100503',
# r'sn020101_v150754',
# r'sn020101_v201005',
# r'sn020101_v251256',
# r'sn020101_v301508',
# r'sn020101_v351759',
# r'sn020101_v402010',
# r'sn010050_vn402010',
# r'sn010050_vn351759',
# r'sn010050_vn301508',
# r'sn010050_vn251256',
# r'sn010050_vn201005',
# r'sn010050_vn150754',
# r'sn010050_vn100503',
# r'sn010050_vn050251',
# r'sn010050_v000000',
# r'sn010050_v050251',
# r'sn010050_v100503',
# r'sn010050_v150754',
# r'sn010050_v201005',
# r'sn010050_v251256',
# r'sn010050_v301508',
# r'sn010050_v351759',
# r'sn010050_v402010',
# r's000000_vn402010',
# r's000000_vn351759',
# r's000000_vn301508',
# r's000000_vn251256',
# r's000000_vn201005',
# r's000000_vn150754',
# r's000000_vn100503',
# r's000000_vn050251',
# r's000000_v000000',
# r's000000_v050251',
# r's000000_v100503',
# r's000000_v150754',
# r's000000_v201005',
# r's000000_v251256',
# r's000000_v301508',
# r's000000_v351759',
# r's000000_v402010',
# r's010050_vn402010',
# r's010050_vn351759',
# r's010050_vn301508',
# r's010050_vn251256',
# r's010050_vn201005',
# r's010050_vn150754',
# r's010050_vn100503',
# r's010050_vn050251',
# r's010050_v000000',
# r's010050_v050251',
# r's010050_v100503',
# r's010050_v150754',
# r's010050_v201005',
# r's010050_v251256',
# r's010050_v301508',
# r's010050_v351759',
# r's010050_v402010',
# r's020101_vn402010',
# r's020101_vn351759',
# r's020101_vn301508',
# r's020101_vn251256',
# r's020101_vn201005',
# r's020101_vn150754',
# r's020101_vn100503',
# r's020101_vn050251',
# r's020101_v000000',
# r's020101_v050251',
# r's020101_v100503',
# r's020101_v150754',
# r's020101_v201005',
# r's020101_v251256',
# r's020101_v301508',
# r's020101_v351759',
# r's020101_v402010',
# r's030151_vn402010',
# r's030151_vn351759',
# r's030151_vn301508',
# r's030151_vn251256',
# r's030151_vn201005',
# r's030151_vn150754',
# r's030151_vn100503',
# r's030151_vn050251',
# r's030151_v000000',
# r's030151_v050251',
# r's030151_v100503',
# r's030151_v150754',
# r's030151_v201005',
# r's030151_v251256',
# r's030151_v301508',
# r's030151_v351759',
# r's030151_v402010',
# ]

casenames = [
r's000000_vn402010',
r's000000_vn351759',
r's000000_vn301508',
r's000000_vn251256',
r's000000_vn201005',
r's000000_vn150754',
r's000000_vn100503',
r's000000_vn050251',
r's000000_v000000',
r's000000_v050251',
r's000000_v100503',
r's000000_v150754',
r's000000_v201005',
r's000000_v251256',
r's000000_v301508',
r's000000_v351759',
r's000000_v402010'
]

diameter   = 199.0
dhub       = 4.80
hub_height = 378.00
Ntrb       = 1
Nsct       = 158
Nelm       = 26
uinf       = 7.0
rho        = 1.225

# smearing distance
smearingDist = 3

## tower and rotor apex locations:
tower_xloc = 440.0
tower_yloc = 500.0

#============================================================================================================
# Main logic [generally no edits beyond this point]
#============================================================================================================

for count,case in enumerate(casenames):

    print(f'Working on {count + 1}/{len(casenames)}: {case}.\n')

    file2read = netCDF4.Dataset(f'/scratch/09909/smata/wrf_les_sweep/runs/10MW/gad_sweep/{case}/wrfout_d02_0001-01-01_00_00_00','r',mmap=False) # type: ignore # Read Netcdf-type WRF output file
    file2read.variables.keys()


    # Field variables
    dx = file2read.getncattr('DX')
    dy = file2read.getncattr('DY')
    dt = file2read.getncattr('DT')
    Nx = file2read.getncattr('WEST-EAST_PATCH_END_UNSTAG')
    Ny = file2read.getncattr('SOUTH-NORTH_PATCH_END_UNSTAG')
    Nz = file2read.getncattr('BOTTOM-TOP_PATCH_END_UNSTAG')
    Nt = file2read.variables['Times'].shape[0]

    if(remove_data == 0.0):
        save_period_new = 0.0
    else:
        save_period_new = (remove_data * 60 / save_period) + 1 # first xxx timesteps are not included in analysis
    process_period  = Nt - int(save_period_new) # consider only xxx timesteps in analysis

    Ts = Nt - int(process_period)
    Te = Nt
    Nt = Te - Ts

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

    shapiroM    = file2read.variables['WTP_SHAPIROM'    ][Ts:Te,:]

    yaw         = file2read.variables['WTP_CAPITAL_PHI'][Ts:Te,:]

    # Wind turbine blade-element variables
    f   = (file2read.variables['WTP_F'            ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    fn  = (file2read.variables['WTP_FN'           ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    ft  = (file2read.variables['WTP_FT'           ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    l   = (file2read.variables['WTP_L'            ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    d   = (file2read.variables['WTP_D'            ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    cl  = (file2read.variables['WTP_CL'           ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    cd  = (file2read.variables['WTP_CD'           ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    aoa = (file2read.variables['WTP_ALPHA'        ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    v1  = (file2read.variables['WTP_V1'           ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    bpx = (file2read.variables['WTP_BLADEPOINTS_X'][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    bpy = (file2read.variables['WTP_BLADEPOINTS_Y'][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    bpz = (file2read.variables['WTP_BLADEPOINTS_Z'][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    vrel = (file2read.variables['WTP_VREL'        ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    phi = (file2read.variables['WTP_PHI'          ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)

    u    = (file2read.variables['WTP_U'           ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    v    = (file2read.variables['WTP_V'           ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    w    = (file2read.variables['WTP_W'           ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
    vtan = (file2read.variables['WTP_VT'          ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)

    file2read.close()

    rhub = dhub/2
    dist = 0.0
    dr = np.zeros(Nelm)
    for i in range(0,Nelm):
        dist = dist + 0.5*((diameter/2 - rhub)/Nelm)
        dr[i] = rhub + dist
        dist = dist + 0.5*((diameter/2 - rhub)/Nelm)

    rOverR = dr/(diameter/2)

    var_holder = {}

    var_holder['diameter']     = diameter
    var_holder['radius']       = diameter/2
    var_holder['hub_diameter'] = dhub
    var_holder['hub_radius']   = dhub/2
    var_holder['hub_height']  = hub_height
    var_holder['rOverR']      = rOverR
    var_holder['dx']          = dx
    var_holder['dy']          = dy
    var_holder['dz']          = 4.04

    var_holder['dt']          = dt
    var_holder['Nx']          = Nx
    var_holder['Ny']          = Ny
    var_holder['Nz']          = Nz
    var_holder['tower_xloc']  = tower_xloc
    var_holder['tower_yloc']  = tower_yloc
    var_holder['Nsct']        = Nsct
    var_holder['Nelm']        = Nelm

    var_holder['yaw']         = yaw

    var_holder['uinf']        = uinf
    var_holder['omega']       = rotspeed
    var_holder['thrust']      = thrust
    var_holder['power_aero']  = power_aero
    var_holder['power_mech']  = power_mech
    var_holder['power_gen']   = power_gen
    var_holder['torque_aero'] = torque_aero
    var_holder['ct']          = ct
    var_holder['cp']          = cp
    var_holder['v0']          = v0
    var_holder['f']           = f
    var_holder['fn']          = fn
    var_holder['ft']          = ft
    var_holder['l']           = l
    var_holder['d']           = d
    var_holder['cl']          = cl
    var_holder['cd']          = cd
    var_holder['aoa']         = aoa
    var_holder['v1']          = v1

    var_holder['u']           = u
    var_holder['v']           = v
    var_holder['w']           = w
    var_holder['v_tan']       = vtan

    var_holder['vrel']        = vrel
    var_holder['phi']         = phi

    var_holder['bpx']         = bpx
    var_holder['bpy']         = bpy
    var_holder['bpz']         = bpz
    var_holder['shapiroM']    = shapiroM

    np.savez( os.path.join(f'/scratch/09909/smata/wrf_les_sweep/runs/10MW/gad_sweep/{case}_lite.npz'),**var_holder)

del var_holder
