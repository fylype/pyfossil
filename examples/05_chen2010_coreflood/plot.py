#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post-processing and comparison script for Tutorial 5 (Chen 2010).
Plots simulated 1D saturation and foam texture profiles against experimental CSV data.
"""

import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.append(str(script_dir))

from plotter import FossilPlotter

output_dir = script_dir / "output_Chen2010/output"
if not output_dir.exists():
    output_dir = script_dir / "output_Chen2010"
if not output_dir.exists():
    output_dir = script_dir

# Initialize plotter for 1D profile visualization
plotter_1d = FossilPlotter(output_dir=str(output_dir), dim=1)

time_steps = [1, 2, 3, 4, 5]
time_labels = [
    "$0.1$ PV",
    "$0.2$ PV",
    "$0.3$ PV",
    "$0.4$ PV",
    "$0.5$ PV"
]

print("Generating 1D comparison plots...")

# Reference experimental CSV data overlay
csv_files = ["PV_01.csv", "PV_02.csv", "PV_03.csv", "PV_04.csv", "PV_05.csv"]
csv_files = ["Experimental/" + item for item in csv_files]
extra_csvs_sw = []

for i, csv_file in enumerate(csv_files):
    csv_path = script_dir / csv_file
    if csv_path.exists():
        extra_csvs_sw.append({
            'file': str(csv_path),
            'label': f"Experimental - {time_labels[i]}",
            'x_scale': 0.6,
            'linestyle': '--',
            'linewidth': 1.5,
            'marker': plotter_1d.markers[i % len(plotter_1d.markers)],
            'color': plotter_1d.colors[i % len(plotter_1d.colors)],
            'markerfacecolor': 'none',
            'markersize': 7
        })

sim_labels = ["Simulation - " + item for item in time_labels]

# 1. Water Saturation (Sw) 1D profile
plotter_1d.plot_spatial_1d(
    target_variable="Water_Saturation_mean",
    time_steps=time_steps,
    labels=sim_labels,
    xlabel=r"Length $x$ [m]",
    ylabel=r"Water Saturation ($S_w$) [-]",
    save_as=str(script_dir / "chen2010_sw_1d.pdf"),
    extra_csvs=extra_csvs_sw if extra_csvs_sw else None,
    legend_ncol=2
)

# 2. Foam Bubble Texture (nD) 1D profile
plotter_1d.plot_spatial_1d(
    target_variable="Foam_Texture_mean",
    time_steps=time_steps,
    labels=sim_labels,
    xlabel=r"Length $x$ [m]",
    ylabel=r"Foam Texture ($n_D$) [-]",
    save_as=str(script_dir / "chen2010_nd_1d.pdf")
)

print("Plotting process completed successfully!")
