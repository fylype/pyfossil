#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
TUTORIAL 4: SPE 10 Model 2 Benchmark on 3D Orthogonal Grid with Peaceman Wells
================================================================================

Implements the standard industry benchmark SPE 10 Dataset 2 (Christie & Blunt,
2001), modeling waterflooding in a highly heterogeneous channelized 3D reservoir.

Physical and Numerical Highlights:
----------------------------------
1. SPE 10 Field Geometry (1200 ft x 2200 ft x 170 ft):
   Exact conversion to SI units and 3D orthogonal structured discretization.
2. Peaceman Well System (5 vertical wells):
   - 1 Central Injector (INJ1): Water injection under target rate of 5,000 STB/D
     with maximum Bottom-Hole Pressure limit (BHP max = 10,000 psi).
   - 4 Corner Producers (P1 through P4): Fluid production under constant
     bottom-hole pressure (BHP = 4,000 psi).
   - Accounts for hydrostatic head variation along well perforations.
3. Active Dynamic Well Controller with 2% Hysteresis:
   In-situ Python step callback (`set_step_callback`) inspecting physical states.
   The 2% hysteresis deadband eliminates chattering oscillations between
   rate and BHP constraints.
4. Directional Petrophysical Upscaling:
   KD-Tree based Power-Law averaging (exponent 0.33) along X and Y, and
   Harmonic averaging along Z.
5. KPP Central-Upwind Flux Reconstruction:
   Kurganov-Petrova-Popova scheme for non-convex fractional flow functions.
6. Large-Scale Linear Solvers:
   Conjugate Gradient (CG) preconditioned by HYPRE BoomerAMG for Darcy,
   and JFNK with GMRES and Block-ILU for implicit transport.

