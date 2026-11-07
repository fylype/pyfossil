# Tutorial 6: de Paula et al. (2023) SAG vs Co-injection in SPE 10 Layer 36

This tutorial replicates the research scenarios from **de Paula et al. (2023)** comparing Surfactant-Alternating-Gas (**SAG**) injection against **continuous coinjection** in the highly heterogeneous cross-section of SPE 10 Layer 36.

---

## 🎯 Learning Objectives
- Simulate a 2D vertical cross-section (220 x 60 cells) with permeability spanning multiple orders of magnitude.
- Define time-dependent piecewise boundary conditions using Python dictionaries (`{0.0: 1.0, 4000.0: 0.0}`) via the native `ConstantOrMap` framework.
- Employ the adaptive Darcy time-stepping algorithm based on velocity $L_2$ error (Paz et al., 2021).
- Observe foam-assisted mobility control: high-permeability thief zones are blocked by in-situ foam generation, diverting injected fluid into low-permeability unswept zones.

---

## 📁 Included Files
- `run_depaula2023_sag.py`: Fully commented driver script.
- `spe10_layer_36_rot90_perm.dat`: Heterogeneous permeability field of Layer 36 (220 x 60).
- `spe10_layer_36_rot90_por.dat`: Heterogeneous porosity field.

---

## 🚀 How to Run

```bash
python run_depaula2023_sag.py
```
