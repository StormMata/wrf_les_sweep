#!/bin/bash
#SBATCH --nodes={PH_NNODES}
#SBATCH --ntasks={PH_NTASKS}
#SBATCH --time={PH_TIME}
#SBATCH -J {PH_JOB_NAME}
#SBATCH --account=TG-{PH_ALLOCATION}
#SBATCH -p {PH_PARTITION}
#SBATCH --mail-type=ALL
#SBATCH --mail-user=storm@mit.edu

cd $SLURM_SUBMIT_DIR

source "export_libs_load_modules.sh"

MPIRUN=$(which mpirun)

ibrun ./ideal.exe >& log.ideal
wait
ibrun ./wrf.exe >& log.wrf
