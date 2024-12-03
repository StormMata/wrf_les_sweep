#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks={PH_NTASKS}
#SBATCH --time={PH_TIME}
#SBATCH -J {PH_JOB_NAME}
#SBATCH -A {PH_ALLOCATION}
#SBATCH -p wholenode
#SBATCH --mail-user=storm@mit.edu
#SBATCH --mail-type=all

cd $SLURM_SUBMIT_DIR

source "export_libs_load_modules.sh"

MPIRUN=$(which mpirun)
export OPENMPI_ROOT=$(dirname ${MPIRUN} | sed -e 's_/bin__g')
MPI_OPTS="--map-by L3cache -x OMPI_MCA_memory_linux_disable=1 -x MALLOC_MMAP_MAX_=0 -x MALLOC_TRIM_THRESHOLD_=-1 --mca mpi_paffinity_alone 1 --mca pml ucx --mca btl ^vader,tcp,openib,sm,self"

ulimit -s unlimited

echo INFO
ompi_info

$MPIRUN $MPI_OPTS ./ideal.exe >& log.ideal
wait
$MPIRUN $MPI_OPTS ./wrf.exe >& log.wrf
