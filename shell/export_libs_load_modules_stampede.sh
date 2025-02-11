#!/bin/bash

#unlimit stack size
ulimit unlimited
ulimit -c unlimited
ulimit -s unlimited

module load intel
module load impi
module load netcdf
module load parallel-netcdf
module load pnetcdf
#module load hdf5
module load phdf5

###################################################################
# **** PLACE Environment Variables including PATH here.        ****
###################################################################

export NETCDF=/opt/apps/intel24/netcdf/4.9.2
export NETCDFPAR=/opt/apps/intel24/impi21/parallel-netcdf/4.9.2/x86_64
#export HDF5=/opt/apps/intel24/hdf5/1.14.4
export HDF5=/opt/apps/intel24/impi21/phdf5/1.14.4
export PHDF5=/opt/apps/intel24/impi21/phdf5/1.14.4
export PNETCDF=/opt/apps/intel24/impi21/pnetcdf/1.12.3

export J="-j 16"