Authors: Filipe F. de Paula, Thiago Quinelato, Iury Igreja (UFLA)
================================================================================
"""

import os
import sys

# Attempt importing installed pyfossil; fallback to local build directory
try:
    import pyfossil
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_build = os.path.abspath(os.path.join(script_dir, "../../../build"))
    if local_build not in sys.path:
        sys.path.append(local_build)
    import pyfossil


# =============================================================================
# UNIT CONVERSION CONSTANTS (FIELD UNITS -> SI)
# =============================================================================
DAYS_TO_SEC = 86400.0                       # 1 day = 86400 s
FT_TO_M = 0.3048                            # 1 ft = 0.3048 m
PSI_TO_PA = 6894.757                        # 1 psi = 6894.757 Pa
CP_TO_PA_S = 0.001                          # 1 cP = 1.0e-3 Pa.s
BBL_DAY_TO_M3_S = 1.84013e-6                # 1 bbl/day = 1.84013e-6 m^3/s
MD_TO_M2 = 9.86923e-16                      # 1 mD = 9.86923e-16 m^2


# =============================================================================
# SPE 10 BENCHMARK OPERATIONAL SPECIFICATIONS
# =============================================================================
MAX_INJ_BHP = 10000.0 * PSI_TO_PA           # Upper BHP limit: 10,000 psi (~68.95 MPa)
TARGET_INJ_RATE = 5000.0 * BBL_DAY_TO_M3_S  # Target injection rate: 5,000 bbl/day (~9.20e-3 m^3/s)
PROD_BHP = 4000.0 * PSI_TO_PA               # Constant producer BHP: 4,000 psi (~27.58 MPa)

# Well controller global state
well_controller_state = {
    "mode": "FLOW_RATE",
    "switch_count": 0
}


def well_control_callback(t_physical: float, sim, sim_data) -> bool:
    """
    Callback invoked after each physical macro time step.
    Monitors Bottom-Hole Pressure (BHP) of INJ1 and dynamically switches
    between target flow rate (5,000 bbl/day) and maximum BHP (10,000 psi),
    adhering strictly to the SPE 10 benchmark specification.

    Includes a 2% hysteresis deadband to prevent chattering.
    """
    t_days = t_physical / DAYS_TO_SEC
    inj_bhp = sim.get_current_well_bhp("INJ1")
    current_mode = well_controller_state["mode"]

    if current_mode == "FLOW_RATE":
        # If injection pressure reaches or exceeds 10,000 psi:
        if inj_bhp >= MAX_INJ_BHP:
            well_controller_state["mode"] = "BHP"
            sim_data.wells["INJ1"].well_control = pyfossil.WellControl.BHP
            sim_data.wells["INJ1"].well_value = MAX_INJ_BHP
            well_controller_state["switch_count"] += 1
            print(f"\n[WELL CONTROL @ {t_days:.3f} days] INJ1 reached pressure limit ({inj_bhp/PSI_TO_PA:.1f} psi >= 10000 psi).")
            print(f" -> Switching constraint: FLOW_RATE (5000 bbl/d) -> Fixed BHP (10,000 psi).")

    elif current_mode == "BHP":
        # Reverse switch with 2% hysteresis deadband:
        # Revert to FLOW_RATE only if injection capacity >= 5,100 bbl/day (1.02 * target)
        inj_rate = sim.get_current_well_rate("INJ1")
        inj_rate_bblday = inj_rate / BBL_DAY_TO_M3_S

        if inj_rate >= TARGET_INJ_RATE * 1.02:
            well_controller_state["mode"] = "FLOW_RATE"
            sim_data.wells["INJ1"].well_control = pyfossil.WellControl.FLOW_RATE
            sim_data.wells["INJ1"].well_value = TARGET_INJ_RATE
            well_controller_state["switch_count"] += 1
            print(f"\n[WELL CONTROL @ {t_days:.3f} days] INJ1 recovered injection capacity ({inj_rate_bblday:.1f} bbl/d >= {TARGET_INJ_RATE*1.02/BBL_DAY_TO_M3_S:.1f} bbl/d with hysteresis).")
            print(f" -> Switching constraint: BHP (10000 psi) -> Fixed FLOW_RATE (5,000 bbl/day).")

    return True  # Return True to continue simulation


def build_spe_model() -> pyfossil.SimulationData:
    """
    Constructs and parameterizes the complete SPE 10 Model 2 setup.
    """
    sim = pyfossil.SimulationData()

    # =========================================================================
    # 1. RESERVOIR GEOMETRY (SPE 10 Dimensions)
    # =========================================================================
    # Original field dimensions: 1200 ft x 2200 ft x 170 ft (Lx, Ly, Lz)
    sim.global_settings.mesh_type = pyfossil.MeshType.ORTHOGONAL_MESH
    sim.global_settings.dimension = 3

    # Mesh discretization:
    sim.orthogonal_geometry.n_x = 12
    sim.orthogonal_geometry.n_y = 44
    sim.orthogonal_geometry.n_z = 17

    sim.orthogonal_geometry.x_init = 0.0
    sim.orthogonal_geometry.x_final = 1200.0 * FT_TO_M
    sim.orthogonal_geometry.y_init = 0.0
    sim.orthogonal_geometry.y_final = 2200.0 * FT_TO_M
    sim.orthogonal_geometry.z_init = 0.0
    sim.orthogonal_geometry.z_final = 170.0 * FT_TO_M

    # =========================================================================
    # 2. FLUID THERMODYNAMICS AND PROPERTIES
    # =========================================================================
    sim.fluid_properties.water_viscosity = 0.3 * CP_TO_PA_S   # Water viscosity = 0.3 cP
    sim.fluid_properties.water_density = 64.0 * 16.0185       # Water density = 1025.2 kg/m^3 (64 lb/ft^3)
    sim.fluid_properties.gas_viscosity = 3.0 * CP_TO_PA_S     # Oil viscosity = 3.0 cP (non-wetting phase)

    # Real compressibility with PVT density table
    sim.fluid_properties.gas_compressibility = True
    sim.fluid_properties.gas_state_equation = pyfossil.GasStateEquationModel.DENSITY_TABLE
    sim.fluid_properties.table_density_model.density_table = {
        300.0 * PSI_TO_PA: 50.70 * 16.0185,
        800.0 * PSI_TO_PA: 51.58 * 16.0185,
        8000.0 * PSI_TO_PA: 52.48 * 16.0185
    }

    # Gravity activated along vertical Z direction (gz = 9.81 m/s^2)
    sim.fluid_properties.gravity = True
    sim.fluid_properties.gravity_direction = [0.0, 0.0, 9.81]

    # =========================================================================
    # 3. ROCK-FLUID INTERACTIONS (QUADRATIC RELPERMS)
    # =========================================================================
    # SPE 10 defines quadratic relative permeability curves without capillary pressure:
    #   krw = ((Sw - Swc)/(1 - Swc - Sgr))^2
    #   kro = ((1 - Sw - Sgr)/(1 - Swc - Sgr))^2
    sim.rock_fluid_interactions.swc = 0.20
    sim.rock_fluid_interactions.sgr = 0.20
    sim.rock_fluid_interactions.rel_perm_model = pyfossil.RelativePermeabilityModel.CUSTOM_KR
    sim.rock_fluid_interactions.custom_rel_perm.nw = 2.0
    sim.rock_fluid_interactions.custom_rel_perm.ng = 2.0
    sim.rock_fluid_interactions.cap_pressure_model = pyfossil.CapillaryPressureModel.NONE

    # =========================================================================
    # 4. INITIAL RESERVOIR STATE
    # =========================================================================
    # Initial pressure of 6000 psi at the top of the reservoir
    sim.initial_and_boundary_conditions.initial_state.pressure_init.constant_value = 6000.0 * PSI_TO_PA
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.SW].constant_value = 0.20

    # =========================================================================
    # 5. PEACEMAN WELL SYSTEM (5 COMPLETE VERTICAL WELLS)
    # =========================================================================
    z_top = 0.0
    z_bottom = 170.0 * FT_TO_M

    # Central Injector (INJ1): Located at (x = 600 ft, y = 1100 ft)
    w_inj = sim.wells["INJ1"]
    w_inj.well_type = pyfossil.WellType.INJECTOR
    w_inj.well_control = pyfossil.WellControl.FLOW_RATE
    w_inj.well_value = TARGET_INJ_RATE
    w_inj.well_radius = 0.10  # Wellbore radius = 10 cm
    w_inj.skin_factor = 0.0
    w_inj.include_hydrostatic_head = True
    w_inj.trajectory_coords = [600.0 * FT_TO_M, 1100.0 * FT_TO_M, z_top,
                               600.0 * FT_TO_M, 1100.0 * FT_TO_M, z_bottom]

    # Four Corner Producers (P1 through P4):
    producers_specs = {
        "P1": (0.0, 0.0),
        "P2": (1200.0, 0.0),
        "P3": (1200.0, 2200.0),
        "P4": (0.0, 2200.0)
    }

    eps_m = 0.1  # Small offset to avoid exterior face singularity
    for p_name, (x_ft, y_ft) in producers_specs.items():
        w_prod = sim.wells[p_name]
        w_prod.well_type = pyfossil.WellType.PRODUCER
        w_prod.well_control = pyfossil.WellControl.BHP
        w_prod.well_value = PROD_BHP
        w_prod.well_radius = 0.10
        w_prod.skin_factor = 0.0
        w_prod.include_hydrostatic_head = True

        x_m = x_ft * FT_TO_M
        y_m = y_ft * FT_TO_M
        if x_m <= 0.0: x_m += eps_m
        elif x_m >= 1200.0 * FT_TO_M: x_m -= eps_m
        if y_m <= 0.0: y_m += eps_m
        elif y_m >= 2200.0 * FT_TO_M: y_m -= eps_m

        w_prod.trajectory_coords = [x_m, y_m, z_top, x_m, y_m, z_bottom]

    # =========================================================================
    # 6. PETROPHYSICAL DATA AND DIRECTIONAL UPSCALING
    # =========================================================================
    script_dir = os.path.dirname(os.path.abspath(__file__))
    perm_file = os.path.join(script_dir, "spe10_full_model_perm.dat")
    por_file = os.path.join(script_dir, "spe10_full_model_por.dat")

    if os.path.exists(perm_file) and os.path.exists(por_file):
        sim.rock_properties.perm_filename = perm_file
        sim.rock_properties.por_filename = por_file
        sim.rock_properties.rock_regularization = True
        sim.rock_properties.upscaling.method_x = pyfossil.UpscalingMethod.POWER_LAW
        sim.rock_properties.upscaling.method_y = pyfossil.UpscalingMethod.POWER_LAW
        sim.rock_properties.upscaling.power_law_exponent_x = 0.33
        sim.rock_properties.upscaling.power_law_exponent_y = 0.33
        sim.rock_properties.upscaling.method_z = pyfossil.UpscalingMethod.HARMONIC
        sim.rock_properties.upscaling.por_method = pyfossil.UpscalingMethod.ARITHMETIC
    else:
        # Homogeneous properties fallback
        sim.rock_properties.perm_x = 100.0 * MD_TO_M2
        sim.rock_properties.perm_y = 100.0 * MD_TO_M2
        sim.rock_properties.perm_z = 10.0 * MD_TO_M2
        sim.rock_properties.porosity = 0.20

    # =========================================================================
    # 7. EXECUTION CONTROL AND NUMERICAL SOLVERS
    # =========================================================================
    sim.execution_control.variables = {pyfossil.Variable.SW}
    sim.execution_control.abstol = 1.0e-5
    sim.execution_control.reltol = 1.0e-4
    sim.execution_control.bounds_check_at_reconstruction = True
    sim.execution_control.bounds_check_at_each_timestep = True
    sim.execution_control.num_threads = 4

    # KPP central-upwind scheme for two-phase flow
    sim.execution_control.num_method = pyfossil.NumericalMethod.KPP
    sim.execution_control.time_integrator = pyfossil.TimeIntegrator.BDF
    sim.execution_control.nonlinear_solver = pyfossil.NonlinearSolver.NEWTON

    # Darcy H-MFE with CG and BoomerAMG
    sim.execution_control.darcy_linear_solver = pyfossil.DarcyLinearSolver.CG
    sim.execution_control.darcy_preconditioner = pyfossil.DarcyPreconditioner.BOOMER_AMG

    # Transport implicit JFNK with GMRES and Block-ILU
    sim.execution_control.transport_linear_solver = pyfossil.TransportLinearSolver.GMRES
    sim.execution_control.transport_preconditioner = pyfossil.TransportPreconditioner.BLOCK_ILU

    # Adaptive macro time stepping based on Delta Sw
    sim.execution_control.darcy_extrapolation_degree = 0
    sim.execution_control.darcy_time_step_strategy = pyfossil.DarcyTimeStepStrategy.SW_VARIATION
    sim.execution_control.darcy_error_tolerance = 0.05

    # =========================================================================
    # 8. TIME STEPPING AND OUTPUT CONTROL
    # =========================================================================
    sim.time_data.final_time = 2000.0 * DAYS_TO_SEC      # 2000 days total
    sim.time_data.darcy_time_step = 0.25 * DAYS_TO_SEC   # 6 hours initial step
    sim.time_data.max_time_step = 10.0 * DAYS_TO_SEC     # 10 days max step

    sim.output_control.write_pressure_drop_file = True
    sim.output_control.text_output_interval = 10.0 * DAYS_TO_SEC

    # =========================================================================
    # 9. SEALED NO-FLOW EXTERNAL BOUNDARIES
    # =========================================================================
    bcs = sim.initial_and_boundary_conditions
    for name in ["Left", "Right", "Top", "Bottom", "Front", "Back"]:
        bcs[name].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
        bcs[name].darcy_boundary_value = 0.0
        bcs[name].trans_boundary_type = pyfossil.TransportBoundaryType.NO_FLOW

    return sim


if __name__ == "__main__":
    print("==================================================================")
    print(" FOSSIL Tutorial 4: SPE 10 Model 2 (3D Field Simulation)")
    print("==================================================================")

    # 1. Build benchmark model
    sim_data = build_spe_model()

    # 2. Initialize simulator and register dynamic callback
    output_dir = "./output_spe10_3d"
    simulator = pyfossil.FossilSimulator(sim_data, output_dir)
    simulator.set_step_callback(well_control_callback)

    # 3. Execute simulation
    try:
        simulator.run()
        print("\n[SUCCESS] SPE 10 simulation completed successfully!")
        print(f"Well production profiles and pressure drop files saved to: '{output_dir}/'")
        print("To generate comparison plots, execute: python plot.py")
    except Exception as err:
        print(f"\n[SIMULATION ERROR]: {err}")
