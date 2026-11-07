# Tutorial 2: 2D Unstructured Mesh with Hole & Multi-Material Petrophysics

This tutorial demonstrates compressible two-phase flow with Kovscek Local Equilibrium foam and dynamic surfactant transport ($C_s$) in a **2D unstructured hybrid Gmsh grid**, featuring an internal perforation wellbore cavity and multiple petrophysical rock zones.

---

## 🎯 Learning Objectives
- Import unstructured Gmsh `.msh` files directly into `pyfossil`.
- Map distinct petrophysical properties (permeability and porosity) across Gmsh physical region tags using `use_material_ids` and dictionary mappings (`permeability_x_map`, `porosity_map`).
- Configure dynamic boundary conditions on Gmsh boundary curves (`setup_dynamic_boundaries`), modeling fluid injection through the central cavity (`Hole`) and pressure outflow at lateral boundaries (`Left`, `Right`).
- Incorporate non-ideal real-gas PVT density tables.
- Solve the coupled system using `BiCGSTAB + BoomerAMG` for Darcy flow and `JFNK + KNP` for stiff multi-species transport.

---

## 📁 Included Files
- `run_unstructured_2d_materials.py`: Fully commented driver script.
- `reservatorio_com_furo_Materials.geo`: Gmsh CAD geometry script.
- `reservatorio_com_furo_Materials.msh`: Pre-generated 2D hybrid unstructured mesh.

---

## 🚀 How to Run

```bash
python run_unstructured_2d_materials.py
```

The output `.vtu` files will be saved to `./output_unstructured_2d/` and can be opened directly in [ParaView](https://www.paraview.org/) to observe the radial propagation of water saturation and surfactant fronts navigating through the heterogeneous materials.
