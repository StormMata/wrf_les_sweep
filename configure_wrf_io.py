#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

from wrf_io import sweep

# ==================================================================
# INPUTS
# ==================================================================

sweep_params = {}

sweep_params['shear']          = [-4, -2, 0, 2, 4]
sweep_params['veer']           = [-4, -2, 0, 2, 4]
sweep_params['excluded_pairs'] = [(-4,4), (-2,4), (2,4), (4,4),
                                  (-4,2), (4,2),
                                  (-4,-2), (4,-2),
                                  (-4,-4), (-2,-4), (2,-4), (4,-4)]

sweep_params['Ufst']           = 7.0
sweep_params['GAD']            = True
sweep_params['GAL']            = False
sweep_params['GADrs']          = False
sweep_params['max_sample']     = 10

sweep_params['base_dir']       = '/anvil/scratch/x-smata/wrf_les_sweep/runs/counterclockwise'
sweep_params['wrf_path']       = '/home/x-smata/to_storm/WRF-4.6.0'
sweep_params['library_path']   = '/home/x-smata/libraries/libinsdir'
sweep_params['turbine']        = 'iea10MW'
sweep_params['allocation']     = 'atm170028'
sweep_params['runtime']        = '48:00:00'

sweep_params['max_sample']     = 10
sweep_params['batch_submit']   = True
sweep_params['plot_profiles']  = True
sweep_params['plot_domain']    = True

plt.rcParams['text.usetex'] = True

# ==================================================================
# EXECUTE
# ==================================================================

if sweep_params['GAD']:
    header = "[bold yellow]Working on GAD Sweep.[/bold yellow]"
    print('\n')
    flag = sweep.setup(sweep_params, console, header, 'gad_sweep')

if sweep_params['GAL']:
    header = "[bold yellow]Working on GAL Sweep.[/bold yellow]"
    print('\n')
    flag = create_directories(combinations, excluded_pairs, console, header, 'gal_sweep')

if sweep_params['GADrs']:
    header = "[bold yellow]Working on GADrs Sweep.[/bold yellow]"
    print('\n')
    flag = create_directories(combinations, excluded_pairs, console, header, 'gadrs_sweep')

if flag:
    console.print("\n[bold green]Success.[/bold green]\n")
else:
    console.print("\n")