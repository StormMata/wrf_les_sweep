#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
import platform
import subprocess
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

from wrf_io import preproc
from rich.live import Live
from rich.table import Table
from itertools import product
from rich.console import Console
from scipy.interpolate import interp1d

# ==================================================================
# INPUTS
# ==================================================================
# shear = [0]
# veer  = [-3.5, -2, -1, 0, 1, 2.5, 3]

# shear = [0]
# veer  = [4]

shear = [-4, -2, 0, 2, 4]
veer  = [-4, -2, 0, 2, 4]

# shear = [0]
# veer  = [0]

excluded_pairs = [(-4,4), (-2,4), (2,4), (4,4),
                  (-4,2), (4,2),
                  (-4,-2), (4,-2),
                  (-4,-4), (-2,-4), (2,-4), (4,-4)]

# excluded_pairs = [(-4,4),  (-2,4),  (2,4),  (4,4),
#                   (-4,2),  (-2,2),  (2,2),  (4,2),
#                   (-4,-2), (-2,-2), (2,-2), (4,-2),
#                   (-4,-4), (-2,-4), (2,-4), (4,-4)]

max_sample    = 7

Ufst          = 7.0

GAD           = True
GAL           = False
GADrs         = False

# base_dir      = '/anvil/scratch/x-smata/wrf_les_sweep/profile_tests'
# wrf_path      = '/home/x-smata/to_storm/WRF-4.6.0'
# library_path  = '/home/x-smata/libraries/libinsdir'

base_dir      = '/scratch/09909/smata/wrf_les_sweep/runs/15MW'
wrf_path      = '/work2/09909/smata/stampede3/WRF-4.6.0'
library_path  = ''

turbine       = 'iea15MW'
read_from     = 'wrfout_d02_0001-01-01_00_00_00'
batch_submit  = True

plot_profiles = True
plot_domain   = True

allocation    = 'EES230042'
# allocation    = 'ATM170028'
runtime       = '48:00:00'

system        = 'stampede'

plt.rcParams['text.usetex'] = True

# ==================================================================
# HELPER FUNCTIONS
# ==================================================================

def format_value(val, int_digits, frac_digits):
    """
    Format directory name values with the following rules:
    1. The number of digits before the decimal point (int_digits) is consistent across all values.
    2. The number of digits after the decimal point (frac_digits) is consistent across all values.
    3. Decimal points are removed in the output (e.g., 3.0 becomes 300).
    4. A minus sign is replaced with 'n' (e.g., -3.0 becomes n300).

    Args:
        val (float): The value to format.
        int_digits (int): Number of digits before the decimal point.
        frac_digits (int): Number of digits after the decimal point.

    Returns:
        str: The formatted string.
    """
    # Format the value with specified digits
    formatted = f"{abs(val):0{int_digits}.{frac_digits}f}".replace('.', '')
    
    # Add 'n' for negative values or return the positive string
    return f"n{formatted}" if val < 0 else formatted

def determine_format(shear, veer):
    """
    Determine the maximum number of integer and fractional digits from shear and veer lists.

    Args:
        shear (list[float]): List of shear values.
        veer (list[float]): List of veer values.

    Returns:
        tuple: (int_digits, frac_digits)
    """
    all_values = shear + veer
    
    # Determine max integer and fractional digits
    max_int_digits  = max(len(str(int(abs(val)))) for val in all_values)
    max_frac_digits = max(len(str(val).split('.')[-1]) if '.' in str(val) else 0 for val in all_values)
    
    return max_int_digits, max_frac_digits

def run_subprocess(command, mac_flag = False):
    """Run subprocess commands with OS compatibility."""
    if platform.system() == "Darwin" and mac_flag:
        command.insert(2, "")
    subprocess.run(command, check = True)

def create_symlinks(target_dir):
    """Create symbolic links in the target directory."""
    links = [
        f"{wrf_path}/main/wrf.exe",
        f"{wrf_path}/main/ideal.exe",
        f"{wrf_path}/run/README.namelist",
        f"{wrf_path}/run/README.physics_files",
        f"{wrf_path}/run/README.tslist",
    ]
    for link in links:
        subprocess.run([f"ln -s {link} {target_dir}"], shell = True)

