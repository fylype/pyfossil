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
- **`water_viscosity` (`float`):** Dynamic water viscosity $\mu_w$ [Pa·s] (alias for `mu_w`).
- **`water_density` (`float`):** Water density $\rho_w$ [kg/m³] (alias for `rho_w`).
- **`gas_viscosity` (`float`):** Dynamic gas viscosity $\mu_g$ [Pa·s] (alias for `mu_g`).
- **`gas_density` (`float`):** Reference gas density $\rho_g$ [kg/m³] (alias for `rho_g`).
- **`gas_compressibility` (`bool`):** Enables compressible gas regime (alias for `gas_comp_prop.compressibility`).
- **`gas_state_equation` (`pyfossil.GasStateEquationModel`):**
  - `GasStateEquationModel.IDEAL_GAS`: Ideal gas law.
  - `GasStateEquationModel.EXPONENTIAL`: Exponential compressibility equation of state.
  - `GasStateEquationModel.LINEAR`: Linear compressibility equation of state.
  - `GasStateEquationModel.DENSITY_TABLE` (or `TABLE`): Discrete tabular PVT relationship of Pressure vs. Density.
- **`table_density_model.density_table` (`dict[float, float]`):** Dictionary mapping `{Pressure [Pa]: Density [kg/m³]}` with automatic spline interpolation.
- **`gravity` (`bool`):** Enables gravitational acceleration and buoyancy terms (alias for `grav_acl.using_gravity`).
- **`gravity_direction` (`list[float]`):** Gravitational acceleration vector $[g_x, g_y, g_z]$ [m/s²].

---

### 1.5 Rock Petrophysics (`sim.rock_properties`)
- **`perm_x`, `perm_y`, `perm_z` (`float`):** Absolute permeabilities in X, Y, and Z [m²] (aliases for `permeability_x`, `permeability_y`, `permeability_z`). *(Note: $1\text{ mD} \approx 9.86923\times 10^{-16}\text{ m}^2$)*.
- **`porosity` (`float`):** Porosity of the porous medium $\phi \in (0, 1)$ (alias `por`).
- **`permeability_filename` (`str`):** External data point cloud file for permeability (alias `perm_filename`).
- **`porosity_filename` (`str`):** External data point cloud file for porosity (alias `por_filename`).
- **`use_material_ids` (`bool`):** Enables petrophysical mapping across Gmsh physical region tags.
  - `permeability_x_map` (`dict[int, float]`): Material mapping `{Material_ID: Perm_X}`.
  - `porosity_map` (`dict[int, float]`): Material mapping `{Material_ID: Porosity}`.
- **`use_synthetic_field` (`bool`):** Generates a spatially correlated log-normal synthetic field using the built-in stochastic generator.
  - `synthetic_rock_field.seed`: Integer pseudo-random seed.
  - `synthetic_rock_field.permeability_avg`: Mean permeability [m²].
  - `synthetic_rock_field.porosity_avg`: Mean porosity.
  - `synthetic_rock_field.heterogeneity`: Log-normal variance parameter.
- **Petrophysical Upscaling (`sim.petrophysical_upscaling`):** Directional cell-by-cell upscaling engine:
  - `active` (`bool`): Enables petrophysical upscaling.
  - `method_x`, `method_y`, `method_z` (`pyfossil.UpscalingMethod`): `ARITHMETIC`, `HARMONIC`, `GEOMETRIC`, `POWER_LAW`.
  - `por_method` (`pyfossil.UpscalingMethod`): Pore-volume conserving porosity upscaling.
  - `power_law_p` (`float`): Exponent used when `method = POWER_LAW`.

---

### 1.6 Rock-Fluid Interactions (`sim.rock_fluid_interactions`)
- **`connate_water_saturation` (`float`):** Connate / irreducible water saturation $S_{wc}$ (aliases: `swc`, `residual_water_saturation`, `critical_water_saturation`).
- **`residual_gas_saturation` (`float`):** Residual gas saturation $S_{gr}$ (aliases: `sgr`, `critical_gas_saturation`).
- **`interfacial_tension` (`float`):** Water-gas interfacial tension $\sigma_{wg}$ [N/m] (aliases: `sigma_wg`, `surface_tension`).
- **`relative_permeability_model` (`pyfossil.RelativePermeabilityModel`):** (alias `rel_perm_model`)
  - `COREY_BROOKS` (`COREY_BROOKS_KR`): Standard Corey-Brooks model.
  - `CUSTOM` (`CUSTOM_KR`): Custom saturation exponents $N_w$ and $N_g$ (`custom_rel_perm.nw`, `ng`).
  - `ASHOORI` (`ASHOORI_KR`): Ashoori quadratic relative permeability.
  - `TABLE`: Tabular relative permeability.
  - `NONE`: Linear relative permeability.
- **`capillary_pressure_model` (`pyfossil.CapillaryPressureModel`):** (alias `cap_pressure_model`)
  - `NONE` (`NONE_CP`): Neglect capillary pressure.
  - `LEVERETT_J`: Leverett J-function scaled by local permeability and porosity.
  - `ASHOORI` (`ASHOORI_CP`): Ashoori capillary model.
  - `TABLE`: Tabular capillary pressure curve.

---

