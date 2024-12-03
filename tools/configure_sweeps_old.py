#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import stat
import shutil
import platform
import itertools
import subprocess
import numpy as np

from rich.table import Table
from datetime import datetime
from rich.console import Console

# ==================================================================
# INPUTS
# ==================================================================

# shear = [-4, -2, 0, 2, 4]
# veer  = [-4, -2, 0, 2, 4]

shear = [0]
veer  = [-3, -2, -1, 0, 1, 2, 3]
# veer  = np.array([-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3])

# shear = [0]
# veer  = [0]

# excluded_pairs = [(-4, 4),  (-2, 4), (2, 4), (4, 4),
#                   (-4, 2),  (4, 2),
#                   (-4, -2), (4, -2),
#                   (-4, -4), (-2, -4), (2, -4), (4, -4)]  # Add any pairs you want to exclude here

# excluded_pairs = [(-4, 4),  (-2, 4), (2, 4), (4, 4),
#                   (-4, 2),  (4, 2),
#                   (-4, 0),  (4, 0),
#                   (-4, -2), (-2, -2), (0, -2), (2, -2), (4, -2),
#                   (-4, -4), (-2, -4), (0, -4), (2, -4), (4, -4)]  # Add any pairs you want to exclude here

# excluded_pairs = [(0, 2), (2, 0)]

excluded_pairs = []

GAD   = True
GAL   = False
GADrs = False

base_dir      = '/anvil/scratch/x-smata/wrf_les_sweep/runs'
wrf_path      = '/home/x-smata/to_storm/WRF-4.6.0'
library_path  = '/home/x-smata/libraries/libinsdir'
sounding_path = '/anvil/scratch/x-smata/postprocessing/results'
tools_path    = '/anvil/scratch/x-smata/wrf_les_sweep/tools'
turbine       = 'iea10MW'
read_from     = 'wrfout_d02_0001-01-01_00_00_00'

batch_submit  = True

# ==================================================================
# MAIN LOGIC
# ==================================================================

# Determine if running on MacOS
is_mac = platform.system() == "Darwin"

# Create all combinations
combinations = list(itertools.product(shear, veer))
# combinations = list(itertools.product(shear, np.round(veer,1)))

filtered_combinations  = [pair for pair in combinations if pair not in excluded_pairs]
formatted_combinations = [f"r's{pair[0]}_v{pair[1]}'" for pair in filtered_combinations]
casename_string        = [rf"s{str(pair[0]).replace('-', 'n')}_v{str(pair[1]).replace('-', 'n')}" for pair in filtered_combinations]
# casename_string = [
#     rf"s{str(int(pair[0] * 10)).replace('-', 'n').lstrip('0') or '0'}_v{str(int(pair[1] * 10)).replace('-', 'n').lstrip('0') or '0'}"
#     for pair in combinations if pair not in excluded_pairs
# ]










# print(combinations)
# print(combinations)

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

