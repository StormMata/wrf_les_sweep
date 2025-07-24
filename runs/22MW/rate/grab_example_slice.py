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
import gc
#============================================================================================================
# Inputs
#============================================================================================================

np.seterr(divide='ignore',invalid='ignore')

save_data = True

save_period = 10.0 # in seconds
remove_data = 10.0 # in minutes;  discard first xxx minutes (e.g., ~2 flow-through times)

casenames = [
r's030_v025',
]

diameter   = 284.0
dhub       = 8.4
hub_height = 378.00
Ntrb       = 1
Nsct       = 224
Nelm       = 37
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

    file2read = netCDF4.Dataset(f'/scratch/09909/smata/wrf_les_sweep/runs/22MW/rate/gad_sweep/{case}/wrfout_d02_0001-01-01_00_00_00','r',mmap=False) # type: ignore # Read Netcdf-type WRF output file
    file2read.variables.keys()

    print(f'Calculating variables for {case}...')

    # Field variables
    dx = file2read.getncattr('DX')
    dy = file2read.getncattr('DY')
    dt = file2read.getncattr('DT')
    Nx = file2read.getncattr('WEST-EAST_PATCH_END_UNSTAG')
    Ny = file2read.getncattr('SOUTH-NORTH_PATCH_END_UNSTAG')
    Nz = file2read.getncattr('BOTTOM-TOP_PATCH_END_UNSTAG')
    Nt = file2read.variables['Times'].shape[0]

    if(remove_data == 0.0):
        save_period = 0.0
    else:
        save_period = (remove_data * 60 / save_period) + 1 # first xxx timesteps are not included in analysis
    process_period  = Nt - int(save_period) # consider only xxx timesteps in analysis

    Ts = Nt - int(process_period)
    Te = Nt
    Nt = Te - Ts

    print(f'Ts: {Ts}')
    print(f'Te: {Te}')

    downstreamDist = int(np.floor(1 * diameter / dx))

    h   = file2read.variables['HGT'][Ts:Te,:,:]
    ph  = file2read.variables['PH' ][Ts:Te,:,:,:]
    phb = file2read.variables['PHB'][Ts:Te,:,:,:]
    p   = file2read.variables['P'  ][Ts:Te,:,:,:]
    pb  = file2read.variables['PB' ][Ts:Te,:,:,:]
    th  = file2read.variables['T'  ][Ts:Te,:,:,:]
    u   = file2read.variables['U'  ][Ts:Te,:,:,:]
    v   = file2read.variables['V'  ][Ts:Te,:,:,:]
    w   = file2read.variables['W'  ][Ts:Te,:,:,:]

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

    Lx = Nx * dx # Lx of the computational domain
    Ly = Ny * dy # Ly of the computational domain

    nrow_vect = np.arange(0,Nx)
    ncol_vect = np.arange(0,Ny)
    neta_vect = np.arange(0,Nz)
    ntme_vect = np.arange(0,Nt)

    h_reshape = h.reshape(Nt,1,Ny,Nx)

    u4d = 0.5*(  u[:,:,:,nrow_vect] +   u[:,:,:,nrow_vect+1] ) # x-component of wind speed in 4d
    del u
    gc.collect()
    v4d = 0.5*(  v[:,:,ncol_vect,:] +   v[:,:,ncol_vect+1,:] ) # y-component of wind speed in 4d
    del v
    gc.collect()
    w4d = 0.5*(  w[:,neta_vect,:,:] +   w[:,neta_vect+1,:,:] ) # z-component of wind speed in 4d
    del w
    gc.collect()
    phm  = 0.5*( ph[:,neta_vect,:,:] +  ph[:,neta_vect+1,:,:] )
    del ph
    gc.collect()
    phbm = 0.5*(phb[:,neta_vect,:,:] + phb[:,neta_vect+1,:,:] )
    del phb
    gc.collect()
    z4d = (phm[:,neta_vect,:,:] + phbm[:,neta_vect,:,:])/9.81 - h_reshape # altitude in 4d
    del phm,phbm,h,h_reshape
    gc.collect()
    p4d = p + pb # total pressure in Pa in 4d (perturbation pressure + base state pressure)
    del p,pb
    gc.collect()

    file2read.close()
    ###########################################################################
    # tower
    ix_tower = int(np.floor((tower_xloc + 0.5*dx)/dx))     # i-level of the tower in input file
    jy_tower = int(np.floor((tower_yloc + 0.5*dy)/dy))     # j-level of the tower in input file

    # rotor
    ix_rotor = int(np.floor((np.mean(rotorApex_x) + 0.5*dx)/dx)) # i-level of the rotor in wrfout file         
    jy_rotor = int(np.floor((np.mean(rotorApex_y) + 0.5*dy)/dy)) # j-level of the tower in wrfout file

    jyl_rotor = jy_rotor - int(np.floor(((diameter/2) + 0.5*dy)/dy)) - smearingDist
    jyr_rotor = jy_rotor + int(np.floor(((diameter/2) + 0.5*dy)/dy)) + smearingDist

    rotor_xloc = np.mean(rotorApex_x)                 # Rotor x-position in meters
    rotor_yloc = np.mean(rotorApex_y)                 # Rotor y-position in meters
    rotor_zloc = np.mean(rotorApex_z)                 # Rotor z-position in meters
    ###########################################################################
    ## Vertical positions:
    # Time-averaged vertical levels:
    z_m  = np.mean(np.mean(z4d,axis=3),axis=2)    # Horizontal averaging in 4d 
    z_av = np.mean(z_m,axis=0)

    # Turbine hub upper and lower boundaries based on k-level:
    for k in range(0,Nz-1):
        if z_av[k] > hub_height:
            ktop = k; kbot = k-1
            break

    # k-level of the turbine hub center:
    k_loc = min(range(len(z_av)),key=lambda m: abs(z_av[m]-hub_height))
    z_height = z_av[k_loc]

    kzd_rotor = k_loc - int(np.floor(((diameter/2) + 0.5*dx)/dx)) - smearingDist
    kzu_rotor = k_loc + int(np.floor(((diameter/2) + 0.5*dx)/dx)) + smearingDist
    ###########################################################################
    # mean and fluctuations of velocity components and temperature:

    # u-velocity component:
    um = np.mean(np.mean(u4d,axis=3),axis=2)    # U_mean
    up = u4d - um.reshape(Nt,Nz,1,1)         # U_prime = U - U_mean
        
    # v-velocity component:
    vm = np.mean(np.mean(v4d,axis=3),axis=2)    # V_mean
    vp = v4d - vm.reshape(Nt,Nz,1,1)        # V_prime = V - V_mean

    # w-velocity component:
    wm = np.mean(np.mean(w4d,axis=3),axis=2)    # W_mean
    wp = w4d - wm.reshape(Nt,Nz,1,1)        # W_prime = W - W_mean

    # Total horizontal wind speed:
    uh = np.sqrt(u4d**2 + v4d**2)              # Total horizontal wind speed
    ###########################################################################
    # calculation of the horizontal and vertical spacings:
    xx = np.linspace(dx/2,Lx-(dx/2),Nx) # Longitudinal spacing in meters
    yy = np.linspace(dy/2,Ly-(dy/2),Ny) # Lateral spacing in meters

    X2,Y2 = np.meshgrid(xx,yy)            # Meshgrid for plotting contours in x-y plane
    X3,Z2 = np.meshgrid(xx,z_av)          # Meshgrid for plotting contours in x-z plane
    Y3,Z3 = np.meshgrid(yy,z_av)          # Meshgrid for plotting contours in y-z plane
    ###########################################################################
    ## downstream positions,time averages,and interpolations

    # Velocity components,and total horizontal wind speed at rotor's lateral position:
    uy = u4d[:,:,jy_rotor,:] + ( u4d[:,:,jy_rotor+1,:] - u4d[:,:,jy_rotor,:] )*(rotor_yloc - jy_rotor*dy)/dy
    vy = v4d[:,:,jy_rotor,:] + ( v4d[:,:,jy_rotor+1,:] - v4d[:,:,jy_rotor,:] )*(rotor_yloc - jy_rotor*dy)/dy
    wy = w4d[:,:,jy_rotor,:] + ( w4d[:,:,jy_rotor+1,:] - w4d[:,:,jy_rotor,:] )*(rotor_yloc - jy_rotor*dy)/dy
    uhy = uh[:,:,jy_rotor,:] + ( uh[:,:,jy_rotor+1,:] - uh[:,:,jy_rotor,:] )*(rotor_yloc - jy_rotor*dy)/dy

    idownstreamrotor = ix_rotor+downstreamDist
    ux_1D = u4d[:,:,:,idownstreamrotor]; vx_1D = v4d[:,:,:,idownstreamrotor]; wx_1D = w4d[:,:,:,idownstreamrotor]

    # Velocity components at hub-height:
    uz = u4d[:,kbot,:,:] + ( u4d[:,ktop,:,:] -  u4d[:,kbot,:,:] )*( ( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] ) )
    vz = v4d[:,kbot,:,:] + ( v4d[:,ktop,:,:] -  v4d[:,kbot,:,:] )*( ( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] ) )
    wz = w4d[:,kbot,:,:] + ( w4d[:,ktop,:,:] -  w4d[:,kbot,:,:] )*( ( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] ) )
    pz = p4d[:,kbot,:,:] + ( p4d[:,ktop,:,:] -  p4d[:,kbot,:,:] )*( ( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] ) )

    # Variance of velocity components at hub-height:
    uz_var = np.var(uz,axis=0); vz_var = np.var(vz,axis=0); wz_var = np.var(wz,axis=0)

    # Variance of velocity components at rotor's lateral position:
    uy_var = np.var(uy,axis=0); vy_var = np.var(vy,axis=0); wy_var = np.var(wy,axis=0)

    # Total horizontal wind speed at hub-height:
    uh_z = uh[:,kbot,:,:] + ( uh[:,ktop,:,:] -  uh[:,kbot,:,:] )*( ( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] ) )

    # Time averages of velocity components and total horizontal wind speed:
    ut = np.mean(u4d,axis=0); vt = np.mean(v4d,axis=0); wt = np.mean(w4d,axis=0); uht = np.mean(uh,axis=0)

    # Time-averaged total pressure
    pt = np.mean(p4d,axis=0)

    # Time averages of velocity components at hub-height:
    utz = ut[kbot,:,:] + ( ut[ktop,:,:] - ut[kbot,:,:] )*( ( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] ) )
    vtz = vt[kbot,:,:] + ( vt[ktop,:,:] - vt[kbot,:,:] )*( ( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] ) )
    wtz = wt[kbot,:,:] + ( wt[ktop,:,:] - wt[kbot,:,:] )*( ( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] ) )

    # Time-averaged total pressure at hub-height:
    # ptz = pt[kbot,:,:] + ( pt[ktop,:,:] - pt[kbot,:,:] )*( ( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] ) )

    # Time averages of total horizontal wind speed at hub-height:
    uhtz = uht[kbot,:,:] + ( uht[ktop,:,:] - uht[kbot,:,:] )*( ( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] ) )

    # Time averages of velocity components at rotor's longitudinal position:
    uxt_1D = np.mean(ux_1D,axis=0); vxt_1D = np.mean(vx_1D,axis=0); wxt_1D = np.mean(wx_1D,axis=0)

    # Variance of velocity components at rotor's longitudinal position:
    ux_1D_var = np.var(ux_1D,axis=0); vx_1D_var = np.var(vx_1D,axis=0); wx_1D_var = np.var(wx_1D,axis=0)

    # Time-averaged total pressure at rotor's longitudinal position at hub-height:
    # pytz = ptz[jy_rotor,:] + ( ptz[jy_rotor+1,:] - ptz[jy_rotor,:] )*(rotor_yloc - jy_rotor*dy)/dy

    # Time averages of velocity components at rotor's longitudinal position at hub-height:
    # uytz = utz[jy_rotor,:] + ( utz[jy_rotor+1,:] - utz[jy_rotor,:] )*(rotor_yloc - jy_rotor*dy)/dy
    # vytz = vtz[jy_rotor,:] + ( vtz[jy_rotor+1,:] - vtz[jy_rotor,:] )*(rotor_yloc - jy_rotor*dy)/dy
    # wytz = wtz[jy_rotor,:] + ( wtz[jy_rotor+1,:] - wtz[jy_rotor,:] )*(rotor_yloc - jy_rotor*dy)/dy

    # Time-and-disk-averaged pressure and velocity components:
    pytz = np.mean(pt[kzd_rotor:kzu_rotor,jyl_rotor:jyr_rotor,:],axis=(0,1))
    uytz = np.mean(ut[kzd_rotor:kzu_rotor,jyl_rotor:jyr_rotor,:],axis=(0,1))
    vytz = np.mean(vt[kzd_rotor:kzu_rotor,jyl_rotor:jyr_rotor,:],axis=(0,1))
    wytz = np.mean(wt[kzd_rotor:kzu_rotor,jyl_rotor:jyr_rotor,:],axis=(0,1))
    ###########################################################################
    uinf = np.mean(uh_z[:,int(jy_rotor),0],axis=0)
    # uinf = 8.0
    # Donwstream positions in meters:
    dist_0D  = rotor_xloc + (0*diameter)
    dist_2D  = rotor_xloc + (2*diameter)
    dist_4D  = rotor_xloc + (4*diameter)
    dist_6D  = rotor_xloc + (6*diameter)
    dist_8D  = rotor_xloc + (8*diameter)
    dist_10D = rotor_xloc + (10*diameter)
    # dist_15D = rotor_xloc + (15*diameter)

    # Downstream positions in i-level:
    lat_dist_0D  = int(np.floor((dist_0D+(0.5*dx))/dx))
    lat_dist_2D  = int(np.floor((dist_2D+(0.5*dx))/dx))
    lat_dist_4D  = int(np.floor((dist_4D+(0.5*dx))/dx))
    lat_dist_6D  = int(np.floor((dist_6D+(0.5*dx))/dx))
    lat_dist_8D  = int(np.floor((dist_8D+(0.5*dx))/dx))
    lat_dist_10D = int(np.floor((dist_10D+(0.5*dx))/dx))
    # lat_dist_15D = int(np.floor((dist_15D+(0.5*dx))/dx))

    # Donwstream positions in meters:
    dist_lon_0D = rotor_yloc + (0*diameter)

    # Downstream positions in j-level:
    lon_dist_0D = int(np.floor((dist_lon_0D+(0.5*dy))/dy))

    # -------------------------------------------------------------------------
    # Target lateral (y) location
    # y_target = 0.0

    # Find the j-index below y=0
    j0 = jy_rotor
    y0 = j0 * dy

    # Interpolation weight
    weight_y = (rotor_yloc - jy_rotor*dy)/dy

    # Extract x–z slices at y = 0 for all times
    # Shape: (Nt, Nz, Nx)
    u_xz = u4d[:,:,j0,:] + (u4d[:,:,j0+1,:] - u4d[:,:,j0,:]) * weight_y
    v_xz = v4d[:,:,j0,:] + (v4d[:,:,j0+1,:] - v4d[:,:,j0,:]) * weight_y
    w_xz = w4d[:,:,j0,:] + (w4d[:,:,j0+1,:] - w4d[:,:,j0,:]) * weight_y
