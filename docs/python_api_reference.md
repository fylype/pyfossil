# Python API Reference (`pyfossil`)

This document provides a comprehensive reference for the classes, data structures, enumerations, and methods exposed by the `pyfossil` module.

---

## 🏗️ 1. Central Configuration Class: `SimulationData`

The `pyfossil.SimulationData` object is the unified repository defining all physical, geometric, fluid, rock, well, and numerical solver configurations.

```python
import pyfossil
sim = pyfossil.SimulationData()
```

### 1.1 Global Settings (`sim.global_settings`)
- **`dimension` (`int`):** Spatial dimension of the domain (`1`, `2`, or `3`).
- **`mesh_type` (`pyfossil.MeshType`):**
  - `MeshType.ORTHOGONAL_MESH`: Structured Cartesian / orthogonal grid.
  - `MeshType.UNSTRUCTURED_MESH`: Unstructured mesh imported from Gmsh (`.msh`).

---

### 1.2 Orthogonal Geometry (`sim.orthogonal_geometry`)
Used when `mesh_type = MeshType.ORTHOGONAL_MESH`.
- **`n_x`, `n_y`, `n_z` (`int`):** Number of cells in X, Y, and Z directions.
- **`x_init`, `x_final` (`float`):** Beginning and end coordinates along the X-axis [m].
- **`y_init`, `y_final` (`float`):** Beginning and end coordinates along the Y-axis [m].
- **`z_init`, `z_final` (`float`):** Beginning and end coordinates along the Z-axis [m].
- **`block_thickness` (`float`):** Extrusion thickness of the reservoir (useful for planar 2D models) [m].

---

### 1.3 Unstructured Mesh (`sim.unstructured_geometry`)
Used when `mesh_type = MeshType.UNSTRUCTURED_MESH`.
- **`mesh_filename` (`str`):** Absolute or relative path to the Gmsh mesh file (`.msh`, formats 2.2 or 4.1).

---

### 1.4 Fluid Properties (`sim.fluid_properties`)
- **`water_viscosity` (`float`):** Dynamic water viscosity $\mu_w$ [Pa·s].
- **`water_density` (`float`):** Water density $\rho_w$ [kg/m³].
- **`gas_viscosity` (`float`):** Dynamic gas viscosity $\mu_g$ [Pa·s].
- **`gas_density` (`float`):** Reference gas density $\rho_g$ [kg/m³].
- **`gas_compressibility` (`bool`):** Enables compressible gas regime.
- **`gas_state_equation` (`pyfossil.GasStateEquationModel`):**
  - `GasStateEquationModel.IDEAL_GAS`: Ideal gas law.
  - `GasStateEquationModel.DENSITY_TABLE`: Discrete tabular PVT relationship of Pressure vs. Density.
- **`table_density_model.density_table` (`dict[float, float]`):** Dictionary mapping `{Pressure [Pa]: Density [kg/m³]}`.
- **`gravity` (`bool`):** Enables gravitational acceleration and buoyancy terms.
- **`gravity_direction` (`list[float]`):** Gravitational acceleration vector $[g_x, g_y, g_z]$ [m/s²].

---

### 1.5 Rock Petrophysics (`sim.rock_properties`)
- **`perm_x`, `perm_y`, `perm_z` (`float`):** Absolute permeabilities in X, Y, and Z [m²]. *(Note: $1\text{ mD} \approx 9.86923\times 10^{-16}\text{ m}^2$)*.
- **`porosity` (`float`):** Porosity of the porous medium $\phi \in (0, 1)$.
- **`perm_filename` (`str`):** External data point cloud file for permeability (e.g., SPE 10 Model 2).
- **`por_filename` (`str`):** External data point cloud file for porosity.
- **`use_material_ids` (`bool`):** Enables petrophysical mapping across Gmsh physical region tags.
  - `permeability_x_map` (`dict[int, float]`): Material mapping `{Material_ID: Perm_X}`.
  - `porosity_map` (`dict[int, float]`): Material mapping `{Material_ID: Porosity}`.
- **`use_synthetic_field` (`bool`):** Generates a spatially correlated log-normal synthetic field using the built-in stochastic generator.
  - `synthetic_rock_field.seed`: Integer pseudo-random seed.
  - `synthetic_rock_field.permeability_avg`: Mean permeability [m²].
  - `synthetic_rock_field.porosity_avg`: Mean porosity.
  - `synthetic_rock_field.heterogeneity`: Log-normal variance parameter.