def copy_files(source, destination, dirs_exist_ok = True):
    """Copy files and directories from source to destination."""
    if os.path.isdir(source):
        shutil.copytree(source, destination, dirs_exist_ok = dirs_exist_ok)
    else:
        shutil.copy2(source, destination)

def parse_turbineProperties(file_path):
    """Extract turbine diameter and hub height"""
    config = {}

    # Open the file and read its contents
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Check for key-value pairs where value comes first and key is in quotes
            key_value_match = re.match(r'^\s*([\d\.\-]+)\s+"([^"]+)"\s*$', line)
            if key_value_match:
                value = float(key_value_match.group(1))  # Convert value to float
                key   = key_value_match.group(2)  # Extract key as string
                config[key] = value  # Store in dictionary with key-value pair

    return float(config['Rotor diameter [m]']), float(config['Hub height [m]'])

def generate_v(x, D, shear):
    # Define the regions
    x1, x2 = -(D / 2) * 2, (D / 2) * 2  # Region boundaries
    
    # Initialize the result as zeros
    v = np.zeros_like(x, dtype=float)

    # Region 1: x < x1
    v[x < x1] = shear / 10 * x1

    # Region 2: x1 <= x <= x2 (linear function with constant slope)
    mask_region2 = (x >= x1) & (x <= x2)
    v[mask_region2] = shear / 10 * x[mask_region2]

    # Region 3: x > x2
    v[x > x2] = shear / 10 * x2

    return v

def generate_u(x, D, shear):
    # # Define the regions
    # x1, x2 = -(1/2) * 1.75 , (1/2) * 1.75 # Region boundaries
    # # Calculate the constant values based on Region 2
    # value_region1 = shear/10 * x1  # f(x_1) for Region 1
    # value_region3 = shear/10 * x2  # f(x_2) for Region 3

    # if shear == 0:
    #     return np.full_like(x, 1)
    
    # else:
    #     # Define the piecewise behavior
    #     return np.piecewise(
    #         x,
    #         [x < x1, (x >= x1) & (x <= x2), x > x2],
    #         [value_region1, lambda x: shear/10 * x, value_region3],
    #     ) + 1

    # Define the regions
    x1, x2 = -(1 / 2) * 1.95, (1 / 2) * 1.95  # Region boundaries

    # Initialize the result as ones (to handle the "+1" offset)
    u = np.ones_like(x, dtype=float)

    if shear == 0:
        # If shear is zero, return an array of ones
        return u
    
    # Region 1: x < x1 (constant value)
    u[x < x1] += shear / 10 * x1

    # Region 2: x1 <= x <= x2 (linear function with constant slope)
    mask_region2 = (x >= x1) & (x <= x2)
    u[mask_region2] += shear / 10 * x[mask_region2]

    # Region 3: x > x2 (constant value)
    u[x > x2] += shear / 10 * x2

    return u

def smooth_piecewise(y, sigma, dx):
    # Create a Gaussian kernel with a given standard deviation (sigma)
    kernel_size = int(6 * sigma / dx)  # Ensure the kernel is large enough to cover the influence of the Gaussian
    kernel = np.exp(-np.linspace(-3, 3, kernel_size)**2 / (2 * sigma**2))
    kernel /= np.sum(kernel)  # Normalize the kernel

    # Apply convolution (low-pass filter) to smooth the signal
    y_smoothed = signal.convolve(y, kernel, mode='same')

    # Skip the endpoints by copying them directly from the original signal
    skip_points = kernel_size // 2  # Number of points influenced by the kernel
    y_smoothed[:skip_points] = y[:skip_points]  # Preserve the start
    y_smoothed[-skip_points:] = y[-skip_points:]  # Preserve the end
    
    return y_smoothed

