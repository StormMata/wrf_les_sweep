#!/bin/bash
#SBATCH --nodes=3
#SBATCH --ntasks=77
#SBATCH --time=12:00:00
#SBATCH -J 10_sn015_v200
#SBATCH --account=TG-ATM170028
#SBATCH -p skx
#SBATCH --mail-type=ALL
#SBATCH --mail-user=storm@mit.edu

cd $SLURM_SUBMIT_DIR

source "export_libs_load_modules.sh"

MPIRUN=$(which mpirun)

ibrun ./ideal.exe >& log.ideal
wait
ibrun ./wrf.exe >& log.wrf
