"""
OSDAG Screening Task - Dataset Verification Script
--------------------------------------------------
File: xarray_usage.py
Author: Divit Singhania
Description:
    This script fulfills the foundational requirements:
    1. Loads the .nc dataset correctly using Xarray.
    2. Identifies the specific indices/names for Shear Force (Vy) and Bending Moment (Mz).
    3. Extracts the raw data for the 'Central Longitudinal Girder' elements.
"""

import xarray as xr
import os
import pandas as pd

# 1. LOAD DATASET
# Construct absolute or relative path to ensure cross-platform compatibility
nc_path = os.path.join("..", "data", "screening_task.nc")

try:
    ds = xr.open_dataset(nc_path)
    print(f"SUCCESS: Dataset loaded from {nc_path}")
    print("-" * 50)
except FileNotFoundError:
    print(f"ERROR: Could not find file at {nc_path}. Check your directory structure.")
    exit()

# 2. IDENTIFY COMPONENTS (Mz & Vy)
# The task requires:
# - Vy_i, Vy_j : Shear Force at start(i) and end(j) nodes
# - Mz_i, Mz_j : Bending Moment at start(i) and end(j) nodes

required_components = ["Vy_i", "Vy_j", "Mz_i", "Mz_j"]
available_components = ds.Component.values.tolist()

print("Verifying Components:")
for comp in required_components:
    if comp in available_components:
        print(f" [✓] Found Component: {comp}")
    else:
        print(f" [X] MISSING Component: {comp}")
print("-" * 50)

# 3. EXTRACT VALUES FOR CENTRAL GIRDER
# Element IDs provided in the Task 1 description
central_girder_ids = [15, 24, 33, 42, 51, 60, 69, 78, 83]

print(f"Extracting data for Central Girder Elements: {central_girder_ids}\n")

# Use Xarray's .sel() functionality for efficient data slicing
# This extracts all required components for all required elements in one go
girder_data = ds.forces.sel(
    Element=central_girder_ids,
    Component=required_components
)

# Convert to DataFrame for readable display/verification
df = pd.DataFrame(girder_data.values, index=central_girder_ids, columns=required_components)
df.index.name = "Element_ID"

print("Extracted Data Sample:")
print(df)
print("-" * 50)
print("VERIFICATION COMPLETE: Data is ready for plotting.")