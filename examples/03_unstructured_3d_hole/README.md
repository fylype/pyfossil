# Tutorial 3: 3D Unstructured Mesh with Central Well Perforation

This tutorial demonstrates fully 3D multiphase flow and foam displacement in a **3D tetrahedral unstructured Gmsh grid**, containing an internal vertical wellbore cavity and a synthetic spatially correlated heterogeneous rock field.

---

## 🎯 Learning Objectives
- Import high-resolution 3D tetrahedral Gmsh `.msh` grids.
- Generate synthetic heterogeneous petrophysical fields using the built-in stochastic log-normal algorithm (`use_synthetic_field`).
- Configure 7 dynamic boundary surface conditions (`setup_dynamic_boundaries`), injecting fluid through the central cavity (`Hole`) and draining through opposing lateral faces.
- Employ parallel iterative solvers (`BiCGSTAB + BoomerAMG`) and `JFNK + KNP` accelerated by OpenMP multi-threading.

---

## 📁 Included Files
- `run_unstructured_3d_hole.py`: Fully commented 3D driver script.
- `reservatorio_com_furo.geo`: Gmsh 3D CAD script.
- `reservatorio_com_furo.msh`: Pre-generated 3D tetrahedral mesh.

---

## 🚀 How to Run

```bash
python run_unstructured_3d_hole.py
```

3D simulation snapshots are written in standard VTU format to `./output_unstructured_3d/`. Open them in [ParaView](https://www.paraview.org/) and apply *Clip* or *Threshold* filters to inspect the 3D radial propagation of the foam front away from the injection cavity.
