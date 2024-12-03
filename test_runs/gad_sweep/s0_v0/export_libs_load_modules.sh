#!/bin/bash

# path/to/wrf/libraries
LIBDIR="/home/x-smata/libraries/libinsdir"

# unlimit stack size
ulimit unlimited
ulimit -c unlimited
ulimit -s unlimited

# load default system modules
source /etc/profile.d/modules.sh
# load modules
module load gcc
module load openmpi

# export modules
export NETCDF="$LIBDIR/netcdf" # export netcdf first not to get compilation errors
#export NETCDFPAR="$LIBDIR/netcdf"
export HDF5="$LIBDIR/hdf5"
export PHDF5="$LIBDIR/hdf5"
export PNETCDF="$LIBDIR/pnetcdf"
export ZLIB="$LIBDIR/grib2"
#export ADIOS2="$LIBDIR/adios2"
export JASPERLIB="$LIBDIR/grib2/lib"
export JASPERINC="$LIBDIR/grib2/include"

export PATH="$LIBDIR/netcdf/bin:$PATH"
export PATH="$LIBDIR/hdf5/bin:$PATH"
#export PATH="$LIBDIR/grib2/bin:$PATH"
export PATH="$LIBDIR/pnetcdf/bin:$PATH"
#export PATH="$LIBDIR/adios2/bin:$PATH"

export LD_LIBRARY_PATH="$LIBDIR/netcdf/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="$LIBDIR/hdf5/lib:$LD_LIBRARY_PATH"
#export LD_LIBRARY_PATH="$LIBDIR/grib2/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="$LIBDIR/pnetcdf/lib:$LD_LIBRARY_PATH"
#export LD_LIBRARY_PATH="$LIBDIR/adios2/lib:$LD_LIBRARY_PATH"

# activate netcdf large file support
export WRFIO_NCD_LARGE_FILE_SUPPORT=1
