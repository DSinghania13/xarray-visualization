"""
OSDAG Screening Task - Task 1: 2D Force Diagrams
------------------------------------------------
File: task1_2d.py
Author: Divit Singhania
Description:
    Generates 2D Shear Force (SFD) and Bending Moment (BMD) diagrams
    for the Central Longitudinal Girder.

    Key Features:
    - Uses "Continuous Rough Analysis" style (vertical jumps at nodes).
    - Preserves Xarray sign convention (no manual flipping).
    - Includes darker internal hatching and zero-crossing labels.
"""

import xarray as xr
import plotly.graph_objects as go
import numpy as np
import os

# Import structural topology (Node coordinates and Element connectivity)
from data.element import members
from data.node import nodes

# CONFIGURATION
DATA_PATH = os.path.join("..", "data", "screening_task.nc")
CENTRAL_GIRDER_IDS = [15, 24, 33, 42, 51, 60, 69, 78, 83]

# Load Dataset
try:
    ds = xr.open_dataset(DATA_PATH)
except FileNotFoundError:
    print("Error: Dataset not found. Please check the DATA_PATH.")
    exit()


def generate_midas_style_plot(comp_i, comp_j, title, color, unit, is_step=False):
    """
    Generates a Plotly Figure for structural forces.

    Parameters:
    - comp_i, comp_j: Component names for start/end nodes (e.g., 'Vy_i', 'Vy_j')
    - title: Graph title
    - color: Line/Hatch color
    - unit: Force unit ('kN' or 'kN-m')
    - is_step: Boolean. True for SFD (stepped), False for BMD (linear).
    """
    fig = go.Figure()

    # Lists to store the continuous boundary path
    x_full_path = []
    y_full_path = []

    # Iterate through elements to build the diagram piece-by-piece
    for eid in CENTRAL_GIRDER_IDS:
        # 1. Get Node Coordinates
        start_node, end_node = members[eid]
        x_i = nodes[start_node][0]  # X-coordinate of start node
        x_j = nodes[end_node][0]  # X-coordinate of end node

        # 2. Get Force Values directly from Xarray
        # No manual sign flipping is performed, adhering to the dataset's convention.
        val_i = float(ds.forces.sel(Element=eid, Component=comp_i))
        val_j = float(ds.forces.sel(Element=eid, Component=comp_j))

        # 3. Define Segment Geometry
        if is_step:
            # SFD: Shear is constant along the element.
            # We visualize this as a flat "step".
            x_segment = [x_i, x_j]
            y_segment = [val_i, val_i]
            val_start, val_end = val_i, val_i
        else:
            # BMD: Moment varies linearly from node i to node j.
            x_segment = [x_i, x_j]
            y_segment = [val_i, val_j]
            val_start, val_end = val_i, val_j

        # Append to full path for the main boundary line
        x_full_path.extend(x_segment)
        y_full_path.extend(y_segment)

        # 4. Generate Internal Hatching (The "Rough" Look)
        # We generate vertical lines to create a "filled" structural diagram effect.
        hatch_density = 12
        hatch_x = np.linspace(x_i, x_j, hatch_density)

        for hx in hatch_x:
            # Interpolate Y value at this hatch position
            hy = val_start if is_step else val_start + (val_end - val_start) * (hx - x_i) / (x_j - x_i)

            # Add vertical line from y=0 to y=hy
            fig.add_shape(type="line", x0=hx, y0=0, x1=hx, y1=hy,
                          line=dict(color="rgba(30, 30, 30, 0.8)", width=1.3))

        # 5. Label Zero Crossings
        # Calculate exact intersection where force changes sign
        if not is_step and (val_i * val_j < 0):
            x_zero = x_i - val_i * (x_j - x_i) / (val_j - val_i)
            fig.add_annotation(
                x=x_zero, y=0, text=f"<b>x={x_zero:.2f} m</b>",
                showarrow=True, arrowhead=2, font=dict(color="green", size=10),
                bgcolor="white", bordercolor="green", yshift=20
            )

    # PLOTTING TRACES

    # Trace 1: The Main Boundary Line (with markers at nodes)
    fig.add_trace(go.Scatter(
        x=x_full_path, y=y_full_path,
        mode='lines+markers',
        marker=dict(size=4, color=color),
        line=dict(color=color, width=3),
        name=f"{title}"
    ))

    # Annotate Global Max/Min
    y_arr = np.array(y_full_path)
    max_idx, min_idx = np.argmax(y_arr), np.argmin(y_arr)

    for idx, label in [(max_idx, "MAX"), (min_idx, "MIN")]:
        fig.add_annotation(
            x=x_full_path[idx], y=y_full_path[idx],
            text=f"<b>{label}: {y_full_path[idx]:.3f} {unit}</b>",
            showarrow=True, arrowhead=2, bgcolor="white", bordercolor="black",
            font=dict(color=color, size=12)
        )

    # Layout Styling
    fig.update_layout(
        title=f"<b>{title} (Continuous Rough Analysis)</b>",
        xaxis_title="Bridge Longitudinal Axis (X) [m]",
        yaxis_title=f"Magnitude [{unit}]",
        template="simple_white",
        xaxis=dict(zeroline=True, zerolinecolor="black", zerolinewidth=2.5),
        showlegend=False
    )
    return fig


# MAIN EXECUTION
if __name__ == "__main__":
    print("Generating 2D Plots...")

    # 1. Shear Force Diagram
    fig_sfd = generate_midas_style_plot("Vy_i", "Vy_j", "SFD - Central Girder", "blue", "kN", is_step=True)
    fig_sfd.show()

    # 2. Bending Moment Diagram
    fig_bmd = generate_midas_style_plot("Mz_i", "Mz_j", "BMD - Central Girder", "red", "kN-m", is_step=False)
    fig_bmd.show()