#!/bin/bash

file="process_sweep_min.py"

conda run --no-capture-output -n mitrotor python3 process_sweep_min.py

old_case="r'U06'"
new_case="r'U07'"

# # Use sed to find and replace
sed -i "s/${old_case}/${new_case}/g" "$file"

conda run --no-capture-output -n mitrotor python3 process_sweep_min.py

old_case="r'U07'"
new_case="r'U08'"

# Use sed to find and replace
sed -i "s/${old_case}/${new_case}/g" "$file"

conda run --no-capture-output -n mitrotor python3 process_sweep_min.py

old_case="r'U08'"
new_case="r'U09'"

# Use sed to find and replace
sed -i "s/${old_case}/${new_case}/g" "$file"

conda run --no-capture-output -n mitrotor python3 process_sweep_min.py

old_case="r'U09'"
new_case="r'U10'"

# Use sed to find and replace
sed -i "s/${old_case}/${new_case}/g" "$file"

conda run --no-capture-output -n mitrotor python3 process_sweep_min.py







sn030151_vn402010
sn030151_vn201005
sn030151_vn100503
sn030151_vn050251
sn030151_v000000
sn030151_v050251
sn030151_v100503
sn030151_v201005
sn030151_v402010
sn020101_vn402010
sn020101_vn201005
sn020101_vn100503
sn020101_vn050251
sn020101_v000000
sn020101_v050251
sn020101_v100503
sn020101_v201005
sn020101_v402010
sn010050_vn402010
sn010050_vn201005
sn010050_vn100503
sn010050_vn050251
sn010050_v000000
sn010050_v050251
sn010050_v100503
sn010050_v201005
sn010050_v402010
s000000_vn402010
s000000_vn201005
s000000_vn100503
s000000_vn050251
s000000_v000000
s000000_v050251
s000000_v100503
s000000_v201005
s000000_v402010
s010050_vn402010
s010050_vn201005
s010050_vn100503
s010050_vn050251
s010050_v000000
s010050_v050251
s010050_v100503
s010050_v201005
s010050_v402010
s020101_vn402010
s020101_vn201005
s020101_vn100503
s020101_vn050251
s020101_v000000
s020101_v050251
s020101_v100503
s020101_v201005
s020101_v402010
s030151_vn402010
s030151_vn201005
s030151_vn100503
s030151_vn050251
s030151_v000000
s030151_v050251
s030151_v100503
s030151_v201005
s030151_v402010