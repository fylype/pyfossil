#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
TUTORIAL 2: 2D Unstructured Mesh with Central Well Cavity & Multiple Materials
================================================================================

Demonstrates FOSSIL's advanced capabilities for handling hybrid unstructured
grids generated in Gmsh, containing an internal wellbore perforation cavity
and a heterogeneous petrophysical distribution defined by Gmsh Material IDs.

Physical and Numerical Highlights:
----------------------------------
1. Unstructured Geometry (Gmsh .msh):
   2D triangular/quadrilateral mesh refined around the central well cavity.
2. Heterogeneous Material Mapping (Material IDs):
   Assigns distinct permeability tensors (Kx, Ky) and porosities to each Gmsh
   physical surface tag using Python dictionaries (`materials_id`).
3. Kovscek et al. Local Equilibrium (LE) Foam Model:
   Foam bubble texture adapts dynamically based on local interstitial velocity
   and active surfactant concentration.
4. Reactive Surfactant Transport (Cs):
   Coupled conservation of chemical agent dissolved in the aqueous phase.
5. Non-Ideal Real-Gas Thermodynamics via PVT Table:
   Compressible flow with tabular Pressure vs. Density interpolation.
6. High-Performance Linear Solvers:
   Solves the elliptic Darcy system via BiCGSTAB preconditioned by HYPRE BoomerAMG.

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


