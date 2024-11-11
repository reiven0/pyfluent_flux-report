# pyfluent_flux-report

This repository contains a Python script for generating and saving a flux report.

## Description

The `flux-report.py` script provides the following functionality:

- Generates a flux report using a given configuration
- Saves the report results to a CSV file in the `result_folder` directory

## Usage

1. Ensure you have Python and the required dependencies installed.
2. The Python code should be pasted and executed within the Solution > Calculation Activities > Execute Commands section.
   
   ![readme_en-excute](https://github.com/user-attachments/assets/a14f4161-1c54-42a1-944d-dec567d9f770)

3. :white_check_mark:Please change the contents of 'boundaries=["cha", "chb", "chc", "chd"]' to suit your environment.

## Prerequisites

- This script is designed to be used with a Workbench parameter set, executed from the Table Design Point.
- The script has been tested on 2024R2.03.
- The intermediate analysis files are saved to a path like 'A:\Temp\multi_surface_test@Fluent\cylinder01_files\dp0\FLU\Fluent'.
  The result_folder is created in the parent directory three levels up from the above path (cylinder01_files), and the CSV file is saved there.
- The DP (Design Point) number is extracted from the above path and added to the beginning of the file name.
　(For example, dp0_output.csv)

  ![result_csv](https://github.com/user-attachments/assets/431ce53f-3b9e-47a2-bd1c-c351a09bd956)
