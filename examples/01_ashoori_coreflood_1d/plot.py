#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post-processing and visualization script for Tutorial 1 (Ashoori 2011).
Generates publication-quality 1D spatial profiles and 2D/3D field renderings.
"""

import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.append(str(script_dir))

from plotter import FossilPlotter

output_dir = script_dir / "output_Ashoori2011/output"
if not output_dir.exists():
    output_dir = script_dir / "output_Ashoori2011"
if not output_dir.exists():
    output_dir = script_dir

# Initialize plotter for 2D/1D visualizations
plotter_2d = FossilPlotter(output_dir=str(output_dir), dim=2)

time_steps = [20, 40, 60, 80, 100]
time_labels = [
    r"$t = 20$ s",
    r"$t = 40$ s",
    r"$t = 60$ s",
    r"$t = 80$ s",
    r"$t = 100$ s"
]

print("Generating 1D spatial profile plots...")

# 1. Plot Water Saturation (Sw) 1D profile
plotter_2d.plot_spatial_1d(
    target_variable="Water_Saturation_mean",
    time_steps=time_steps,
    labels=time_labels,
    xlabel=r"Length $x$ [m]",
    ylabel=r"Water Saturation ($S_w$) [-]",
    save_as=str(script_dir / "ashoori_sw_1d.pdf")
)

# 2. Plot Foam Bubble Texture (nD) 1D profile
plotter_2d.plot_spatial_1d(
    target_variable="Foam_Texture_mean",
    time_steps=time_steps,
    labels=time_labels,
    xlabel=r"Length $x$ [m]",
    ylabel=r"Foam Texture ($n_D$) [-]",
    save_as=str(script_dir / "ashoori_nd_1d.pdf")
)

target_step = 100

print("Generating 2D and 3D spatial maps...")

# 3. 2D Spatial Map (XY top-view)
plotter_2d.plot_spatial_mesh(
    target_variable="Water_Saturation_mean",
    time_step=target_step,
    cmap="jet_r",
    save_as=str(script_dir / "ashoori_sw_2d.pdf")
)

# Isolated colorbar
plotter_2d.plot_isolated_colorbar(
    label_name="Water Saturation",
    cmap="jet_r",
    save_as=str(script_dir / "ashoori_sw_2d_cbar.pdf"),
    orientation="horizontal"
)

# 4. 3D Spatial Map (Isometric view with vertical exaggeration)
plotter_3d = FossilPlotter(output_dir=str(output_dir), dim=3)
plotter_3d.plot_spatial_mesh(
    target_variable="Foam_Texture_mean",
    time_step=target_step,
    cmap="viridis",
    z_scale=5.0,
    save_as=str(script_dir / "ashoori_nd_3d.pdf")
)

plotter_3d.plot_isolated_colorbar(
    label_name="Foam Texture",
    cmap="viridis",
    save_as=str(script_dir / "ashoori_nd_3d_cbar.pdf"),
    orientation="horizontal"
)

print("Plotting process completed successfully!")
