#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
TUTORIAL 4B: SPE 10 Benchmark on 3D Unstructured Mesh with Local Grid Refinement
================================================================================

Demonstrates the SPE 10 benchmark executed on an unstructured tetrahedral mesh
generated in Gmsh (`spe10_reservatorio_com_pocos.msh`), featuring Local Grid
Refinement (LGR) surrounding the 5 vertical wells to capture steep near-well
pressure gradients accurately.

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

DAYS_TO_SEC = 86400.0
FT_TO_M = 0.3048
PSI_TO_PA = 6894.757
CP_TO_PA_S = 0.001
BBL_DAY_TO_M3_S = 1.84013e-6
MD_TO_M2 = 9.86923e-16

MAX_INJ_BHP = 10000.0 * PSI_TO_PA
TARGET_INJ_RATE = 5000.0 * BBL_DAY_TO_M3_S
PROD_BHP = 4000.0 * PSI_TO_PA

well_controller_state = {
    "mode": "FLOW_RATE",
    "switch_count": 0
}

def well_control_callback(t_physical: float, sim, sim_data) -> bool:
    """Dynamic well control callback with 2% hysteresis deadband."""
    t_days = t_physical / DAYS_TO_SEC
    inj_bhp = sim.get_current_well_bhp("INJ1")
    current_mode = well_controller_state["mode"]

    if current_mode == "FLOW_RATE":
        if inj_bhp >= MAX_INJ_BHP:
            well_controller_state["mode"] = "BHP"
            sim_data.wells["INJ1"].well_control = pyfossil.WellControl.BHP
            sim_data.wells["INJ1"].well_value = MAX_INJ_BHP
            well_controller_state["switch_count"] += 1
            print(f"\n[WELL CONTROL @ {t_days:.3f} days] INJ1 reached maximum BHP (10,000 psi). Switching to BHP mode.")

    elif current_mode == "BHP":
        inj_rate = sim.get_current_well_rate("INJ1")
        if inj_rate >= TARGET_INJ_RATE * 1.02:
            well_controller_state["mode"] = "FLOW_RATE"
            sim_data.wells["INJ1"].well_control = pyfossil.WellControl.FLOW_RATE
            sim_data.wells["INJ1"].well_value = TARGET_INJ_RATE
            well_controller_state["switch_count"] += 1
            print(f"\n[WELL CONTROL @ {t_days:.3f} days] INJ1 recovered injection capacity. Switching to Rate mode.")

    return True


