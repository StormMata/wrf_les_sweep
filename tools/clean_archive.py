#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import fnmatch

# Change this to your top-level directory
MASTER_DIR = '/scratch/09909/smata/wrf_les_sweep/runs/archive'

# Patterns to match
PATTERNS = ['rsl.*', 'wrfout_d01*', 'wrfout_d02*']

def matches_any_pattern(filename, patterns):
    return any(fnmatch.fnmatch(filename, pattern) for pattern in patterns)

def delete_matching_files(root_dir, patterns):
    deleted_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if matches_any_pattern(filename, patterns):
                filepath = os.path.join(dirpath, filename)
                try:
                    os.remove(filepath)
                    deleted_files.append(filepath)
                    print(f"Deleted: {filepath}")
                except Exception as e:
                    print(f"Failed to delete {filepath}: {e}")
    print(f"\nFinished. {len(deleted_files)} files deleted.")

if __name__ == "__main__":
    delete_matching_files(MASTER_DIR, PATTERNS)