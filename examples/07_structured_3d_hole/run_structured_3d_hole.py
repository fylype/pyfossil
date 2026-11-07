#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
TUTORIAL 7: 3D Structured Hexahedral Mesh with Well Perforation Cavity (Gmsh)
================================================================================

Demonstrates 3D simulation on a curvilinear structured hexahedral grid generated
in Gmsh (`reservatorio_com_furo.msh`), preserving geometric regularity and high
boundary resolution along an internal cylindrical well perforation.

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


def build_structured_3d_model() -> pyfossil.SimulationData:
    sim = pyfossil.SimulationData()

    # 1. 3D Grid Loading
    sim.global_settings.mesh_type = pyfossil.MeshType.UNSTRUCTURED_MESH
    sim.global_settings.dimension = 3
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sim.unstructured_geometry.mesh_filename = os.path.join(script_dir, "reservatorio_com_furo.msh")

    # 2. Fluid Thermodynamics & Compressibility
    sim.fluid_properties.water_viscosity = 1.0e-3
    sim.fluid_properties.water_density = 1000.0
    sim.fluid_properties.gas_viscosity = 4.6e-5
    sim.fluid_properties.gas_density = 1.65
    sim.fluid_properties.gas_compressibility = True
    sim.fluid_properties.gas_state_equation = pyfossil.GasStateEquationModel.DENSITY_TABLE
    sim.fluid_properties.table_density_model.density_table = {
        100000: 1.8152, 500000: 9.2761, 1000000: 19.099, 2000000: 40.773,
        3000000: 66.156, 4000000: 97.492, 6000000: 186.95, 8000000: 378.30,
        10000000: 562.50, 20000000: 655.14, 40000000: 698.16
    }

    # 3. Kovscek Foam Model
    sim.physical_models.foam_model = pyfossil.FoamModel.KOVSCEK
    sim.eor_mechanisms.n_max = 1.0e12
    sim.eor_mechanisms.kovscek_model.k01 = 1.65e15
    sim.eor_mechanisms.kovscek_model.k0m1 = 10.0
    sim.eor_mechanisms.kovscek_model.refSurf = 0.083
    sim.eor_mechanisms.kovscek_model.alpha = 5.7e-16
    sim.eor_mechanisms.kovscek_model.pcStarMax = 1.83e4
    sim.eor_mechanisms.kovscek_model.const_trapping = True
    sim.eor_mechanisms.kovscek_model.XtMax = 0.0

    # 4. Rock-Fluid Interactions
    sim.rock_fluid_interactions.swc = 0.02
    sim.rock_fluid_interactions.sgr = 0.0
    sim.rock_fluid_interactions.sigma_wg = 0.035
    sim.rock_fluid_interactions.rel_perm_model = pyfossil.RelativePermeabilityModel.COREY_BROOKS_KR
    sim.rock_fluid_interactions.corey_brooks_rel_perm.krg0 = 0.57
    sim.rock_fluid_interactions.corey_brooks_rel_perm.krw0 = 1.0
    sim.rock_fluid_interactions.corey_brooks_rel_perm.pore_dist_coeff = 4.24

    sim.rock_fluid_interactions.cap_pressure_model = pyfossil.CapillaryPressureModel.LEVERETT_J
    sim.rock_fluid_interactions.leverett_j_cp_model.gamma = 0.19
    sim.rock_fluid_interactions.leverett_j_cp_model.pore_dist_coeff = 4.24

    # 5. Initial State
    sim.initial_and_boundary_conditions.initial_state.pressure_init.constant_value = 101325.0
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.SW].constant_value = 1.0
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.CS].constant_value = 0.0

    # 6. Stochastic Heterogeneous Rock Field
    sim.rock_properties.use_synthetic_field = True
    sim.rock_properties.synthetic_rock_field.seed = 123456789123456789
    sim.rock_properties.synthetic_rock_field.permeability_avg = 1.085e-12
    sim.rock_properties.synthetic_rock_field.porosity_avg = 0.22
    sim.rock_properties.synthetic_rock_field.heterogeneity = 1.0

    # 7. Solvers and Execution
    sim.execution_control.variables = {
        pyfossil.Variable.SW,
        pyfossil.Variable.ND,
        pyfossil.Variable.CS
    }
    sim.execution_control.foam_behavior = pyfossil.FoamBehavior.LOCAL_EQUILIBRIUM
    sim.execution_control.surfactant_behavior = pyfossil.SurfactantBehavior.COMPUTED
    sim.execution_control.abstol = 1.0e-6
    sim.execution_control.reltol = 1.0e-4
    sim.execution_control.bounds_check_at_reconstruction = True
    sim.execution_control.num_threads = 4
    sim.execution_control.num_method = pyfossil.NumericalMethod.KNP
    sim.execution_control.time_integrator = pyfossil.TimeIntegrator.BDF
    sim.execution_control.darcy_linear_solver = pyfossil.DarcyLinearSolver.BiCGSTAB
    sim.execution_control.darcy_preconditioner = pyfossil.DarcyPreconditioner.BOOMER_AMG
    sim.execution_control.transport_linear_solver = pyfossil.TransportLinearSolver.GMRES
    sim.execution_control.transport_preconditioner = pyfossil.TransportPreconditioner.BLOCK_ILU

    # 8. Time Stepping
    sim.time_data.final_time = 200000.0
    sim.time_data.darcy_time_step = 500.0
    sim.time_data.max_time_step = 1.0e6

    # 9. Boundary Conditions
    bcs = sim.initial_and_boundary_conditions
    bcs.setup_dynamic_boundaries(["Left", "Right", "Bottom", "Top", "Front", "Back", "Hole"])

    bcs["Left"].darcy_boundary_type = pyfossil.DarcyBoundaryType.DIRICHLET
    bcs["Left"].darcy_boundary_value = 101325.0
    bcs["Left"].trans_boundary_type = pyfossil.TransportBoundaryType.OUTFLOW

    bcs["Right"].darcy_boundary_type = pyfossil.DarcyBoundaryType.DIRICHLET
    bcs["Right"].darcy_boundary_value = 101325.0
    bcs["Right"].trans_boundary_type = pyfossil.TransportBoundaryType.OUTFLOW

    for name in ["Bottom", "Top", "Front", "Back"]:
        bcs[name].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
        bcs[name].darcy_boundary_value = 0.0
        bcs[name].trans_boundary_type = pyfossil.TransportBoundaryType.NO_FLOW

    bcs["Hole"].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
    bcs["Hole"].darcy_boundary_value = 6.63e-6
    bcs["Hole"].trans_boundary_type = pyfossil.TransportBoundaryType.INFLOW_DIRICHLET
    bcs["Hole"].trans_boundary_values[pyfossil.Variable.SW] = 0.43
    bcs["Hole"].trans_boundary_values[pyfossil.Variable.CS] = 1.0

    return sim


if __name__ == "__main__":
    print("==================================================================")
    print(" FOSSIL Tutorial 7: 3D Structured Mesh with Well Perforation")
    print("==================================================================")

    model = build_structured_3d_model()
    output_dir = "./output_structured_3d"
    simulator = pyfossil.FossilSimulator(model, output_dir)

    try:
        simulator.run()
        print("\n[SUCCESS] 3D simulation completed successfully!")
    except Exception as err:
        print(f"\n[SIMULATION ERROR]: {err}")
