"""
OSDAG Screening Task - Task 2: 3D Visualization
-----------------------------------------------
File: task2_3d.py
Author: Divit Singhania
Description:
    Generates 3D Shear Force (SFD) and Bending Moment (BMD) diagrams
    for ALL 5 Girders.

    Implementation Details (MIDAS Style):
    1. Vertical Extrusion: Forces are mapped to the Y-axis.
    2. Vertical Hatching: Uses dense lines ("Fence Plot") instead of solid mesh for transparency.
    3. Heat Map Coloring: Applies 'Jet' colorscale (Blue->Red) based on magnitude.
    4. Aspect Ratio Correction: X and Y axes are manually scaled to make forces visible.
"""

import xarray as xr
import plotly.graph_objects as go
from data.node import nodes
from data.element import members
import os

# 1. SETUP & DATA DEFINITION
DATA_PATH = os.path.join("..", "data", "screening_task.nc")
ds = xr.open_dataset(DATA_PATH)

# Dictionary defining the structural topology for all 5 girders
GIRDERS = {
    "Girder 1": {"elements": [13, 22, 31, 40, 49, 58, 67, 76, 81], "nodes": [1, 11, 16, 21, 26, 31, 36, 41, 46, 6]},
    "Girder 2": {"elements": [14, 23, 32, 41, 50, 59, 68, 77, 82], "nodes": [2, 12, 17, 22, 27, 32, 37, 42, 47, 7]},
    "Girder 3": {"elements": [15, 24, 33, 42, 51, 60, 69, 78, 83], "nodes": [3, 13, 18, 23, 28, 33, 38, 43, 48, 8]},
    "Girder 4": {"elements": [16, 25, 34, 43, 52, 61, 70, 79, 84], "nodes": [4, 14, 19, 24, 29, 34, 39, 44, 49, 9]},
    "Girder 5": {"elements": [17, 26, 35, 44, 53, 62, 71, 80, 85], "nodes": [5, 15, 20, 25, 30, 35, 40, 45, 50, 10]}
}

