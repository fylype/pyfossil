# Tutorial 5: Chen et al. (2010) Coreflood Simulation

This tutorial replicates the laboratory coreflood experiment of **Chen et al. (2010)** for gas and surfactant coinjection in homogeneous Berea sandstone core.

---

## 🎯 Learning Objectives
- Model mechanistic foam generation using the Kovscek et al. model in Local Equilibrium (LE) mode.
- Couple reactive advective transport of surfactant concentration ($C_s$) dissolved in the aqueous phase.
- Apply cubic relative permeability curves ($n_w = 3.0, n_g = 3.0$) and Kovscek capillary pressure formulation.
- Solve the coupled system using the direct sparse solver UMFPACK for Darcy flow and implicit JFNK CVODE for transport.

---

## 🚀 How to Run

```bash
# Execute simulation:
python run_chen2010.py

# Generate comparison plots:
python plot.py
```
