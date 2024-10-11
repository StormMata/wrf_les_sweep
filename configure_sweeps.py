#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools
import os
import subprocess
import shutil
from rich.table import Table
from rich.console import Console
import platform
import re

#shear = [-4, -2, 0, 2, 4]
#veer  = [-4, -2, 0, 2, 4]

shear = [0]
veer  = [0]

excluded_pairs = [(-4, 4),  (-2, 4), (2, 4), (4, 4),
                  (-4, 2),  (4, 2),
                  (-4, -2), (4, -2),
                  (-4, -4), (-2, -4), (2, -4), (4, -4)]  # Add any pairs you want to exclude here

GAD   = True
GAL   = True
GADrs = False

base_dir      = "./runs"
wrf_path      = '/home/x-smata/to_storm/WRF-4.6.0'
library_path  = "/home/x-smata/libraries/libinsdir"
sounding_path = "/anvil/scratch/x-smata/postprocessing/results"

batch_submit  = True

# Determine if running on MacOS
is_mac = platform.system() == "Darwin"

# Create all combinations
combinations = list(itertools.product(shear, veer))

# Helper function to format the directory name without negative signs
def format_value(val):
    if val < 0:
        return f"n{abs(val)}"
    return str(val)

# Initialize the rich console
console = Console()

# Create a table for displaying combinations
table = Table(title="Combinations")

# Add table headers
table.add_column("Case", justify="right", no_wrap=True)
table.add_column("Shear", justify="right", style="green")
table.add_column("Veer", justify="right", style="red")

# Assemble table of pairs
case_num = 1
for pair in combinations:
    # Skip pairs that are in the excluded list
    if pair in excluded_pairs:
        continue
    
    # Add each combination as a row in the table
    table.add_row(str(case_num), str(pair[0]), str(pair[1]))
    
    case_num += 1

# Print the table to the console
console.print(table)

# print("Directories created.")

def create_directories(combinations, excluded_pairs, model):

    os.makedirs(base_dir + '/' + model, exist_ok=True)

    # Get model string
    model_str = model.split('_')[0].lower()

    # Initialize batch script if the flag is True
    if batch_submit:
        batch_file_path = base_dir + '/' + model_str + '_group_submit.sh'
        with open(batch_file_path, 'w') as batch_file:
            batch_file.write("#!/bin/bash\n\n")  # Add shebang and a blank line for clarity

    case_num = 1
    for pair in combinations:
        # Skip pairs that are in the excluded list
        if pair in excluded_pairs:
            continue

        print(f'working on case {pair}')
        shear_str = format_value(pair[0])
        veer_str = format_value(pair[1])
        dir_name = f"s{shear_str}_v{veer_str}"
        current_path = base_dir + '/' + model + '/' + dir_name

        # Create case directory
        os.makedirs(current_path, exist_ok=True)

        # Create symbolic links to executables
        subprocess.run([f"ln -s {wrf_path}/main/wrf.exe {current_path}"], shell=True)
        subprocess.run([f"ln -s {wrf_path}/main/ideal.exe {current_path}"], shell=True)
        subprocess.run([f"ln -s {wrf_path}/run/README.namelist {current_path}"], shell=True)
        subprocess.run([f"ln -s {wrf_path}/run/README.physics_files {current_path}"], shell=True)
        subprocess.run([f"ln -s {wrf_path}/run/README.tslist {current_path}"], shell=True)

        # Copy basic files
        for item in os.listdir('./case'):
            source_path = os.path.join('./case', item)
            destination_path = os.path.join(current_path, item)

            if os.path.isdir(source_path):
                # If it's a directory, copy it (and its contents)
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
            else:
                # If it's a file, copy it
                shutil.copy2(source_path, destination_path)

        # Copy NAMELIST file
        shutil.copy2('./namelists/' + model_str + '_namelist.input', current_path + '/' + 'namelist.input')

        # Copy SOUNDING file
        shutil.copy2(sounding_path + '/input_sounding_' + dir_name, current_path + '/' + 'namelist.input')

        # Copy TUBRINE_IJ file
        shutil.copy2('./turbines/' + model_str + '_windturbines-ij.dat', current_path + '/windturbines-ij.dat')

        # Copy MODULE LOAD file
        shutil.copy2('./shell/export_libs_load_modules.sh', current_path + '/' + 'export_libs_load_modules.sh')

        search_term = "lib_path"
        escaped_lib_path = library_path.replace("/", "\\/")

        # Adjust sed command based on the OS
        if is_mac:
            subprocess.run(['sed', '-i', '', f's/{search_term}/{escaped_lib_path}/g', current_path + '/export_libs_load_modules.sh'], check=True)
        else:
            subprocess.run(['sed', '-i', f's/{search_term}/{escaped_lib_path}/g', current_path + '/export_libs_load_modules.sh'], check=True)

        # Copy submit file
        shutil.copy2('./shell/submit_template.sh', current_path + '/' + 'submit.sh')

        search_term = "job_name"
        replacement = dir_name + "_" + model_str

        # Adjust sed command based on the OS
        if is_mac:
            subprocess.run(['sed', '-i', '', f's/{search_term}/{replacement}/g', current_path + '/' + 'submit.sh'], check=True)
        else:
            subprocess.run(['sed', '-i', f's/{search_term}/{replacement}/g', current_path + '/' + 'submit.sh'], check=True)

        # Append to batch file if the flag is True
        if batch_submit:
            with open(batch_file_path, 'a') as batch_file:
                batch_file.write(f"cd {current_path}\nsbatch submit.sh\n\n")

        case_num += 1

if GAD:
    print("\n\n=========================")
    print("========== GAD ==========")
    print("=========================")
    
    create_directories(combinations, excluded_pairs, 'gad_sweep')
    
if GAL:
    print("\n\n=========================")
    print("========== GAL ==========")
    print("=========================")

    create_directories(combinations, excluded_pairs, 'gal_sweep')

if GADrs:
    print("\n\n=========================")
    print("========= GADrs =========")
    print("=========================")

    create_directories(combinations, excluded_pairs, 'gadrs_sweep')

print("\n\n=========================")
print("========= DONE. =========")
print("=========================")