def create_sounding(current_path, figure_path, figure_name, pair, height):
    """Create sounding files based on shear and veer settings"""

    zmid  = 0 # [nondimensional] middle point in z-direction

    # # eps_x = [0,]

    # eps   = 1e4

    # # znondim = np.linspace(-zhub/D , (1.1 * zhub/D), 189, endpoint = True)
    # znondim = np.arange((-zhub/D), (1.5 * zhub/D), 2/D)

    # if ((pair[0] == 0) & (pair[1] == 0)) :        # uniform
    #     uinf     = np.full_like(znondim, 1)
    #     vinf     = np.full_like(znondim, 0)

    # if ((pair[0] != 0) & (pair[1] == 0)) :        # sheer only
    #     A        = pair[0] / 10
    #     uinf     = (1 + eps * np.tanh(A * (znondim - zmid) / eps))
    #     vinf     = np.full_like(znondim, 0)

    # if ((pair[0] == 0) & (pair[1] != 0)) :        # veer only
    #     uinf     = np.full_like(znondim, 1)
    #     v_inflow = 1.0
    #     A        = np.pi / 180 * D * pair[1]/10
    #     # vinf     = eps * np.tanh(v_inflow * A * (znondim - zmid) / eps)

    #     a = 1000
    #     vinf     = np.copysign(1, v_inflow * A * (znondim - zmid)) * (np.tanh(((v_inflow * A * (znondim - zmid))**(2))**(a/2)))**(1/a)


    #     vinflow = piecewise_function(znondim)


    # if ((pair[0] != 0) & (pair[1] != 0)) :        # shear AND veer
        # A_eq     = np.pi / 180 * D * pair[1]/10
        # v_inflow = A_eq / (pair[1] / 10)
        # A        = (pair[0] / 10)
        # uinf     = (1 + eps * np.tanh(A * (znondim - zmid) / eps))
        # vinf     = eps * np.tanh(v_inflow * A * (znondim - zmid) / eps)

    ######################################################################
    # dimensionalize all variables
    # z = abs((znondim*D)+zhub)
    # zmid = 0
    z = np.arange(-1000, 1000, 1)

    uinf = generate_u(z/D, D, pair[0])
    uinf = smooth_piecewise(uinf, 35, z[1]-z[0])

    wdir     = generate_v(z, D, pair[1])
    wdir     = -smooth_piecewise(wdir, 35, z[1]-z[0])
    cor_func = interp1d(wdir, z, kind='linear')
    z_corr   = cor_func(0)
    dir_func = interp1d(z-z_corr,wdir,kind='linear', fill_value='extrapolate')
    wdir     = dir_func(z)
    
    vinf = np.full_like(z,1) * np.sin(np.deg2rad(wdir))

    u = Ufst*uinf
    v = Ufst*vinf

    u[u == -0.00] = 0.0
    v[v == -0.00] = 0.0

    # calculate wind direction in compass coordinates
    # wdir = np.mod(180+np.rad2deg(np.arctan2(u, v)), 360)

    wdir = wdir + 270

    z = z + zhub

    znondim = (z - zhub)/D

    ######################################################################
    # Plot profiles

    if(plot_profiles):

        # Create a figure with a custom gridspec layout
        fig, axs = plt.subplots(
            nrows = 2,
            ncols = 3,
            figsize = (10, 6),
            constrained_layout = True,
        )

        # Merge the third column into a single subplot
        big_ax = fig.add_subplot(2, 3, (3, 6))  # Span rows for the third column

        # Add titles and sample data
        axs[0, 0].set_title("Nondimensional velocity")
        axs[0, 1].set_title("Nondimensional direction")
        axs[1, 0].set_title("Dimensional velocity")
        axs[1, 1].set_title("Dimensional direction")
        big_ax.set_title("Wind speed magnitude")

        axs[0, 2].axis('off')
        axs[1, 2].axis('off')

        # non-dimensional
        # velocity profiles
        axs[0, 0].axhline(-0.5, linestyle='dashed', linewidth=1, dashes=(8, 3))
        axs[0, 0].axhline(zmid, linestyle='dotted', linewidth=1)
        axs[0, 0].axhline(0.5,  linestyle='dashed', linewidth=1, dashes=(8, 3))
        axs[0, 0].axvline((Ufst/Ufst)-1, linestyle='dotted', linewidth=1)
        axs[0, 0].axvline(Ufst/Ufst, linestyle='dotted', linewidth=1)
        axs[0, 0].plot(uinf[:], znondim, color='#0000FF', linestyle='solid', label=r'$u_{inflow}$')
        axs[0, 0].plot(vinf[:], znondim, color='#E50000', linestyle='solid', label=r'$v_{inflow}$')
        axs[0, 0].set_xlim([-1.0, 2.0])
        axs[0, 0].set_ylim([-zhub/D, zhub/D])
        axs[0, 0].set_xticks(np.arange(0.0, 3.0, 1.0))
        axs[0, 0].set_xlabel(r'$u_{i}/U_{\infty}~[-]$')
        axs[0, 0].set_ylabel(r'$(z-z_{h})/D~[-]$')

        # wind direction
        axs[0, 1].axhline(-0.5, linestyle='dashed', linewidth=1, dashes=(8, 3))
        axs[0, 1].axhline(zmid, linestyle='dotted', linewidth=1)
        axs[0, 1].axhline(0.5,  linestyle='dashed', linewidth=1, dashes=(8, 3))
        axs[0, 1].axvline(270.0, linestyle='dotted', linewidth=1)
        axs[0, 1].plot(wdir[:], znondim, color='#006400', linestyle='solid', label=r'_nolegend_')
        axs[0, 1].set_xlim([170.0, 370.0])
        axs[0, 1].set_ylim([-zhub/D, zhub/D])
        # axs[0, 1].set_xticks(np.arange(210.0, 330.0, 30.0))
        axs[0, 1].set_xlabel(r'$\beta~[\textrm{$^{\circ}$}]$')
        axs[0, 1].set_ylabel(r'$(z-z_{h})/D~[-]$')
        
        # dimensional
        # velocity profiles
        axs[1, 0].axhline(zhub-(0.5*D), linestyle='dashed', linewidth=1, dashes=(8, 3))
        axs[1, 0].axhline(zhub, linestyle='dotted', linewidth=1)
        axs[1, 0].axhline(zhub+(0.5*D), linestyle='dashed', linewidth=1, dashes=(8, 3))
        axs[1, 0].axvline(0.0, linestyle='dotted', linewidth=1)
        axs[1, 0].axvline(Ufst, linestyle='dotted', linewidth=1)
        axs[1, 0].plot(u[:], z, color='#0000FF', linestyle='solid', label=r'$u_{inflow}$')
        axs[1, 0].plot(v[:], z, color='#E50000', linestyle='solid', label=r'$v_{inflow}$')
        axs[1, 0].set_xlim([-Ufst, Ufst*2])
        axs[1, 0].set_ylim([0, height])
        axs[1, 0].set_xticks(np.arange(-8, Ufst+10, 4))
        # axs[1, 0].set_yticks(np.arange(min(z), max(z)+250.0, 250.0))
        axs[1, 0].set_xlabel(r'$u_{i}~[\textrm{m~s$^{-1}$}]$')
        axs[1, 0].set_ylabel(r'$z~[\textrm{m}]$')
        
        # wind direction
        axs[1, 1].axhline(zhub-(0.5*D), linestyle='dashed', linewidth=1, dashes=(8, 3))
        axs[1, 1].axhline(zhub, linestyle='dotted', linewidth=1)
        axs[1, 1].axhline(zhub+(0.5*D), linestyle='dashed', linewidth=1, dashes=(8, 3))
        axs[1, 1].axvline(270.0, linestyle='dotted', linewidth=1)
        axs[1, 1].plot(wdir[:], z, color='#006400', linestyle='solid', label=r'_nolegend_')
        test_z    = np.linspace((-0.5*D),(0.5*D), 20)
        test_line = -pair[1]/10 * test_z
        axs[1, 1].plot(test_line + 270, test_z + zhub, color='orange', linestyle='solid', label=r'_nolegend_')

        tip_deg = np.interp(zhub-0.5*D,z,wdir)
        diff = (((test_line[0] + 270) - tip_deg) + 180) % 360 - 180
        axs[1, 1].text(275, 700, f"Tip error: {abs(diff):.2f} deg", fontsize=6, color="k", ha='left')

        if wdir[-1] <= 180:
            axs[1, 1].text(275, 660, f"RESVERSE FLOW", fontsize=6, color='r', ha='left', fontweight='bold')

        axs[1, 1].set_xlim([170.0, 370.0])
        axs[1, 1].set_ylim([0, height])
        # axs[1, 1].set_xticks(np.arange(210.0, 330.0, 30.0))
        # axs[1, 1].set_yticks(np.arange(min(z), max(z)+250.0, 250.0))
        axs[1, 1].set_xlabel(r'$\beta~[\textrm{$^{\circ}$}]$')
        axs[1, 1].set_ylabel(r'$z~[\textrm{m}]$')

        # wind speed magnitude
        big_ax.axhline(zhub-(0.5*D), linestyle='dashed', linewidth=1, dashes=(8, 3))
        big_ax.axhline(zhub, linestyle='dotted', linewidth=1)
        big_ax.axhline(zhub+(0.5*D), linestyle='dashed', linewidth=1, dashes=(8, 3))
        # big_ax.axvline(0.0, linestyle='dotted', linewidth=1)
        big_ax.axvline(Ufst, linestyle='dotted', linewidth=1)
        big_ax.plot((u[:]**2 + v[:]**2)**(0.5), z, color='#730080', linestyle='solid')
        big_ax.set_xlim([Ufst-2, 15])
        big_ax.set_ylim([0, height])
        # big_ax.set_xticks(np.arange(-8, Ufst+10, 4))
        # big_ax.set_yticks(np.arange(min(z), max(z)+250.0, 250.0))
        big_ax.set_xlabel(r'Wind speed $[\textrm{m~s$^{-1}$}]$')
        big_ax.set_ylabel(r'$z~[\textrm{m}]$')

        plt.savefig(figure_path + '/' + figure_name + '.png', bbox_inches="tight", dpi=600)

        plt.show()

    ######################################################################
    # write to sounding file
    theta = 288.0 # temperature in K
    w     = 0.0 # water vapor mixing ratio in g kg-1

    mask = (z >= 0) & (z <= height * 1.1)

    z_clip = z[mask]
    u_clip = u[mask]
    v_clip = v[mask]

    theta = theta * np.ones(len(z_clip))
    w     = w * np.ones(len(z_clip))

    fmt = '%1.2f %1.2f %1.2f %1.2f %1.2f'

    prependline = r"1000.00 288.00 00.00"

    filepath = current_path + '/' + 'input_sounding'
    
    # Open the file in write mode
    with open(filepath, 'w') as f:
        # Write the prepended line first
        f.write(prependline + '\n')
        
        # Append the NumPy array data
        np.savetxt(f, np.stack([z_clip, theta, w, u_clip, v_clip], axis=1), fmt=fmt)

