#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 09:00:00 2024

@author: kale
"""

import gc
import os
import numpy as np
import netCDF4
import wrf
import pandas as pd

np.seterr(divide='ignore',invalid='ignore')

save_data = True

path_main = '/nobackup1c/users/bkale/postprocessing'
path_simdata = path_main+'/'+'simdata'
path_savedata = path_main+'/'+'results'
path_processdata = path_main+'/'+'data'
path_pythonPP = path_main+'/'+'scripts'
sim_type = 'controller_simple'
sim_name = 'shear_00_backing_01'
sim_data = 'shear_veer/wrfles_data_10m'+'/'+sim_type+'/'+sim_name
file = 'wrfout_d02_0001-01-01_00_00_00'

file2read = netCDF4.Dataset(path_simdata+'/'+sim_data+'/'+file,'r',mmap=False) # type: ignore # Read Netcdf-type WRF output file
file2read.variables.keys()

timeidx = wrf.extract_times(file2read, timeidx=wrf.ALL_TIMES, meta=False)
times={}
for i in range(0,len(timeidx)):
    times[i] = pd.to_datetime(str(timeidx[i])).strftime('%Y-%m-%d %H:%M:%S')

# Field variables
dx  = file2read.getncattr('DX')
dy  = file2read.getncattr('DY')
dt  = file2read.getncattr('DT')
Nx  = file2read.getncattr('WEST-EAST_PATCH_END_UNSTAG')
Ny  = file2read.getncattr('SOUTH-NORTH_PATCH_END_UNSTAG')
Nz  = file2read.getncattr('BOTTOM-TOP_PATCH_END_UNSTAG')
Nt  = file2read.variables['Times'].shape[0]

save_period = 10.0 # in seconds
remove_data = 15.0 # in minutes;  discard first xxx minutes (e.g., ~2 flow-through times)

if(remove_data == 0.0):
    save_period = 0.0
else:
    save_period = (remove_data*60/save_period)+1 # first xxx timesteps are not included in analysis
process_period = Nt-int(save_period) # consider only xxx timesteps in analysis

Ts = Nt-int(process_period); Te = Nt
Nt = Te-Ts

diameter = 126.0; hub_height = 500.0
Ntrb = 1; Nsct = 45; Nelm = 24; uinf = 8.0; downstreamDist = int(np.floor(1*diameter/dx)); rho = 1.225

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
rotspeed    = file2read.variables['WTP_OMEGA'       ][Ts:Te,:]*(30.0/np.pi) # convert rad/s to rpm
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

Lx = Nx*dx # Lx of the computational domain
Ly = Ny*dy # Ly of the computational domain

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
# smearing distance
smearingDist = 3

## tower and rotor apex locations:
tower_xloc = 500.0                                # Tower x-position in meters
tower_yloc = 1000.0                                # Tower y-position in meters

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
dist_1D  = rotor_xloc + (1*diameter)
dist_3D  = rotor_xloc + (3*diameter)
dist_6D  = rotor_xloc + (6*diameter)
dist_9D  = rotor_xloc + (9*diameter)
dist_12D = rotor_xloc + (12*diameter)
dist_15D = rotor_xloc + (15*diameter)

# Downstream positions in i-level:
lat_dist_0D  = int(np.floor((dist_0D+(0.5*dx))/dx))
lat_dist_1D  = int(np.floor((dist_1D+(0.5*dx))/dx))
lat_dist_3D  = int(np.floor((dist_3D+(0.5*dx))/dx))
lat_dist_6D  = int(np.floor((dist_6D+(0.5*dx))/dx))
lat_dist_9D  = int(np.floor((dist_9D+(0.5*dx))/dx))
lat_dist_12D = int(np.floor((dist_12D+(0.5*dx))/dx))
lat_dist_15D = int(np.floor((dist_15D+(0.5*dx))/dx))

# Donwstream positions in meters:
dist_lon_0D = rotor_yloc + (0*diameter)

# Downstream positions in j-level:
lon_dist_0D = int(np.floor((dist_lon_0D+(0.5*dy))/dy))

# u-velocity component at different downstream locations,yz plots:
ux_0D  = u4d[:,:,:,lat_dist_0D]  + ( u4d[:,:,:,lat_dist_0D+1]  - u4d[:,:,:,lat_dist_0D]  )*(dist_0D  - lat_dist_0D*dx)/dx
ux_1D  = u4d[:,:,:,lat_dist_1D]  + ( u4d[:,:,:,lat_dist_1D+1]  - u4d[:,:,:,lat_dist_1D]  )*(dist_1D  - lat_dist_1D*dx)/dx
ux_3D  = u4d[:,:,:,lat_dist_3D]  + ( u4d[:,:,:,lat_dist_3D+1]  - u4d[:,:,:,lat_dist_3D]  )*(dist_3D  - lat_dist_3D*dx)/dx
ux_6D  = u4d[:,:,:,lat_dist_6D]  + ( u4d[:,:,:,lat_dist_6D+1]  - u4d[:,:,:,lat_dist_6D]  )*(dist_6D  - lat_dist_6D*dx)/dx
ux_9D  = u4d[:,:,:,lat_dist_9D]  + ( u4d[:,:,:,lat_dist_9D+1]  - u4d[:,:,:,lat_dist_9D]  )*(dist_9D  - lat_dist_9D*dx)/dx
ux_12D = u4d[:,:,:,lat_dist_12D] + ( u4d[:,:,:,lat_dist_12D+1] - u4d[:,:,:,lat_dist_12D] )*(dist_12D - lat_dist_12D*dx)/dx
ux_15D = u4d[:,:,:,lat_dist_15D] + ( u4d[:,:,:,lat_dist_15D+1] - u4d[:,:,:,lat_dist_15D] )*(dist_15D - lat_dist_15D*dx)/dx

uxy_0D  = ux_0D[:,:,lon_dist_0D]  + ( ux_0D[:,:,lon_dist_0D+1]  - ux_0D[:,:,lon_dist_0D]  )*(dist_lon_0D - lon_dist_0D*dy)/dy
uxy_1D  = ux_1D[:,:,lon_dist_0D]  + ( ux_1D[:,:,lon_dist_0D+1]  - ux_1D[:,:,lon_dist_0D]  )*(dist_lon_0D - lon_dist_0D*dy)/dy
uxy_3D  = ux_3D[:,:,lon_dist_0D]  + ( ux_3D[:,:,lon_dist_0D+1]  - ux_3D[:,:,lon_dist_0D]  )*(dist_lon_0D - lon_dist_0D*dy)/dy
uxy_6D  = ux_6D[:,:,lon_dist_0D]  + ( ux_6D[:,:,lon_dist_0D+1]  - ux_6D[:,:,lon_dist_0D]  )*(dist_lon_0D - lon_dist_0D*dy)/dy
uxy_9D  = ux_9D[:,:,lon_dist_0D]  + ( ux_9D[:,:,lon_dist_0D+1]  - ux_9D[:,:,lon_dist_0D]  )*(dist_lon_0D - lon_dist_0D*dy)/dy
uxy_12D = ux_12D[:,:,lon_dist_0D] + ( ux_12D[:,:,lon_dist_0D+1] - ux_12D[:,:,lon_dist_0D] )*(dist_lon_0D - lon_dist_0D*dy)/dy
uxy_15D = ux_15D[:,:,lon_dist_0D] + ( ux_15D[:,:,lon_dist_0D+1] - ux_15D[:,:,lon_dist_0D] )*(dist_lon_0D - lon_dist_0D*dy)/dy

uxyt_0D  = np.mean(uxy_0D,axis=0)/uinf
uxyt_1D  = np.mean(uxy_1D,axis=0)/uinf
uxyt_3D  = np.mean(uxy_3D,axis=0)/uinf
uxyt_6D  = np.mean(uxy_6D,axis=0)/uinf
uxyt_9D  = np.mean(uxy_9D,axis=0)/uinf
uxyt_12D = np.mean(uxy_12D,axis=0)/uinf
uxyt_15D = np.mean(uxy_15D,axis=0)/uinf

# u-velocity component at different downstream locations,xy plots:
uxz_0D  = uz[:,:,lat_dist_0D]  + ( uz[:,:,lat_dist_0D+1]  - uz[:,:,lat_dist_0D]  )*( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] )
uxz_1D  = uz[:,:,lat_dist_1D]  + ( uz[:,:,lat_dist_1D+1]  - uz[:,:,lat_dist_1D]  )*( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] )
uxz_3D  = uz[:,:,lat_dist_3D]  + ( uz[:,:,lat_dist_3D+1]  - uz[:,:,lat_dist_3D]  )*( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] )
uxz_6D  = uz[:,:,lat_dist_6D]  + ( uz[:,:,lat_dist_6D+1]  - uz[:,:,lat_dist_6D]  )*( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] )
uxz_9D  = uz[:,:,lat_dist_9D]  + ( uz[:,:,lat_dist_9D+1]  - uz[:,:,lat_dist_9D]  )*( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] )
uxz_12D = uz[:,:,lat_dist_12D] + ( uz[:,:,lat_dist_12D+1] - uz[:,:,lat_dist_12D] )*( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] )
uxz_15D = uz[:,:,lat_dist_15D] + ( uz[:,:,lat_dist_15D+1] - uz[:,:,lat_dist_15D] )*( hub_height-z_av[kbot] )/( z_av[ktop] - z_av[kbot] )

uxzt_0D  = np.mean(uxz_0D,axis=0)/uinf
uxzt_1D  = np.mean(uxz_1D,axis=0)/uinf
uxzt_3D  = np.mean(uxz_3D,axis=0)/uinf
uxzt_6D  = np.mean(uxz_6D,axis=0)/uinf
uxzt_9D  = np.mean(uxz_9D,axis=0)/uinf
uxzt_12D = np.mean(uxz_12D,axis=0)/uinf
uxzt_15D = np.mean(uxz_15D,axis=0)/uinf

# v-velocity component at different downstream locations,yz plots:
vx_0D  = v4d[:,:,:,lat_dist_0D]  + ( v4d[:,:,:,lat_dist_0D+1]  - v4d[:,:,:,lat_dist_0D]  )*(dist_0D  - lat_dist_0D*dx)/dx
vx_1D  = v4d[:,:,:,lat_dist_1D]  + ( v4d[:,:,:,lat_dist_1D+1]  - v4d[:,:,:,lat_dist_1D]  )*(dist_1D  - lat_dist_1D*dx)/dx
vx_3D  = v4d[:,:,:,lat_dist_3D]  + ( v4d[:,:,:,lat_dist_3D+1]  - v4d[:,:,:,lat_dist_3D]  )*(dist_3D  - lat_dist_3D*dx)/dx
vx_6D  = v4d[:,:,:,lat_dist_6D]  + ( v4d[:,:,:,lat_dist_6D+1]  - v4d[:,:,:,lat_dist_6D]  )*(dist_6D  - lat_dist_6D*dx)/dx
vx_9D  = v4d[:,:,:,lat_dist_9D]  + ( v4d[:,:,:,lat_dist_9D+1]  - v4d[:,:,:,lat_dist_9D]  )*(dist_9D  - lat_dist_9D*dx)/dx
vx_12D = v4d[:,:,:,lat_dist_12D] + ( v4d[:,:,:,lat_dist_12D+1] - v4d[:,:,:,lat_dist_12D] )*(dist_12D - lat_dist_12D*dx)/dx
vx_15D = v4d[:,:,:,lat_dist_15D] + ( v4d[:,:,:,lat_dist_15D+1] - v4d[:,:,:,lat_dist_15D] )*(dist_15D - lat_dist_15D*dx)/dx
###########################################################################
# turbulence statistics
# uup = up**2  # uu_prime in 4d
# uupx_0D  = uup[:,:,:,lat_dist_0D]  + ( uup[:,:,:,lat_dist_0D+1]  - uup[:,:,:,lat_dist_0D]  )*(dist_0D  - lat_dist_0D*dx)/dx
# uupx_1D  = uup[:,:,:,lat_dist_1D]  + ( uup[:,:,:,lat_dist_1D+1]  - uup[:,:,:,lat_dist_1D]  )*(dist_1D  - lat_dist_1D*dx)/dx
# uupx_3D  = uup[:,:,:,lat_dist_3D]  + ( uup[:,:,:,lat_dist_3D+1]  - uup[:,:,:,lat_dist_3D]  )*(dist_3D  - lat_dist_3D*dx)/dx
# uupx_6D  = uup[:,:,:,lat_dist_6D]  + ( uup[:,:,:,lat_dist_6D+1]  - uup[:,:,:,lat_dist_6D]  )*(dist_6D  - lat_dist_6D*dx)/dx
# uupx_9D  = uup[:,:,:,lat_dist_9D]  + ( uup[:,:,:,lat_dist_9D+1]  - uup[:,:,:,lat_dist_9D]  )*(dist_9D  - lat_dist_9D*dx)/dx
# uupx_12D = uup[:,:,:,lat_dist_12D] + ( uup[:,:,:,lat_dist_12D+1] - uup[:,:,:,lat_dist_12D] )*(dist_12D - lat_dist_12D*dx)/dx
# uupx_15D = uup[:,:,:,lat_dist_15D] + ( uup[:,:,:,lat_dist_15D+1] - uup[:,:,:,lat_dist_15D] )*(dist_15D - lat_dist_15D*dx)/dx

# uupxy_0D  = uupx_0D[:,:,lon_dist_0D]  + ( uupx_0D[:,:,lon_dist_0D+1]  - uupx_0D[:,:,lon_dist_0D]  )*(dist_lon_0D - lon_dist_0D*dy)/dy
# uupxy_1D  = uupx_1D[:,:,lon_dist_0D]  + ( uupx_1D[:,:,lon_dist_0D+1]  - uupx_1D[:,:,lon_dist_0D]  )*(dist_lon_0D - lon_dist_0D*dy)/dy
# uupxy_3D  = uupx_3D[:,:,lon_dist_0D]  + ( uupx_3D[:,:,lon_dist_0D+1]  - uupx_3D[:,:,lon_dist_0D]  )*(dist_lon_0D - lon_dist_0D*dy)/dy
# uupxy_6D  = uupx_6D[:,:,lon_dist_0D]  + ( uupx_6D[:,:,lon_dist_0D+1]  - uupx_6D[:,:,lon_dist_0D]  )*(dist_lon_0D - lon_dist_0D*dy)/dy
# uupxy_9D  = uupx_9D[:,:,lon_dist_0D]  + ( uupx_9D[:,:,lon_dist_0D+1]  - uupx_9D[:,:,lon_dist_0D]  )*(dist_lon_0D - lon_dist_0D*dy)/dy
# uupxy_12D = uupx_12D[:,:,lon_dist_0D] + ( uupx_12D[:,:,lon_dist_0D+1] - uupx_12D[:,:,lon_dist_0D] )*(dist_lon_0D - lon_dist_0D*dy)/dy
# uupxy_15D = uupx_15D[:,:,lon_dist_0D] + ( uupx_15D[:,:,lon_dist_0D+1] - uupx_15D[:,:,lon_dist_0D] )*(dist_lon_0D - lon_dist_0D*dy)/dy

# uupxyt_0D  = np.mean(uupxy_0D,axis=0)/(uinf**2)
# uupxyt_1D  = np.mean(uupxy_1D,axis=0)/(uinf**2)
# uupxyt_3D  = np.mean(uupxy_3D,axis=0)/(uinf**2)
# uupxyt_6D  = np.mean(uupxy_6D,axis=0)/(uinf**2)
# uupxyt_9D  = np.mean(uupxy_9D,axis=0)/(uinf**2)
# uupxyt_12D = np.mean(uupxy_12D,axis=0)/(uinf**2)
# uupxyt_15D = np.mean(uupxy_15D,axis=0)/(uinf**2)

# del uup # Free-up some memory

uupxy_0D  = uy_var[:,lat_dist_0D]  + ( uy_var[:,lat_dist_0D+1]  - uy_var[:,lat_dist_0D]  )*(dist_0D  - lat_dist_0D*dx)/dx
uupxy_1D  = uy_var[:,lat_dist_1D]  + ( uy_var[:,lat_dist_1D+1]  - uy_var[:,lat_dist_1D]  )*(dist_1D  - lat_dist_1D*dx)/dx
uupxy_3D  = uy_var[:,lat_dist_3D]  + ( uy_var[:,lat_dist_3D+1]  - uy_var[:,lat_dist_3D]  )*(dist_3D  - lat_dist_3D*dx)/dx
uupxy_6D  = uy_var[:,lat_dist_6D]  + ( uy_var[:,lat_dist_6D+1]  - uy_var[:,lat_dist_6D]  )*(dist_6D  - lat_dist_6D*dx)/dx
uupxy_9D  = uy_var[:,lat_dist_9D]  + ( uy_var[:,lat_dist_9D+1]  - uy_var[:,lat_dist_9D]  )*(dist_9D  - lat_dist_9D*dx)/dx
uupxy_12D = uy_var[:,lat_dist_12D] + ( uy_var[:,lat_dist_12D+1] - uy_var[:,lat_dist_12D] )*(dist_12D - lat_dist_12D*dx)/dx
uupxy_15D = uy_var[:,lat_dist_15D] + ( uy_var[:,lat_dist_15D+1] - uy_var[:,lat_dist_15D] )*(dist_15D - lat_dist_15D*dx)/dx

uupxyt_0D  = uupxy_0D/(uinf**2)
uupxyt_1D  = uupxy_1D/(uinf**2)
uupxyt_3D  = uupxy_3D/(uinf**2)
uupxyt_6D  = uupxy_6D/(uinf**2)
uupxyt_9D  = uupxy_9D/(uinf**2)
uupxyt_12D = uupxy_12D/(uinf**2)
uupxyt_15D = uupxy_15D/(uinf**2)
###########################################################################
# wind turbine data
aoam = np.mean(aoa,axis=(0,2))
v1m = np.mean(v1,axis=(0,2))
lm = np.mean(l,axis=(0,2))
dm = np.mean(d,axis=(0,2))

rhub = 1.5
dist = 0.0
dr = np.zeros(Nelm)
for i in range(0,Nelm):
    dist = dist + 0.5*(61.5/Nelm)
    dr[i] = rhub + dist
    dist = dist + 0.5*(61.5/Nelm)

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
var_holder['omega'] = rotspeed
var_holder['thrust'] = thrust
var_holder['power_aero'] = power_aero
var_holder['power_mech'] = power_mech
var_holder['power_gen'] = power_gen
var_holder['torque_aero'] = torque_aero
var_holder['ct'] = ct
var_holder['cp'] = cp
var_holder['v0'] = v0
var_holder['f'] = f
var_holder['fn'] = fn
var_holder['ft'] = ft
var_holder['l'] = l
var_holder['d'] = d
var_holder['cl'] = cl
var_holder['cd'] = cd
var_holder['aoa'] = aoa
var_holder['v1'] = v1
var_holder['um'] = um
var_holder['vm'] = vm
var_holder['wm'] = wm
var_holder['uh'] = uh
var_holder['uhy'] = uhy
var_holder['uytz'] = uytz
var_holder['vytz'] = vytz
var_holder['wytz'] = wytz
var_holder['pytz'] = pytz
var_holder['uz_var'] = uz_var
var_holder['vz_var'] = vz_var
var_holder['wz_var'] = wz_var
var_holder['uy_var'] = uy_var
var_holder['vy_var'] = vy_var
var_holder['wy_var'] = wy_var
var_holder['ux_var'] = ux_1D_var
var_holder['vx_var'] = vx_1D_var
var_holder['wx_var'] = wx_1D_var
var_holder['uhtz'] = uhtz
var_holder['ux_0D'] = ux_0D
var_holder['ux_1D'] = ux_1D
var_holder['ux_3D'] = ux_3D
var_holder['ux_6D'] = ux_6D
var_holder['ux_9D'] = ux_9D
var_holder['ux_12D'] = ux_12D
var_holder['ux_15D'] = ux_15D
var_holder['vx_0D'] = vx_0D
var_holder['vx_1D'] = vx_1D
var_holder['vx_3D'] = vx_3D
var_holder['vx_6D'] = vx_6D
var_holder['vx_9D'] = vx_9D
var_holder['vx_12D'] = vx_12D
var_holder['vx_15D'] = vx_15D
var_holder['uxyt_0D'] = uxyt_0D
var_holder['uxyt_1D'] = uxyt_1D
var_holder['uxyt_3D'] = uxyt_3D
var_holder['uxyt_6D'] = uxyt_6D
var_holder['uxyt_9D'] = uxyt_9D
var_holder['uxyt_12D'] = uxyt_12D
var_holder['uxyt_15D'] = uxyt_15D
var_holder['uxzt_0D'] = uxzt_0D
var_holder['uxzt_1D'] = uxzt_1D
var_holder['uxzt_3D'] = uxzt_3D
var_holder['uxzt_6D'] = uxzt_6D
var_holder['uxzt_9D'] = uxzt_9D
var_holder['uxzt_12D'] = uxzt_12D
var_holder['uxzt_15D'] = uxzt_15D
var_holder['uupxyt_0D'] = uupxyt_0D
var_holder['uupxyt_1D'] = uupxyt_1D
var_holder['uupxyt_3D'] = uupxyt_3D
var_holder['uupxyt_6D'] = uupxyt_6D
var_holder['uupxyt_9D'] = uupxyt_9D
var_holder['uupxyt_12D'] = uupxyt_12D
var_holder['uupxyt_15D'] = uupxyt_15D
var_holder['aoam'] = aoam
var_holder['v1m_star'] = v1m_star
var_holder['fl_star'] = fl_star
var_holder['fd_star'] = fd_star
var_holder['bpx'] = bpx
var_holder['bpy'] = bpy
var_holder['bpz'] = bpz
var_holder['trb_x'] = rotor_xloc
var_holder['trb_y'] = rotor_yloc
var_holder['trb_z'] = rotor_zloc

# Save low-frequency output variables into .npz file
if(save_data):
    print('##### saving data #####')
    np.savez( os.path.join(path_simdata+'/'+sim_data+'/gad_'+sim_name+'.npz'),**var_holder)
    print('done.')