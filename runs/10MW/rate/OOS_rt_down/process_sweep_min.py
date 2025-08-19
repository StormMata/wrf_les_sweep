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

#============================================================================================================
# Inputs
#============================================================================================================

np.seterr(divide='ignore',invalid='ignore')

save_data = True

save_period = 10.0 # in seconds
remove_data = 10.0 # in minutes;  discard first xxx minutes (e.g., ~2 flow-through times)

casenames = [
# r'sn030_vn200',
# r'sn030_vn100',
# r'sn030_vn050',
# r'sn030_vn025',
# r'sn030_v000',
# r'sn030_v025',
# r'sn030_v050',
# r'sn030_v100',
# r'sn030_v200',
# r'sn020_vn200',
r'sn020_vn100',
# r'sn020_vn050',
# r'sn020_vn025',
r'sn020_v000',
# r'sn020_v025',
# r'sn020_v050',
r'sn020_v100',
# r'sn020_v200',
# r'sn010_vn200',
# r'sn010_vn100',
# r'sn010_vn050',
# r'sn010_vn025',
# r'sn010_v000',
# r'sn010_v025',
# r'sn010_v050',
# r'sn010_v100',
# r'sn010_v200',
# r's000_vn200',
r's000_vn100',
# r's000_vn050',
# r's000_vn025',
r's000_v000',
# r's000_v025',
# r's000_v050',
r's000_v100',
# r's000_v200',
# r's010_vn200',
# r's010_vn100',
# r's010_vn050',
# r's010_vn025',
# r's010_v000',
# r's010_v025',
# r's010_v050',
# r's010_v100',
# r's010_v200',
# r's020_vn200',
r's020_vn100',
# r's020_vn050',
# r's020_vn025',
r's020_v000',
# r's020_v025',
# r's020_v050',
r's020_v100',
# r's020_v200',
# r's030_vn200',
# r's030_vn100',
# r's030_vn050',
# r's030_vn025',
# r's030_v000',
# r's030_v025',
# r's030_v050',
# r's030_v100',
# r's030_v200'
]

diameter   = 199.0
dhub       = 4.80
hub_height = 378.00
Ntrb       = 1
Nsct       = 134
Nelm       = 22
uinf       = 7.0
rho        = 1.225

# smearing distance
smearingDist = 3

## tower and rotor apex locations:
tower_xloc = 720.0
tower_yloc = 720.0

#============================================================================================================
# Main logic [generally no edits beyond this point]
#============================================================================================================

for count,case in enumerate(casenames):

    print(f'Working on {count + 1}/{len(casenames)}: {case}.\n')

    file2read = netCDF4.Dataset(f'/scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/OOS_rt_down/gad_sweep/{case}/wrfout_d02_0001-01-01_00_00_00','r',mmap=False) # type: ignore # Read Netcdf-type WRF output file
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
    pitch       = file2read.variables['WTP_PITCH'       ][Ts:Te,:]
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
    vtnn = (file2read.variables['WTP_VTHETA'      ][Ts:Te,:]).reshape(Nt,Nelm,Nsct)
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
    var_holder['v_tan_no_rot']= vtnn

    var_holder['vrel']        = vrel
    var_holder['phi']         = phi
    var_holder['pitch']       = pitch

    var_holder['bpx']         = bpx
    var_holder['bpy']         = bpy
    var_holder['bpz']         = bpz
    var_holder['shapiroM']    = shapiroM

    np.savez( os.path.join(f'/scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/OOS_rt_down/gad_sweep/{case}_lite.npz'),**var_holder)

del var_holder
