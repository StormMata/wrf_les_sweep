#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks=104
#SBATCH --time=12:00:00
#SBATCH -J 15_s010_vn025
#SBATCH --account=TG-ATM170028
#SBATCH -p spr
#SBATCH --mail-type=ALL
#SBATCH --mail-user=storm@mit.edu

cd $SLURM_SUBMIT_DIR

source "export_libs_load_modules.sh"

MPIRUN=$(which mpirun)

ibrun ./ideal.exe >& log.ideal
wait
ibrun ./wrf.exe >& log.wrf