# ==================================================================
# MAIN LOGIC
# ==================================================================

# Create a Rich table summary
console = Console()
combinations = [pair for pair in product(shear, veer) if pair not in excluded_pairs]

# Determine the number of digits for formatting
int_digits, frac_digits = determine_format(shear, veer)

# Display combinations
table = Table(title = "Combinations")
table.add_column("Case",  justify = "right")
table.add_column("Shear", justify = "right", style = "green")
table.add_column("Veer",  justify = "right", style = "red")

# Format each value for table display with decimal points
for idx, (s, v) in enumerate(combinations, start=1):
    shear_str = f"{s: {int_digits + frac_digits + 1}.{frac_digits}f}"
    veer_str  = f"{v: {int_digits + frac_digits + 1}.{frac_digits}f}"
    table.add_row(str(idx), shear_str, veer_str)

console.print(table)

# Get turbine information
D, zhub = parse_turbineProperties(f'./case/windTurbines/{turbine}/turbineProperties.tbl')

def create_directories(combinations, excluded_pairs, console, header, model):

    # Initialize the success flag
    success = True

    # Check if the top directory already exists
    top_dir = f"{base_dir}/{model}"
    if os.path.exists(top_dir):
        with Live(console=console) as live:
            live.update(f"{header} Skipped, already exists.")
        return False 
    
    # Make top directory
    os.makedirs(f"{base_dir}/{model}/figs", exist_ok=False)

    # Clip model string for further use
    model_str = model.split('_')[0].lower()

    # Create batch submit file if requested
    batch_file_path = f"{base_dir}/submit_group_{model_str}.sh"

    if batch_submit:
        with open(batch_file_path, 'w') as batch_file:
            batch_file.write("#!/bin/bash\n\n")

    # Initialize Live for dynamic updates
    with Live(console=console) as live:
        live.update(f"{header} Creating summary table...")

        params = {}
        params['read_from']   = '.'
        params['name_path']   = f'./namelists/{model_str}_namelist.input'
        params['save_to']     = f'{base_dir}/{model}'
        params['turb_model']  = turbine
        params['rotor_model'] = model_str.upper()
        params['save_both']   = plot_domain 
        params['outer_pad']   = 75
        params['print_table'] = False
        params['slice_loc']   = max_sample

        # print('point 1')

        namelist, turbtuple = preproc.validate(opt_params=params)

        # print('point 2')

        ntasks = namelist.nproc_x * namelist.nproc_y

        if turbtuple.rot_dir == 1:
            rot_dir = 'cw'
        if turbtuple.rot_dir == -1:
            rot_dir = 'ccw'
        if turbtuple.rot_dir == 0:
            rot_dir = 'irr'

        counter = 1

        # Only create pairs requested
        for pair in combinations:
            if pair in excluded_pairs:
                continue

            # Update the live console output for each loop iteration
            live.update(f"{header} Case: {counter}. ({pair[0]},{pair[1]})")

            # Format shear and veer values
            shear_str = format_value(pair[0], int_digits, frac_digits)
            veer_str = format_value(pair[1], int_digits, frac_digits)
            dir_name = f"s{shear_str}_v{veer_str}"
            current_path = f"{base_dir}/{model}/{dir_name}"

            # Create shear + veer directory
            os.makedirs(current_path, exist_ok=False)

            # Create sounding file
            create_sounding(current_path, f"{base_dir}/{model}/figs", dir_name, pair, namelist.ztop)

            # Create symbolic links the executables
            create_symlinks(current_path)

            # Copy items in case template directory
            for item in os.listdir('./case'):
                source_path = os.path.join('./case', item)
                if os.path.isfile(source_path):  # Check if the item is a file
                    copy_files(source_path, os.path.join(current_path, item))

            # Copy requested turbine directory
            turb_source_dir = f'./case/windTurbines/{turbine}'
            destination_dir = os.path.join(current_path, 'windTurbines', turbine)

            if os.path.exists(turb_source_dir) and os.path.isdir(turb_source_dir):
                os.makedirs(os.path.join(current_path, 'windTurbines'), exist_ok=False)
                shutil.copytree(turb_source_dir, destination_dir)
            else:
                live.update(f"{header} ERROR. Source directory {turb_source_dir} does not exist.")
                return False
            
            # Copy wind turbine database
            shutil.copy2('./case/windTurbines/windTurbineTypes.dat', os.path.join(current_path, 'windTurbines'))

            # Copy additional files
            file_map = {
                f'./namelists/{model_str}_namelist.input': 'namelist.input',
                f'./turbines/{model_str}_windturbines-ij.dat': 'windturbines-ij.dat',
                f'./shell/export_libs_load_modules_{system}.sh': 'export_libs_load_modules.sh',
                f'./shell/submit_template_{system}.sh': 'submit.sh',
            }
            for src, dst in file_map.items():
                copy_files(src, os.path.join(current_path, dst))

            # Update file placeholders with requested values
            replacements = {
                "lib_path": library_path.replace("/", "\\/"),
                "{PH_JOB_NAME}": f"{dir_name}_{model_str}_{rot_dir}",
                "{PH_ALLOCATION}": f"{allocation}",
                "{PH_NTASKS}": ntasks,
                "{PH_TIME}": f"{runtime}",
            }
            for key, val in replacements.items():
                run_subprocess(['sed', '-i', f"s/{key}/{val}/g", os.path.join(current_path, 'export_libs_load_modules.sh')])
                run_subprocess(['sed', '-i', f"s/{key}/{val}/g", os.path.join(current_path, 'submit.sh')])

            if batch_submit:
                with open(batch_file_path, 'a') as batch_file:
                    batch_file.write(f"cd {current_path}\nsbatch submit.sh\n\n")

            counter = counter + 1

        os.chmod(batch_file_path, 0o777)

        live.update(f"{header} Done.")  # Final message

        return success

# ==================================================================
# EXECUTE
# ==================================================================

if GAD:
    header = "[bold yellow]Working on GAD Sweep.[/bold yellow]"
    print('\n')
    flag = create_directories(combinations, excluded_pairs, console, header, 'gad_sweep')

if GAL:
    header = "[bold yellow]Working on GAL Sweep.[/bold yellow]"
    print('\n')
    flag = create_directories(combinations, excluded_pairs, console, header, 'gal_sweep')

if GADrs:
    header = "[bold yellow]Working on GADrs Sweep.[/bold yellow]"
    print('\n')
    flag = create_directories(combinations, excluded_pairs, console, header, 'gadrs_sweep')

if flag:
    console.print("\n[bold green]Success.[/bold green]\n")
else:
    console.print("\n")