def create_midas_polished_plot(comp_i, comp_j, title):
    """
    Generates a 3D structural analysis plot.

    Args:
        comp_i, comp_j: Force components (e.g. 'Vy_i')
        title: Plot title
    """
    fig = go.Figure()
    diagram_type = "SFD" if "Vy" in comp_i else "BMD"

    # --- A. GLOBAL SCALING CALCULATIONS ---
    # We must scan ALL girders to find the global Max/Min forces.
    # This ensures that "Red" means the same force magnitude on Girder 1 as Girder 5.
    all_forces = []
    for g_data in GIRDERS.values():
        for eid in g_data["elements"]:
            v_i = float(ds.forces.sel(Element=eid, Component=comp_i))
            v_j = float(ds.forces.sel(Element=eid, Component=comp_j))
            all_forces.extend([v_i, v_j])

    # 1. Height Scaling:
    # Forces are typically much larger than bridge dimensions (e.g., 200kN vs 25m).
    # We scale forces to be approx 5 meters high visually.
    abs_forces = [abs(f) for f in all_forces]
    max_abs_val = max(abs_forces) if abs_forces else 1.0
    TARGET_HEIGHT = 5.0
    HEIGHT_SCALE = TARGET_HEIGHT / max_abs_val

    # 2. Color Limits (for Heat Map):
    C_MIN, C_MAX = min(all_forces), max(all_forces)

    # 3. Z-Expansion Factor:
    # Artificially widens the bridge (1.5x) so inner girders aren't hidden by outer ones.
    Z_EXPANSION = 1.5

    print(f"Generating {title}...")
    print(f" - Max Force: {max_abs_val:.2f} | Scale Factor: {HEIGHT_SCALE:.4f}")

    # --- B. PLOTTING LOOP ---
    for g_name, data in GIRDERS.items():

        # 1. Plot Zero-Force Baseline (The Beam Axis)
        # We assume Y=0 is the neutral axis of the bridge.
        bx, by, bz = [], [], []
        for n in data["nodes"]:
            bx.append(nodes[n][0])
            by.append(0)
            bz.append(nodes[n][2] * Z_EXPANSION) # Apply visual expansion

        fig.add_trace(go.Scatter3d(
            x=bx, y=by, z=bz,
            mode='lines',
            line=dict(color='gray', width=3), # Grey structural line
            name=f"{g_name} Axis",
            showlegend=False
        ))

        # 2. Generate Diagram Geometry (Profile + Hatching)
        outline_x, outline_y, outline_z, outline_c = [], [], [], []
        hatch_x, hatch_y, hatch_z, hatch_c = [], [], [], []

        for eid in data["elements"]:
            sn, en = members[eid]
            x1, _, z1 = nodes[sn]
            x2, _, z2 = nodes[en]

            # Apply Z-Expansion
            z1 *= Z_EXPANSION
            z2 *= Z_EXPANSION

            val1 = float(ds.forces.sel(Element=eid, Component=comp_i))
            val2 = float(ds.forces.sel(Element=eid, Component=comp_j))

            # --- DIAGRAM LOGIC ---
            if diagram_type == "SFD":
                # Stepped Diagram: Constant Height & Color
                h1 = val1 * HEIGHT_SCALE
                h2 = val1 * HEIGHT_SCALE
                c1, c2 = val1, val1
            else:
                # Linear Diagram: Sloped Height & Gradient Color
                h1 = val1 * HEIGHT_SCALE
                h2 = val2 * HEIGHT_SCALE
                c1, c2 = val1, val2

            # Append Top Profile Data
            # 'None' breaks the line between elements for the discrete look
            outline_x.extend([x1, x2, None])
            outline_y.extend([h1, h2, None])
            outline_z.extend([z1, z2, None])
            outline_c.extend([c1, c2, c2])

            # Append Vertical Hatching Data (The "Fence")
            num_lines = 10
            for k in range(num_lines + 1):
                frac = k / num_lines

                # Interpolate geometry
                cx = x1 + (x2 - x1) * frac
                cz = z1 + (z2 - z1) * frac
                ch = h1 + (h2 - h1) * frac

                # Interpolate color (creates gradient for BMD)
                cc = c1 + (c2 - c1) * frac

                # Draw vertical line from 0 to h
                hatch_x.extend([cx, cx, None])
                hatch_y.extend([0, ch, None])
                hatch_z.extend([cz, cz, None])
                hatch_c.extend([cc, cc, cc])

        # Trace 3: The Top Profile (Thick Line)
        fig.add_trace(go.Scatter3d(
            x=outline_x, y=outline_y, z=outline_z,
            mode='lines',
            line=dict(width=6, color=outline_c, colorscale='Jet', cmin=C_MIN, cmax=C_MAX, showscale=False),
            showlegend=False
        ))

        # Trace 4: The Hatching (Semi-Transparent Fill)
        fig.add_trace(go.Scatter3d(
            x=hatch_x, y=hatch_y, z=hatch_z,
            mode='lines',
            line=dict(
                width=3,
                color=hatch_c,
                colorscale='Jet',
                cmin=C_MIN, cmax=C_MAX,
                # Show colorbar only once (for Girder 1)
                showscale=True if g_name == "Girder 1" else False,
                colorbar=dict(
                    title=f"<b>Internal Force<br>({'kN' if 'Vy' in comp_i else 'kN-m'})</b>",
                    x=0.9, len=0.6, thickness=15
                )
            ),
            opacity=0.75,
            showlegend=False
        ))

    # --- C. LAYOUT & CAMERA ---
    fig.update_layout(
        title=f"<b>3D {title} Analysis</b>",
        scene=dict(
            xaxis_title="Length (X)",
            yaxis_title="Force Magnitude (Exaggerated)",
            zaxis_title="Width (Z)",

            # 📌 ASPECT MODE: Manual
            # We exaggerate Y (force) and X (length) relative to Z (width)
            # This mimics the MIDAS visual style where diagrams stand out clearly.
            aspectmode='manual',
            aspectratio=dict(x=3.0, y=1.5, z=1.2),

            # Clean Technical Background
            xaxis=dict(showbackground=False, gridcolor="lightgray", zerolinecolor="black"),
            yaxis=dict(showbackground=False, gridcolor="lightgray"),
            zaxis=dict(showbackground=False, gridcolor="lightgray"),
            bgcolor="white",

            # Isometric Camera Angle
            camera=dict(eye=dict(x=1.6, y=0.8, z=1.6))
        ),
        margin=dict(t=60, b=20, l=0, r=0)
    )
    return fig

# MAIN EXECUTION
if __name__ == "__main__":
    print("Generating 3D Plots...")

    # 1. Generate 3D Shear Force Diagram
    fig_sfd = create_midas_polished_plot("Vy_i", "Vy_j", "Shear Force (SFD)")
    fig_sfd.show()

    # 2. Generate 3D Bending Moment Diagram
    fig_bmd = create_midas_polished_plot("Mz_i", "Mz_j", "Bending Moment (BMD)")
    fig_bmd.show()