def build_unstructured_2d_model() -> pyfossil.SimulationData:
    """
    Configures the 2D unstructured multi-material cavity simulation.
    """
    sim = pyfossil.SimulationData()

    # =========================================================================
    # 1. LOAD UNSTRUCTURED MESH (GMSH .MSH)
    # =========================================================================
    sim.global_settings.mesh_type = pyfossil.MeshType.UNSTRUCTURED_MESH
    sim.global_settings.dimension = 2

    # Path to the Gmsh mesh file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mesh_path = os.path.join(script_dir, "reservatorio_com_furo_Materials.msh")
    sim.unstructured_geometry.mesh_filename = mesh_path

    # =========================================================================
    # 2. FLUID PROPERTIES AND PVT THERMODYNAMICS
    # =========================================================================
    sim.fluid_properties.water_viscosity = 1.0e-3     # Water viscosity = 1.0 cP (Pa.s)
    sim.fluid_properties.water_density = 1000.0       # Water density = 1000 kg/m^3
    sim.fluid_properties.gas_viscosity = 4.6e-5       # Gas viscosity = 0.046 cP (Pa.s)
    sim.fluid_properties.gas_density = 1.65           # Reference gas density

    # Real-gas compressibility via discrete PVT table (Pressure vs Density)
    sim.fluid_properties.gas_compressibility = True
    sim.fluid_properties.gas_state_equation = pyfossil.GasStateEquationModel.DENSITY_TABLE

    # Experimental PVT mapping: Pressure [Pa] -> Density [kg/m^3]
    sim.fluid_properties.table_density_model.density_table = {
        100000: 1.8152, 500000: 9.2761, 1000000: 19.099, 2000000: 40.773,
        3000000: 66.156, 4000000: 97.492, 6000000: 186.95, 8000000: 378.30,
        10000000: 562.50, 15000000: 629.77, 20000000: 655.14, 30000000: 682.72,
        40000000: 698.16
    }

    # =========================================================================
    # 3. KOVSCEK ET AL. FOAM MECHANISTIC MODEL
    # =========================================================================
    sim.physical_models.foam_model = pyfossil.FoamModel.KOVSCEK
    sim.eor_mechanisms.n_max = 1.0e12                       # Maximum bubble density [m^-3]
    sim.eor_mechanisms.kovscek_model.k01 = 1.65e15          # Generation rate coefficient
    sim.eor_mechanisms.kovscek_model.k0m1 = 10.0            # Coalescence rate coefficient
    sim.eor_mechanisms.kovscek_model.refSurf = 0.083        # Critical surfactant threshold [wt%]
    sim.eor_mechanisms.kovscek_model.alpha = 5.7e-16        # Shear-thinning parameter
    sim.eor_mechanisms.kovscek_model.pcStarMax = 1.83e4     # Critical capillary pressure
    sim.eor_mechanisms.kovscek_model.const_trapping = True  # Constant trapped bubble fraction
    sim.eor_mechanisms.kovscek_model.XtMax = 0.0

    # =========================================================================
    # 4. COREY-BROOKS RELPERMS & LEVERETT-J CAPILLARITY
    # =========================================================================
    sim.rock_fluid_interactions.swc = 0.02
    sim.rock_fluid_interactions.sgr = 0.0
    sim.rock_fluid_interactions.sigma_wg = 0.035            # Interfacial tension = 35 mN/m
    sim.rock_fluid_interactions.rel_perm_model = pyfossil.RelativePermeabilityModel.COREY_BROOKS_KR
    sim.rock_fluid_interactions.corey_brooks_rel_perm.krg0 = 0.57
    sim.rock_fluid_interactions.corey_brooks_rel_perm.krw0 = 1.0
    sim.rock_fluid_interactions.corey_brooks_rel_perm.pore_dist_coeff = 4.24

    sim.rock_fluid_interactions.cap_pressure_model = pyfossil.CapillaryPressureModel.LEVERETT_J
    sim.rock_fluid_interactions.leverett_j_cp_model.gamma = 0.19
    sim.rock_fluid_interactions.leverett_j_cp_model.pore_dist_coeff = 4.24

    # =========================================================================
    # 5. INITIAL FIELD STATE
    # =========================================================================
    sim.initial_and_boundary_conditions.initial_state.pressure_init.constant_value = 101325.0  # 1 atm initial
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.SW].constant_value = 1.0  # 100% water saturated
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.CS].constant_value = 0.0  # No initial surfactant

    # =========================================================================
    # 6. PETROPHYSICAL MAPPING VIA MATERIAL IDS (GMSH PHYSICAL SURFACES)
    # =========================================================================
    # The mesh contains 4 distinct geological regions tagged with IDs 1, 2, 3, and 4
    sim.rock_properties.use_material_ids = True
    sim.rock_properties.permeability_x_map = {
        1: 1.0e-12,   # Region 1: High permeability (1000 mD)
        2: 8.0e-13,   # Region 2: Moderate permeability (800 mD)
        3: 4.0e-13,   # Region 3: Low permeability barrier (400 mD)
        4: 3.0e-12    # Region 4: High-flow channel (3000 mD)
    }
    sim.rock_properties.permeability_y_map = sim.rock_properties.permeability_x_map
    sim.rock_properties.porosity_map = {
        1: 0.22,      # 22%
        2: 0.26,      # 26%
        3: 0.32,      # 32%
        4: 0.18       # 18%
    }

    # =========================================================================
    # 7. EXECUTION CONTROL AND NUMERICAL SOLVERS
    # =========================================================================
    # 3 active coupled conservation variables: Sw, nD, and surfactant concentration Cs
    sim.execution_control.variables = {
        pyfossil.Variable.SW,
        pyfossil.Variable.ND,
        pyfossil.Variable.CS
    }
    sim.execution_control.foam_behavior = pyfossil.FoamBehavior.LOCAL_EQUILIBRIUM
    sim.execution_control.surfactant_behavior = pyfossil.SurfactantBehavior.COMPUTED

    # Darcy solver: BiCGSTAB with HYPRE BoomerAMG algebraic multigrid
    sim.execution_control.darcy_linear_solver = pyfossil.DarcyLinearSolver.BiCGSTAB
    sim.execution_control.darcy_preconditioner = pyfossil.DarcyPreconditioner.BOOMER_AMG

    # Transport solver: JFNK with GMRES and Block-ILU
    sim.execution_control.transport_linear_solver = pyfossil.TransportLinearSolver.GMRES
    sim.execution_control.transport_preconditioner = pyfossil.TransportPreconditioner.BLOCK_ILU

    # KNP central-upwind finite volume scheme and OpenMP threading
    sim.execution_control.num_method = pyfossil.NumericalMethod.KNP
    sim.execution_control.abstol = 1.0e-6
    sim.execution_control.reltol = 1.0e-4
    sim.execution_control.bounds_check_at_reconstruction = True
    sim.execution_control.num_threads = 4

    # =========================================================================
    # 8. TIME HORIZON
    # =========================================================================
    sim.time_data.final_time = 200000.0     # 200,000 seconds (~2.3 days)
    sim.time_data.darcy_time_step = 500.0   # Macro Darcy time step = 500 s

    # =========================================================================
    # 9. DYNAMIC BOUNDARY CONDITIONS ON GMSH CURVES
    # =========================================================================
    bcs = sim.initial_and_boundary_conditions
    bcs.setup_dynamic_boundaries(["Bottom", "Right", "Top", "Left", "Hole"])

    # Impermeable outer boundaries (Top and Bottom)
    for name in ["Bottom", "Top"]:
        bcs[name].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
        bcs[name].darcy_boundary_value = 0.0
        bcs[name].trans_boundary_type = pyfossil.TransportBoundaryType.NO_FLOW

    # Pressure relief outflow boundaries (Left and Right)
    for name in ["Left", "Right"]:
        bcs[name].darcy_boundary_type = pyfossil.DarcyBoundaryType.DIRICHLET
        bcs[name].darcy_boundary_value = 101325.0  # Atmospheric discharge pressure
        bcs[name].trans_boundary_type = pyfossil.TransportBoundaryType.OUTFLOW

    # Central well perforation cavity ("Hole", ID=5):
    # Prescribed total fluid injection flux with water, gas, and surfactant
    bcs["Hole"].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
    bcs["Hole"].darcy_boundary_value = 6.63e-6   # Darcy injection velocity [m/s]
    bcs["Hole"].trans_boundary_type = pyfossil.TransportBoundaryType.INFLOW_DIRICHLET
    bcs["Hole"].trans_boundary_values[pyfossil.Variable.SW] = 0.43   # 43% injected water saturation
    bcs["Hole"].trans_boundary_values[pyfossil.Variable.CS] = 1.0    # 1.0 wt% injected surfactant concentration

    return sim


if __name__ == "__main__":
    print("==================================================================")
    print(" FOSSIL Tutorial 2: 2D Unstructured Mesh with Hole & Materials")
    print("==================================================================")

    # 1. Build configuration container
    model = build_unstructured_2d_model()

    # 2. Initialize simulator
    output_dir = "./output_unstructured_2d"
    simulator = pyfossil.FossilSimulator(model, output_dir)

    # 3. Execute simulation
    try:
        simulator.run()
        print("\n[SUCCESS] Simulation completed successfully!")
        print(f"VTU spatial fields saved to: '{output_dir}/'")
        print("Visualize results by opening the .vtu files in ParaView.")
    except Exception as err:
        print(f"\n[SIMULATION ERROR]: {err}")
