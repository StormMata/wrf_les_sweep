#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=77
#SBATCH --time=36:00:00
#SBATCH -J up20_case_1
#SBATCH --account=TG-ATM170028
#SBATCH --partition=spr
#SBATCH --mail-type=ALL
#SBATCH --mail-user=storm@mit.edu

cd $SLURM_SUBMIT_DIR

source "export_libs_load_modules.sh"

MPIRUN=$(which mpirun)

ibrun ./ideal.exe >& log.ideal
wait
ibrun ./wrf.exe >& log.wrf