- **`upscaling`:** Directional petrophysical upscaling manager:
  - `method_x`, `method_y`, `method_z` (`pyfossil.UpscalingMethod`): `ARITHMETIC`, `HARMONIC`, `GEOMETRIC`, `POWER_LAW`.
  - `power_law_exponent_x`, `power_law_exponent_y`: Power-law averaging exponent (e.g., 0.33).

---

### 1.6 Rock-Fluid Interactions (`sim.rock_fluid_interactions`)
- **`swc` (`float`):** Connate / irreducible water saturation $S_{wc}$.
- **`sgr` (`float`):** Residual gas saturation $S_{gr}$.
- **`sigma_wg` (`float`):** Water-gas interfacial tension $\sigma_{wg}$ [N/m].
- **`rel_perm_model` (`pyfossil.RelativePermeabilityModel`):**
  - `COREY_BROOKS_KR`: Standard Corey-Brooks model.
  - `KOVSCEK_KR`: Cubic Kovscek curves.
  - `ASHOORI_KR`: Quadratic Ashoori curves.
  - `CUSTOM_KR`: Custom saturation exponents $N_w$ and $N_g$ (`custom_rel_perm.nw`, `ng`).
- **`cap_pressure_model` (`pyfossil.CapillaryPressureModel`):**
  - `NONE`: Neglect capillary pressure.
  - `LEVERETT_J`: Leverett J-function scaled by local permeability and porosity.
  - `KOVSCEK_CP`, `ASHOORI_CP`: Foam-specific capillary formulations.

---

### 1.7 EOR Mechanisms & Foam Models (`sim.eor_mechanisms`)
- **`foam_model` (`pyfossil.FoamModel`):** `NONE`, `KOVSCEK`, `ASHOORI`.
- **Ashoori Model Parameters (`sim.eor_mechanisms.ashoori_model`):**
  - `A`: Lamella division bubble generation parameter.
  - `sw_critical`: Critical water saturation for capillary transition.
  - `max_mob_red`: Maximum gas mobility reduction factor ($MRF$).
  - `K_c`: Lamella destruction rate constant [s⁻¹].
- **Kovscek Model Parameters (`sim.eor_mechanisms.kovscek_model`):**
  - `k01`: Lamella generation rate coefficient.
  - `k0m1`: Lamella coalescence rate coefficient.
  - `refSurf`: Reference critical surfactant concentration [wt%].
  - `alpha`: Bretherton shear-thinning exponent.
  - `pcStarMax`: Limiting capillary pressure for lamella rupture [Pa].

---

### 1.8 Peaceman Well System (`sim.wells`)
Dictionary of wells indexed by identifier string (`sim.wells["WellName"]`):
- **`well_type` (`pyfossil.WellType`):** `INJECTOR` or `PRODUCER`.
- **`well_control` (`pyfossil.WellControl`):**
  - `WellControl.FLOW_RATE`: Target volumetric flow rate [m³/s].
  - `WellControl.BHP`: Bottom-Hole Pressure constraint [Pa].
- **`well_value` (`float` or `dict`):** Operational constraint value (supports piecewise schedules `{time: value}`).
- **`well_radius` (`float`):** Wellbore radius $r_w$ [m].
- **`skin_factor` (`float`):** Dimensionless well skin factor.
- **`include_hydrostatic_head` (`bool`):** Accounts for hydrostatic fluid head variation along well perforations.
- **`trajectory_coords` (`list[float]`):** 3D well trajectory coordinates `[x1, y1, z1, x2, y2, z2]` from heel to toe.

---

### 1.9 Initial and Boundary Conditions (`sim.initial_and_boundary_conditions`)
- **`initial_state`:**
  - `pressure_init.constant_value`: Initial reservoir pressure [Pa].
  - `initialization[pyfossil.Variable.SW].constant_value`: Initial water saturation $S_w \in [0, 1]$.
  - `initialization[pyfossil.Variable.CS].constant_value`: Initial surfactant concentration $C_s$ [wt%].
- **Cartesian Mesh Boundaries:** Predefined faces `"Left"`, `"Right"`, `"Top"`, `"Bottom"`, `"Front"`, `"Back"`.
- **Unstructured Mesh Boundaries:** Defined dynamically via `setup_dynamic_boundaries(["Name1", "Name2", ...])`.
- **Boundary Properties:**
  - `darcy_boundary_type`: `DIRICHLET` (prescribed pressure) or `NEUMANN` (prescribed Darcy flux [m/s]).
  - `darcy_boundary_value`: Scalar value or time schedule `{t0: v0, t1: v1}`.
  - `trans_boundary_type`: `DIRICHLET`, `INFLOW_DIRICHLET`, `INFLOW_NEUMANN_FW`, `OUTFLOW`, `NO_FLOW`.
  - `trans_boundary_values[pyfossil.Variable.*]`: Prescribed injected volume fraction or concentration.

