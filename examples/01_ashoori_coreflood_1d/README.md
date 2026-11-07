# Tutorial 1: Ashoori 2011 Coreflood Foam Simulation

This tutorial replicates the laboratory coreflood experiment of **Ashoori et al. (2011)** for transient multiphase displacement and foam generation in a 1D homogeneous porous medium.

---

## 🎯 Learning Objectives
- Configure a 1D laboratory core domain with high spatial discretization (200 cells).
- Parameterize the Ashoori foam population balance model accounting for mechanical lamella generation, critical capillary coalescence, and maximum gas mobility reduction ($MRF$).
- Solve the coupled system using the direct sparse solver (`UMFPACK`) for Darcy flow and implicit JFNK (`GMRES + Block-ILU`) for stiff transport of water saturation ($S_w$) and foam texture ($n_D$).
- Extract and visualize spatial saturation and bubble texture profiles using `plot.py`.

---

## 🚀 How to Run

1. **Execute the Simulation:**
   ```bash
   python run_ashoori2011.py
   ```
   The output directory `./output_Ashoori2011/` will be generated containing `.vtu` spatial field snapshots and log files.

2. **Generate Publication-Quality Plots:**
   ```bash
   python plot.py
   ```
   This generates:
   - `ashoori_sw_1d.pdf`: Spatial water saturation profiles at multiple time steps.
   - `ashoori_nd_1d.pdf`: Foam bubble texture density evolution along the core length.