# -------------------------------------------------------------------------
    tidx = -1  # or any value from 0 to Nt-1

    # print(u_xz.size())

    # Shape: (Nz, Nx)
    u_xz_inst = u_xz
    v_xz_inst = v_xz
    w_xz_inst = w_xz

    # wind turbine data
    aoam = np.mean(aoa,axis=(0,2))
    v1m = np.mean(v1,axis=(0,2))
    lm = np.mean(l,axis=(0,2))
    dm = np.mean(d,axis=(0,2))

    rhub = dhub/2
    dist = 0.0
    dr = np.zeros(Nelm)
    for i in range(0,Nelm):
        dist = dist + 0.5*((diameter/2 - rhub)/Nelm)
        dr[i] = rhub + dist
        dist = dist + 0.5*((diameter/2 - rhub)/Nelm)

    rOverR = dr/(diameter/2)

    fl_star = lm/(diameter*rho*uinf**2)
    fd_star = dm/(diameter*rho*uinf**2)
    v1m_star = v1m/uinf
    ###########################################################################
    # store data
    var_holder = {}

    var_holder['diameter'] = diameter
    var_holder['hub_height'] = hub_height
    var_holder['dx'] = dx
    var_holder['dy'] = dy
    var_holder['dt'] = dt
    var_holder['rho'] = rho
    var_holder['Nx'] = Nx
    var_holder['Ny'] = Ny
    var_holder['Nz'] = Nz
    var_holder['tower_xloc'] = tower_xloc
    var_holder['tower_yloc'] = tower_yloc
    var_holder['rotor_xloc'] = rotor_xloc
    var_holder['rotor_yloc'] = rotor_yloc
    var_holder['ix_tower'] = ix_tower
    var_holder['jy_tower'] = jy_tower
    var_holder['ix_rotor'] = ix_rotor
    var_holder['jy_rotor'] = jy_rotor
    var_holder['k_loc'] = k_loc
    var_holder['z_av'] = z_av
    var_holder['ktop'] = ktop
    var_holder['kbot'] = kbot
    var_holder['X2'] = X2
    var_holder['Y2'] = Y2
    var_holder['Z2'] = Z2
    var_holder['X3'] = X3
    var_holder['Y3'] = Y3
    var_holder['Z3'] = Z3
    var_holder['rOverR'] = rOverR
    var_holder['uinf'] = uinf

    var_holder['u_xz_inst'] = u_xz_inst 
    var_holder['v_xz_inst'] = v_xz_inst 
    var_holder['w_xz_inst'] = w_xz_inst 

    # Save low-frequency output variables into .npz file
        # print('##### saving data #####')
    np.savez( os.path.join(f'/scratch/09909/smata/wrf_les_sweep/runs/22MW/rate/gad_sweep/slice.npz'),**var_holder)
    print(f'Done with {case}.\n')
    del var_holder