---

### 1.10 Numerical Solvers & Execution Control (`sim.execution_control`)
- **`variables` (`set[pyfossil.Variable]`):** Set of active conservation equations:
  - `Variable.SW`: Water saturation.
  - `Variable.ND`: Foam bubble texture density.
  - `Variable.CS`: Surfactant concentration.
- **`darcy_linear_solver` (`pyfossil.DarcyLinearSolver`):**
  - `CG`: Conjugate Gradient (ideal for symmetric positive-definite condensed systems).
  - `MINRES`: Minimal Residual (optimal for pure-Neumann problems with nullspace closure).
  - `GMRES`, `BiCGSTAB`: General Krylov solvers for nonsymmetric matrices.
  - `UMFPACK`: Direct sparse LU factorization (exact and robust for 1D/2D).
- **`darcy_preconditioner` (`pyfossil.DarcyPreconditioner`):**
  - `BOOMER_AMG`: HYPRE BoomerAMG algebraic multigrid (peak performance on large 3D meshes).
  - `GAMG`: PETSc native Geometric-Algebraic Multigrid.
  - `ICC`: Incomplete Cholesky Factorization.
  - `PARASAILS`: Parallel Sparse Approximate Inverse.
  - `NONE`: Unpreconditioned iterative solver.
- **`transport_linear_solver` (`pyfossil.TransportLinearSolver`):**
  - `GMRES`, `BICGSTAB`, `TFQMR`: Native SUNDIALS Krylov solvers tightly coupled to JFNK.
  - `GMRES_PETSC`, `BCGSL_PETSC`, `BICGSTAB_PETSC`: PETSc KSP solvers coupled to JFNK.
- **`transport_preconditioner` (`pyfossil.TransportPreconditioner`):**
  - `BLOCK_ILU`: Block-Jacobi incomplete LU per cell (default, excellent efficiency).
  - `GLOBAL_ILU`: Global coupled ILU across the full mesh.
  - `BOOMER_AMG`: Algebraic multigrid for transport systems.
  - `NONE`: Pure matrix-free JFNK without preconditioning.
- **`darcy_time_step_strategy` (`pyfossil.DarcyTimeStepStrategy`):**
  - `NONE`: Fixed constant Darcy macro time step.
  - `SW_VARIATION`: Adaptive time stepping governed by maximum saturation variation $\Delta S_w$.
  - `PAZ_VELOCITY`: Adaptive time stepping based on velocity $L_2$ norm variation (Paz et al., 2021).
- **`num_method` (`pyfossil.NumericalMethod`):**
  - `KNP`: Central-Upwind scheme of Kurganov, Noelle & Petrova (2001).
  - `KPP`: Central-Upwind scheme of Kurganov, Petrova & Popova (2007) for non-convex fractional flows.
- **`abstol`, `reltol` (`float`):** Absolute and relative tolerances for CVODE integration.
- **`num_threads` (`int`):** Number of OpenMP parallel execution threads.

---

## 🎮 2. Executive Engine: `FossilSimulator`

Manages grid assembly, physical field mapping, the coupled Darcy-transport time-stepping loop, and output generation.

### 2.1 Constructor and Core Methods
```python
simulator = pyfossil.FossilSimulator(sim_data, output_dir="./output")
```
- **`run()`:** Executes the complete simulation from initial state to `final_time`.
- **`set_step_callback(callback_fn)`:** Registers a Python callback invoked after each macro time step.
  - Callback signature: `callback(t_physical: float, sim, sim_data) -> bool`
  - Returning `True` continues simulation; returning `False` triggers graceful early termination.
- **`get_current_well_bhp(well_name: str) -> float`:** Returns the current Bottom-Hole Pressure of the specified well in Pascals.
- **`get_current_well_rate(well_name: str) -> float`:** Returns the current volumetric flow rate of the specified well in m³/s.
- **`set_well_bhp(well_name: str, bhp_pa: float)`:** Dynamically modifies the target BHP of a well during execution.
- **`set_well_rate(well_name: str, rate_m3_s: float)`:** Dynamically modifies the target flow rate of a well during execution.
