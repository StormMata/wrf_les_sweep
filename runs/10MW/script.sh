#!/bin/bash

cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/sn010_v025
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d=123456"}}' submit.sh > temp && mv temp submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/sn010_v050 
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/sn010_v100
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s010_v200
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s020_v025
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s020_v050
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s020_v100
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s020_v200
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s030_v025
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s030_v050
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s030_v100
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s030_v200
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s030_vn200
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s030_vn100
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s030_vn050
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s030_vn025
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s020_vn025
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s020_vn050
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s020_vn100
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s020_vn200
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s010_vn025
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s010_vn050
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s010_vn100
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s010_vn200
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/10MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=8:00:00/' submit.sh
# sbatch submit.sh
