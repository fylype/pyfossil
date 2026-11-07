# Tutorial 4: SPE 10 Model 2 Benchmark (3D Field Reservoir)

This tutorial implements the industry-standard **SPE 10 Dataset 2 (Christie & Blunt, 2001)** benchmark for waterflooding in a highly heterogeneous 3D channelized fluvial reservoir.

---

## 🎯 Learning Objectives
- Simulate a full-scale 3D field reservoir (1200 x 2200 x 170 ft) with 5 vertical wells (1 central injector and 4 corner producers).
- Implement 3D multi-layer Peaceman wells accounting for wellbore hydrostatic head (`include_hydrostatic_head`).
- Implement an **active in-situ step callback** (`set_step_callback`) with a **2% hysteresis deadband** to switch dynamically between target injection rate (5000 STB/D) and maximum Bottom-Hole Pressure limit (10,000 psi).
- Apply the **KPP (Kurganov-Petrova-Popova)** central-upwind scheme with cubic extrema reconstruction for non-convex fractional flow functions.
- Compare structured Cartesian grid simulation (`run_spe10_3d.py`) against 3D unstructured hybrid mesh with Local Grid Refinement (`run_spe10_unstructured_3d.py`).

---

## 📁 Included Files
- `run_spe10_3d.py`: 3D structured simulation with directional petrophysical upscaling.
- `run_spe10_unstructured_3d.py`: 3D unstructured simulation with LGR around well trajectories.
- `spe10_reservatorio_com_pocos.geo`: Gmsh CAD script with well perforations.
- `spe10_reservatorio_com_pocos.msh`: Pre-generated 3D tetrahedral mesh.
- `plot.py` and `plotter.py`: Benchmark comparison and production history plotting scripts.

---

## 🚀 How to Run

```bash
# 1. Execute the 3D simulation:
python run_spe10_3d.py

# 2. Generate production history, water cut, and well BHP plots:
python plot.py
```
