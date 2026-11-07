# Tutorials & Benchmarks Guide

The `examples/` directory in the repository provides 7 ready-to-run simulation setups. Each tutorial includes a fully commented Python driver script, required mesh files (`.msh`, `.geo`), input data arrays (`.dat`), post-processing visualization scripts (`plot.py`), and a dedicated `README.md`.

---

## 📋 Benchmark Catalog

| Tutorial | Directory | Domain & Dimension | Physical Phenomena | Linear Solvers & Preconditioners |
| :--- | :--- | :--- | :--- | :--- |
| **01** | `01_ashoori_coreflood_1d` | 1D / 200 cells | Ashoori et al. (2011) experimental coreflood; bubble generation, coalescing transition, and mobility reduction. | UMFPACK + JFNK GMRES |
| **02** | `02_unstructured_2d_materials` | 2D Unstructured Gmsh with well cavity | Multi-region petrophysical mapping (4 `Material IDs`), Kovscek Local Equilibrium foam, surfactant transport, real-gas PVT density table. | BiCGSTAB + BoomerAMG |
| **03** | `03_unstructured_3d_hole` | 3D Tetrahedral Gmsh with well cavity | Radial injection from perforation cavity, 3D spatially correlated log-normal rock field, 7 dynamic boundary faces. | BiCGSTAB + BoomerAMG |
| **04** | `04_spe10_benchmark_3d` | 3D Orthogonal & Gmsh LGR | SPE 10 Model 2 benchmark (1200x2200x170 ft), 5 Peaceman wells, active BHP feedback callback with 2% hysteresis deadband, KPP scheme. | CG + BoomerAMG |
| **05** | `05_chen2010_coreflood` | 1D / 200 cells | Chen et al. (2010) Berea coreflood; shear-thinning foam rheology and dynamic surfactant front propagation. | UMFPACK + JFNK GMRES |
| **06** | `06_depaula2023_heterogeneous_sag` | 2D / 220 x 60 cells | de Paula et al. (2023) Layer 36 of SPE 10: Surfactant-Alternating-Gas (SAG) injection with external permeability/porosity arrays. | CG + BoomerAMG (Adaptive Paz Time Stepping) |
| **07** | `07_structured_3d_hole` | 3D Hexahedral Gmsh with well cavity | Curvilinear 3D grid around a central wellbore perforation, Kovscek foam displacement, compressible real-gas density. | BiCGSTAB + BoomerAMG |

---

## 🏃 Running the Tutorials

Navigate to any tutorial folder and execute the Python driver script:

```bash
cd examples/01_ashoori_coreflood_1d
python run_ashoori2011.py

# Generate publication-quality comparison plots:
python plot.py
```

For 2D and 3D simulation cases (such as `02`, `03`, `04`, and `07`), output directories contain standard VTU files (`volume_vars_*.vtu`) that can be opened directly in [**ParaView**](https://www.paraview.org/) or visualized off-screen using `FossilPlotter`.
