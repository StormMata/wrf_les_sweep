#!/bin/bash

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn010_vn025
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d=2020597"}}' submit.sh > temp && mv temp submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn010_vn050
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020598"}}' submit.sh > temp && mv temp submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn010_vn100
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020599"}}' submit.sh > temp && mv temp submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn010_vn200
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020600"}}' submit.sh > temp && mv temp submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn020_v025
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020577"}}' submit.sh > temp && mv temp submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn020_v050
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020578"}}' submit.sh > temp && mv temp submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn020_v100
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020579"}}' submit.sh > temp && mv temp submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn020_v200
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020580"}}' submit.sh > temp && mv temp submit.sh
# sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn020_vn025
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020582"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn020_vn050
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020583"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn020_vn100
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020584"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn020_vn200
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020586"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn030_v025
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020587"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn030_v050
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020576"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn030_v100
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020567"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn030_v200
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020566"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn030_vn025
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020565"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn030_vn050
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020564"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn030_vn100
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020563"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh

cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/sn030_vn200
rm namelist.input
rm -rf windTurbines
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# awk '/^#SBATCH / {last=NR} {lines[NR]=$0} END {for (i=1;i<=NR;i++) {print lines[i]; if (i==last) print "#SBATCH -d 2020562"}}' submit.sh > temp && mv temp submit.sh
sbatch submit.sh












# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s010_vn025
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s010_vn050
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s010_vn100
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# sbatch submit.sh

# cd /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s010_vn200
# rm namelist.input
# rm -rf windTurbines
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/namelist.input .
# cp -r /scratch/09909/smata/wrf_les_sweep/runs/15MW/rate/gad_sweep/s000_v000/windTurbines .
# sed -i 's/^#SBATCH --time=.*/#SBATCH --time=12:00:00/' submit.sh
# sbatch submit.sh