### 1.7 EOR Mechanisms & Foam Models (`sim.eor_mechanisms` or `sim.foam`)
The foam physics subsection can be accessed either as `sim.eor_mechanisms`, `sim.foam`, or `sim.physical_models`:
- **`model` (`pyfossil.FoamModel`):** (alias `foam_model`)
  - `FoamModel.NONE`: Two-phase displacement without foam.
  - `FoamModel.KOVSCEK`: Mechanistic bubble population balance (snap-off & capillary suction coalescence).
  - `FoamModel.ASHOORI`: Kinetic limiting capillary pressure foam model.
  - `FoamModel.STARS`: Empirical mobility reduction model (CMG STARS standard).
  - `FoamModel.ZITHA`: Dynamic foam quality and pore-throat bubble generation model.
  - `FoamModel.LAMAP`: Look-up apparent mobility approach.
- **`max_foam_texture` (`float`):** Limiting bubble density $n_{\max}$ [1/m³] (aliases: `n_max`, `max_texture`, `max_bubble_density`).

#### Sub-Model Shortcuts:
- **Ashoori Model (`sim.foam.ashoori` or `sim.eor_mechanisms.ashoori_model`):**
  - `generation_parameter` (alias `A`): Lamella division bubble generation parameter.
  - `critical_water_saturation` (alias `sw_critical`): Critical water saturation for capillary transition.
  - `max_mobility_reduction` (aliases `maximum_mobility_reduction`, `max_mob_red`, `max_mrf`): Maximum gas mobility reduction factor ($MRF$).
  - `destruction_time_constant` (aliases `coalescence_rate`, `time_constant`, `K_c`): Lamella destruction rate constant [s⁻¹].
- **Kovscek Model (`sim.foam.kovscek` or `sim.eor_mechanisms.kovscek_model`):**
  - `generation_rate` (aliases `bubble_generation_coeff`, `k01`): Lamella generation rate coefficient.
  - `coalescence_rate` (aliases `bubble_coalescence_coeff`, `destruction_rate`, `k0m1`): Lamella coalescence rate coefficient.
  - `limiting_capillary_pressure` (aliases `critical_capillary_pressure`, `max_capillary_pressure`, `pcStarMax`): Limiting capillary pressure for lamella rupture [Pa].
  - `reference_surfactant` (aliases `reference_surfactant_concentration`, `critical_surfactant_concentration`, `refSurf`): Reference critical surfactant threshold [wt%].
  - `max_trapped_fraction` (aliases `maximum_trapped_fraction`, `trapping_coefficient`, `XtMax`): Trapped foam bubble fraction.
  - `water_endpoint_rel_perm` / `gas_endpoint_rel_perm` (`krw0`, `krg0`): Relative permeability endpoints.
  - `water_rel_perm_exponent` / `gas_rel_perm_exponent` (`nw`, `ng`): Relative permeability exponents.
  - `hirasaki_velocity_exponent` (alias `alpha`): Apparent shear-thinning exponent.
  - `constant_trapping` (alias `const_trapping`): Assumes constant trapped bubble fraction.
- **STARS Model (`sim.foam.stars` or `sim.eor_mechanisms.stars_model`):**
  - `max_mobility_reduction` (alias `fmmob`): Reference mobility reduction multiplier.
  - `critical_water_saturation` (aliases `dry_out_saturation`, `fmsw`): Wetting phase collapse saturation.
  - `transition_sharpness` (alias `sfbet`): Transition steepness parameter $\beta$.
  - `reference_surfactant` (alias `fmsurf`): Critical surfactant threshold [wt%].
  - `surfactant_exponent` (alias `esurf`): Surfactant exponent.
  - `reference_capillary_number` (alias `fmcap`): Critical capillary number.
  - `capillary_number_exponent` (alias `ecap`): Capillary number exponent.
  - `shear_thinning_exponent` (alias `epcap`): Shear-thinning velocity exponent.
- **Zitha Model (`sim.foam.zitha` or `sim.eor_mechanisms.zitha_model`):**
  - `generation_rate` (`C_g`), `destruction_rate` (`C_c`).
  - `max_water_rel_perm` (`krw0`), `max_foamed_gas_rel_perm` (`krgf0`).
  - `effective_pore_radius` (`r_eff`), `contact_angle` (`theta`).
- **LAMAP Model (`sim.foam.lamap` or `sim.eor_mechanisms.lamap_model`):**
  - `apparent_viscosity_table` (alias `visc_foam_table`): Mapping $\{f_g: \mu_{\text{app}}\}$.

---

### 1.8 Peaceman Well Management (`sim.wells`)
Wells can be accessed, created, and iterated directly through the `sim.wells` dictionary proxy:
```python
# Auto-creates and registers "INJ1" if not present:
inj = sim.wells["INJ1"]
inj.well_type = pf.WellType.INJECTOR
inj.well_control = pf.WellControl.FLOW_RATE   # or pf.WellConstraintType.FLOW_RATE
inj.well_value = 1.0e-3                       # direct float or schedule dict
inj.well_radius = 0.1                         # wellbore radius [m]
inj.skin = 0.0                                # skin factor
inj.wfrac = 1.0                               # well angular fraction (0.25 for quarter-well)
inj.trajectory_coords = [0.0, 0.0, 0.0, 0.0, 0.0, 10.0]
inj.injected_fluid = {pf.Variable.SW: 1.0}

# Producers:
prod = sim.wells["PROD1"]
prod.well_type = pf.WellType.PRODUCER
prod.well_control = pf.WellControl.BHP
prod.well_value = 2.0e7                       # 200 bar BHP

# Iteration and introspection:
print(f"Total active wells: {len(sim.wells)}")
for well in sim.wells:
    print(f"Well {well.name}: type={well.well_type}")
if "INJ1" in sim.wells:
    print("INJ1 is configured!")
```

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
