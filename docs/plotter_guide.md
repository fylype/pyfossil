# Post-Processing and Visualization: `FossilPlotter` Guide

`plotter.py` provides the **`FossilPlotter`** class, an automated, publication-quality post-processing and visualization engine designed specifically for FOSSIL simulation data.

---

## 1. Overview and Capabilities

`FossilPlotter` interfaces directly with FOSSIL output directories containing:
* **Unstructured VTU files (`volume_vars_*.vtu`):** Spatial saturation, pressure, foam texture, and surfactant distributions.
* **CSV history tables (`wells.csv`, `time_series.csv`):** Dynamic Bottom-Hole Pressures (BHP), cumulative fluid injection/production, and phase rates.

Key features:
* **Publication-Quality Styling:** Clean white background, crisp axis spines, configurable LaTeX font rendering, and automated legends.
* **Automated 1D Spatial Profiling:** Interpolates field variables along arbitrary 1D lines through 1D, 2D, or 3D meshes at multiple time steps.
* **Off-Screen 2D/3D Rendering:** Uses **PyVista** for headless 2D and 3D spatial field rendering and screenshot generation.
* **Standalone Colorbars:** Generates isolated, high-resolution horizontal/vertical colorbars suitable for multi-panel publication figures.

---

## 2. Installation and Dependencies

The plotting engine requires:
```bash
pip install numpy matplotlib pyvista pandas
```

*Optional:* If `latex` is installed on your operating system, `FossilPlotter` automatically enables LaTeX typography.

---

## 3. Initialization

```python
from plotter import FossilPlotter

plotter = FossilPlotter(
    output_dir="./output_SPE10_3D",
    dim=3,
    style="seaborn-v0_8-whitegrid",
    use_tex=True
)
```

### Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `output_dir` | `str` | *required* | Path to the directory where simulation VTU and CSV files are saved. |
| `dim` | `int` | `3` | Spatial dimension of the domain (`1`, `2`, or `3`). |
| `style` | `str` | `'seaborn-v0_8-whitegrid'` | Matplotlib stylesheet name. |
| `use_tex` | `bool` | `True` | Enables LaTeX font rendering if `latex` executable is found in `PATH`. |

---

## 4. Key Methods and Usage

### 4.1. Plotting 1D Spatial Profiles (`plot_spatial_1d`)

Extracts and plots line profiles of any scalar field variable across multiple time steps.

```python
plotter.plot_spatial_1d(
    target_variable="water_saturation",
    time_steps=[10, 50, 100, 200],
    xlabel="Core Length [m]",
    ylabel="Water Saturation [-]",
    save_path="profiles_Sw.png",
    axis=0,                 # 0 = X-axis, 1 = Y-axis, 2 = Z-axis
    y_limits=(0.0, 1.0),
    title="Water Saturation Advance Along Core"
)
```

### 4.2. Plotting Time-Series History (`plot_history`)

Reads CSV logs produced by wells or global integrators and generates multi-curve time-series plots.

```python
plotter.plot_history(
    filename="wells.csv",
    col_x="time_days",
    cols_y=["INJ1_bhp_psi", "P1_bhp_psi"],
    xlabel="Time [days]",
    ylabel="Bottom-Hole Pressure [psi]",
    save_path="bhp_history.png",
    labels=["Injector 1", "Producer 1"],
    title="Well Pressure Responses"
)
```

### 4.3. 2D and 3D Mesh Rendering (`plot_spatial_mesh`)

Renders 2D or 3D scalar fields directly using PyVista off-screen rendering.

```python
plotter.plot_spatial_mesh(
    target_variable="gas_saturation",
    time_step=150,
    save_path="gas_plume_3d.png",
    cmap="jet_r",
    clim=[0.0, 0.8],
    camera_position="iso",      # 'xy', 'xz', 'yz', or 'iso'
    show_edges=False
)
```

### 4.4. Standalone Colorbar Export (`plot_isolated_colorbar`)

Creates a standalone colorbar graphic for external report formatting.

```python
plotter.plot_isolated_colorbar(
    label_name="Dimensionless Foam Texture $n_D$ [-]",
    cmap="viridis",
    vmin=0.0,
    vmax=1.0,
    orientation="horizontal",
    save_path="colorbar_foam_texture.png"
)
```

---

## 5. Complete Example Script

```python
#!/usr/bin/env python3
from plotter import FossilPlotter

def main():
    # Instantiate plotter pointing to simulation output
    plotter = FossilPlotter(output_dir="./output_case", dim=2)

    # 1. Plot pressure and saturation along core
    plotter.plot_spatial_1d(
        target_variable="water_saturation",
        time_steps=[0, 25, 50, 100],
        xlabel="X Position [m]",
        ylabel="Water Saturation [-]",
        save_path="water_saturation_evolution.png"
    )

    # 2. Render 2D map at final time step
    vtu_files = plotter.get_vtu_files()
    last_step = len(vtu_files) - 1
    plotter.plot_spatial_mesh(
        target_variable="pressure",
        time_step=last_step,
        save_path="pressure_field_final.png",
        cmap="turbo"
    )

if __name__ == "__main__":
    main()
```