def build_spe_unstructured_model() -> pyfossil.SimulationData:
    sim = pyfossil.SimulationData()

    # 1. 3D Unstructured Gmsh Grid
    sim.global_settings.mesh_type = pyfossil.MeshType.UNSTRUCTURED_MESH
    sim.global_settings.dimension = 3
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sim.unstructured_geometry.mesh_filename = os.path.join(script_dir, "spe10_reservatorio_com_pocos.msh")

    # 2. Fluid Thermodynamics
    sim.fluid_properties.water_viscosity = 0.3 * CP_TO_PA_S
    sim.fluid_properties.water_density = 64.0 * 16.0185
    sim.fluid_properties.gas_viscosity = 3.0 * CP_TO_PA_S
    sim.fluid_properties.gas_compressibility = True
    sim.fluid_properties.gas_state_equation = pyfossil.GasStateEquationModel.DENSITY_TABLE
    sim.fluid_properties.table_density_model.density_table = {
        300.0 * PSI_TO_PA: 50.70 * 16.0185,
        800.0 * PSI_TO_PA: 51.58 * 16.0185,
        8000.0 * PSI_TO_PA: 52.48 * 16.0185
    }
    sim.fluid_properties.gravity = True
    sim.fluid_properties.gravity_direction = [0.0, 0.0, 9.81]

    # 3. Rock-Fluid Interactions
    sim.rock_fluid_interactions.swc = 0.20
    sim.rock_fluid_interactions.sgr = 0.20
    sim.rock_fluid_interactions.rel_perm_model = pyfossil.RelativePermeabilityModel.CUSTOM_KR
    sim.rock_fluid_interactions.custom_rel_perm.nw = 2.0
    sim.rock_fluid_interactions.custom_rel_perm.ng = 2.0

    # 4. Initial Reservoir State
    sim.initial_and_boundary_conditions.initial_state.pressure_init.constant_value = 6000.0 * PSI_TO_PA
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.SW].constant_value = 0.20

    # 5. Peaceman Wells (Same trajectories as 3D field case)
    z_top, z_bottom = 0.0, 170.0 * FT_TO_M

    w_inj = sim.wells["INJ1"]
    w_inj.well_type = pyfossil.WellType.INJECTOR
    w_inj.well_control = pyfossil.WellControl.FLOW_RATE
    w_inj.well_value = TARGET_INJ_RATE
    w_inj.well_radius = 0.10
    w_inj.include_hydrostatic_head = True
    w_inj.trajectory_coords = [600.0 * FT_TO_M, 1100.0 * FT_TO_M, z_top, 600.0 * FT_TO_M, 1100.0 * FT_TO_M, z_bottom]

    producers = {"P1": (0.0, 0.0), "P2": (1200.0, 0.0), "P3": (1200.0, 2200.0), "P4": (0.0, 2200.0)}
    eps_m = 0.1
    for p_name, (x_ft, y_ft) in producers.items():
        w_prod = sim.wells[p_name]
        w_prod.well_type = pyfossil.WellType.PRODUCER
        w_prod.well_control = pyfossil.WellControl.BHP
        w_prod.well_value = PROD_BHP
        w_prod.well_radius = 0.10
        w_prod.include_hydrostatic_head = True
        x_m = max(eps_m, min(1200.0 * FT_TO_M - eps_m, x_ft * FT_TO_M))
        y_m = max(eps_m, min(2200.0 * FT_TO_M - eps_m, y_ft * FT_TO_M))
        w_prod.trajectory_coords = [x_m, y_m, z_top, x_m, y_m, z_bottom]

    # 6. Rock Properties
    sim.rock_properties.perm_x = 100.0 * MD_TO_M2
    sim.rock_properties.perm_y = 100.0 * MD_TO_M2
    sim.rock_properties.perm_z = 10.0 * MD_TO_M2
    sim.rock_properties.porosity = 0.20

    # 7. Solvers
    sim.execution_control.variables = {pyfossil.Variable.SW}
    sim.execution_control.darcy_linear_solver = pyfossil.DarcyLinearSolver.CG
    sim.execution_control.darcy_preconditioner = pyfossil.DarcyPreconditioner.BOOMER_AMG
    sim.execution_control.transport_linear_solver = pyfossil.TransportLinearSolver.GMRES
    sim.execution_control.transport_preconditioner = pyfossil.TransportPreconditioner.BLOCK_ILU
    sim.execution_control.num_method = pyfossil.NumericalMethod.KPP
    sim.execution_control.abstol = 1.0e-5
    sim.execution_control.reltol = 1.0e-4
    sim.execution_control.num_threads = 4

    # 8. Time Stepping
    sim.time_data.final_time = 2000.0 * DAYS_TO_SEC
    sim.time_data.darcy_time_step = 0.25 * DAYS_TO_SEC
    sim.time_data.max_time_step = 10.0 * DAYS_TO_SEC
    sim.output_control.write_pressure_drop_file = True
    sim.output_control.text_output_interval = 10.0 * DAYS_TO_SEC

    # 9. Boundaries
    bcs = sim.initial_and_boundary_conditions
    bcs.setup_dynamic_boundaries(["Left", "Right", "Bottom", "Top", "Front", "Back"])
    for name in ["Left", "Right", "Bottom", "Top", "Front", "Back"]:
        bcs[name].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
        bcs[name].darcy_boundary_value = 0.0
        bcs[name].trans_boundary_type = pyfossil.TransportBoundaryType.NO_FLOW

    return sim


if __name__ == "__main__":
    print("==================================================================")
    print(" FOSSIL Tutorial 4B: SPE 10 Model 2 (3D Unstructured Mesh)")
    print("==================================================================")

    model = build_spe_unstructured_model()
    output_dir = "./output_spe10_unstructured_3d"
    simulator = pyfossil.FossilSimulator(model, output_dir)
    simulator.set_step_callback(well_control_callback)

    try:
        simulator.run()
        print("\n[SUCCESS] Unstructured 3D simulation completed successfully!")
    except Exception as err:
        print(f"\n[SIMULATION ERROR]: {err}")
