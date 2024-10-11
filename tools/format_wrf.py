#!/usr/bin/env python3
import argparse

def format_namelist(input_file, output_file):
    """
    Formats a WRF namelist file to ensure proper alignment and indentation,
    ignoring commented lines.
    """
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    formatted_lines = []
    in_group = False  # Tracks whether we are inside a namelist group

    for line in lines:
        # Strip leading/trailing whitespace
        line = line.strip()

        # Skip empty lines and commented lines (starting with '!')
        if not line or line.startswith('!'):
            formatted_lines.append(line + '\n')  # Preserve the empty/commented line
            continue

        # Detect group start (e.g., &time_control)
        if line.startswith('&'):
            in_group = True
            formatted_lines.append(line + '\n')
            continue

        # Detect group end (e.g., /)
        if line == '/':
            in_group = False
            formatted_lines.append(line + '\n\n')  # Add blank line after group for clarity
            continue

        # Inside a group, format the parameters
        if in_group:
            if '=' in line:
                # Split parameter and value, then align the '=' sign
                param, value = line.split('=', 1)
                param = param.strip()
                value = value.strip()
                formatted_lines.append(f'{param:25} = {value}\n')
            else:
                # For continuation lines without '='
                formatted_lines.append(line + '\n')
    
    # Write the formatted content to the output file
    with open(output_file, 'w') as outfile:
        outfile.writelines(formatted_lines)

    print(f"Formatted namelist saved to {output_file}")


def main():
    # Set up command line argument parsing with help texts
    parser = argparse.ArgumentParser(
        description="Format a WRF namelist file to align parameters and ensure consistency, ignoring comments.",
        epilog="Example: python format_namelist.py namelist.input formatted_namelist.input"
    )
    
    # Add input file argument with help text
    parser.add_argument('input_file', help="The input namelist file to format (e.g., namelist.input).")
    
    # Add output file argument with help text
    parser.add_argument('output_file', help="The output file where the formatted namelist will be saved (e.g., formatted_namelist.input).")

    # Parse the arguments
    args = parser.parse_args()

    # Format the namelist using the provided input and output files
    format_namelist(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
