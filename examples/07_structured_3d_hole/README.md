# Tutorial 7: 3D Structured Hexahedral Mesh with Well Perforation

This tutorial demonstrates fully 3D multiphase flow and foam displacement on a **curvilinear hexahedral mesh generated in Gmsh**, combining geometric regularity with conformal boundary discretization around an internal wellbore cavity.

---

## 🎯 Learning Objectives
- Simulate multiphase flow and mechanistic foam displacement on curvilinear non-orthogonal hexahedral grids.
- Evaluate convergence rates of `BiCGSTAB + BoomerAMG` solvers on regular structured-like topologies.
- Inspect the 3D spatial field distribution of pressure and saturation away from the well perforation.

---

## 📁 Included Files
- `run_structured_3d_hole.py`: Fully commented driver script.
- `reservatorio_com_furo.geo`: Gmsh CAD script generating multi-block structured hexahedra.
- `reservatorio_com_furo.msh`: Pre-generated 3D hexahedral mesh.

---

## 🚀 How to Run

```bash
python run_structured_3d_hole.py
```