def create_directories(combinations, excluded_pairs, model):

    os.makedirs(base_dir + '/' + model, exist_ok=True)

    os.makedirs(base_dir + '/' + model + '/figs', exist_ok=True)

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

        # shear_str = str(int(round(pair[0] * 10))).replace('-', 'n')
        # veer_str = str(int(round(pair[1] * 10))).replace('-', 'n')
        # dir_name = f"s{shear_str}_v{veer_str}"

        current_path = base_dir + '/' + model + '/' + dir_name

        # TASK: Create case directory
        os.makedirs(current_path, exist_ok=True)

        # TASK: Create symbolic links to executables
        subprocess.run([f"ln -s {wrf_path}/main/wrf.exe {current_path}"], shell=True)
        subprocess.run([f"ln -s {wrf_path}/main/ideal.exe {current_path}"], shell=True)
        subprocess.run([f"ln -s {wrf_path}/run/README.namelist {current_path}"], shell=True)
        subprocess.run([f"ln -s {wrf_path}/run/README.physics_files {current_path}"], shell=True)
        subprocess.run([f"ln -s {wrf_path}/run/README.tslist {current_path}"], shell=True)

        # TASK: Copy basic files
        for item in os.listdir('./case'):
            source_path = os.path.join('./case', item)
            destination_path = os.path.join(current_path, item)

            if os.path.isdir(source_path):
                # If it's a directory, copy it (and its contents)
                shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
            else:
                # If it's a file, copy it
                shutil.copy2(source_path, destination_path)

        # TASK: Copy NAMELIST file
        shutil.copy2('./namelists/' + model_str + '_namelist.input', current_path + '/' + 'namelist.input')

        # TASK: Copy SOUNDING file
        shutil.copy2(sounding_path + '/input_sounding_' + dir_name, current_path + '/' + 'input_sounding')

        # TASK: Copy TUBRINE_IJ file
        shutil.copy2('./turbines/' + model_str + '_windturbines-ij.dat', current_path + '/windturbines-ij.dat')

        # TASK: Copy MODULE LOAD file
        shutil.copy2('./shell/export_libs_load_modules.sh', current_path + '/' + 'export_libs_load_modules.sh')

        search_term = "lib_path"
        escaped_lib_path = library_path.replace("/", "\\/")

        # command varies by OS
        if is_mac:
            subprocess.run(['sed', '-i', '', f's/{search_term}/{escaped_lib_path}/g', current_path + '/export_libs_load_modules.sh'], check=True)
        else:
            subprocess.run(['sed', '-i', f's/{search_term}/{escaped_lib_path}/g', current_path + '/export_libs_load_modules.sh'], check=True)

        # TASK: Copy submit file
        shutil.copy2('./shell/submit_template.sh', current_path + '/' + 'submit.sh')

        search_term = "job_name"
        replacement = dir_name + "_" + model_str

        # command varies by OS
        if is_mac:
            subprocess.run(['sed', '-i', '', f's/{search_term}/{replacement}/g', current_path + '/' + 'submit.sh'], check=True)
        else:
            subprocess.run(['sed', '-i', f's/{search_term}/{replacement}/g', current_path + '/' + 'submit.sh'], check=True)

        # TASK: Append to batch file if the flag is True
        if batch_submit:
            with open(batch_file_path, 'a') as batch_file:
                batch_file.write(f"cd {base_dir}/{model}/{dir_name}\nsbatch submit.sh\n\n")

        # TASK: grant permissions to submit shell scripts
        os.chmod(base_dir + '/' + model_str + '_group_submit.sh' , stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

        # TASK: Copy post-processing files

        ##--------------------------------------------------------------------------------
        ## SUBTASK 1: turbine properties
        turbine_properties = current_path + '/windTurbines/' + turbine + '/turbineProperties.tbl'

        extracted_values = {}

        patterns = {
        "hub_height": r"([\d.]+)\s+\"Hub height \[m\]\"",
        "diameter":   r"([\d.]+)\s+\"Rotor diameter \[m\]\"",
        "dhub":       r"([\d.]+)\s+\"Hub diameter \[m\]\"",
        }

        # Read the text file and search for the patterns
        with open(turbine_properties, "r") as file:
            content = file.read()

            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    extracted_values[key] = match.group(1)

        # Step 2: Open the original Python script and create a copy of it

        sweep_path = base_dir + '/' + model

        process_template_path = tools_path + '/process_sweep.py'
        process_path          = sweep_path + '/process_sweep.py'

        # Copy the original Python file to create a duplicate
        shutil.copyfile(process_template_path, process_path)

        # Step 3: Open the copied Python file and insert the values
        with open(process_path, "r") as file:
            python_content = file.read()

        # Step 4: Replace placeholders with extracted values
        python_content = python_content.replace("[T_DIAMETER]", extracted_values['diameter'])
        python_content = python_content.replace("[H_DIAMETER]", extracted_values['dhub'])
        python_content = python_content.replace("[HUB_HEIGHT]", extracted_values['hub_height'])

        # Insert timestamp
        timestamp = datetime.now().strftime("Generated on %a %b %d %H:%M:%S %Y")
        # Insert timestamp
        python_content = python_content.replace("[GENERATED_TIMESTAMP]", timestamp)
        python_content = python_content.replace("[TURBINE_NAME]", turbine)
        python_content = python_content.replace("[MODEL_NAME]", model_str.upper())
        python_content = python_content.replace("[NUM_CASES]", str(len(filtered_combinations)))

        # Step 5: Save the changes to the copied Python file
        with open(process_path, "w") as file:
            file.write(python_content)

        ##--------------------------------------------------------------------------------
        ## SUBTASK 2: turbine location

        turbine_coords = current_path + '/windturbines-ij.dat'

        extracted_values = {}

        pattern = r"([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+[+-]?\d+\.\d+\s+\d+"

        # Step 1: Read the data file and extract the first set of x_loc and y_loc
        with open(turbine_coords, "r") as data_file:
            data_content = data_file.read()

        # Find the first match for x and y locations
        match = re.search(pattern, data_content)

        x_loc = match.group(1)  # Extract x-location
        y_loc = match.group(2)  # Extract y-location

        # Step 2: Read the Python file and replace the placeholders
        with open(process_path, "r") as python_file:
            python_content = python_file.read()
        
        # Replace "tower_xloc = ###" with the extracted y_loc
        python_content = python_content.replace('[TOWER_X]', x_loc)

        # Replace "tower_yloc = ###" with the extracted y_loc
        python_content = python_content.replace('[TOWER_Y]', y_loc)

        # Insert sweep name
        python_content = python_content.replace('[SWEEP_NAME]', model)

        # Insert outfile name
        python_content = python_content.replace('[OUT_FILE_NAME]', read_from)

        # Insert shear combination list
        casename_string_n = "[" + ", ".join(f"r'{name}'" for name in casename_string) + "]"
        python_content = python_content.replace('[SHEAR_COMBINATIONS]', casename_string_n)

        # Step 3: Write the modified content back to the same file, overwriting it
        with open(process_path, "w") as python_file:
            python_file.write(python_content)

        ##--------------------------------------------------------------------------------
        ## SUBTASK 3:plotting file

        # Paths to your source (original) file and the destination (copy) file
        plot_template_path = tools_path + '/plot.py'
        plot_path          = sweep_path + '/plot.py'

        # Step 1: Make a copy of the original file (preserving the original template)
        shutil.copyfile(plot_template_path, plot_path)

        # Step 2: Read the content of the original file
        with open(plot_path, "r") as file:
            content = file.read()

        # Step 3: Replace every instance of "gad_sweep" with "gal_sweep"
        updated_content = content.replace('[SWEEP_NAME]', model)

        # Insert shear combination list
        updated_content = updated_content.replace('[SHEAR_COMBINATIONS]', casename_string_n)

        # Insert timestamp
        updated_content = updated_content.replace("[GENERATED_TIMESTAMP]", timestamp)
        updated_content = updated_content.replace("[TURBINE_NAME]", turbine)
        updated_content = updated_content.replace("[MODEL_NAME]", model_str.upper())
        updated_content = updated_content.replace("[NUM_CASES]", str(len(filtered_combinations)))
        
        # Step 4: Write the modified content back to the original file (overwriting it)
        with open(plot_path, "w") as file:
            file.write(updated_content)

        case_num += 1

# ==================================================================
# Execute code for each model selected
# ==================================================================

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
print("=========================\n\n")

# ==================================================================
# END OF SCRIPT
# ==================================================================