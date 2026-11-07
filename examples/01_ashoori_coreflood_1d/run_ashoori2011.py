#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
TUTORIAL 1: 1D Coreflood Foam Displacement (Ashoori et al., 2011)
================================================================================

Numerically replicates the experimental laboratory benchmark of Ashoori et al.
(2011) for transient foam generation and propagation in 1D homogeneous porous media.

Physical and Numerical Highlights:
----------------------------------
1. H-MFE (Hybridized Mixed Finite Elements) for Darcy flow:
   Guarantees strict local mass conservation and continuous velocity fields.
2. Implicit Transport via JFNK (Jacobian-Free Newton-Krylov) with SUNDIALS CVODE:
   Stiff variable-order, variable-step multi-step BDF time integration with the
   high-resolution KNP (Kurganov-Noelle-Petrova) central-upwind finite volume scheme.
3. Ashoori et al. (2011) Foam Population Balance Model:
   Coupled dynamic bubble texture (nD) and water saturation (Sw):
   - A: Lamella division kinetic bubble generation.
   - Sw_critical: Critical capillary transition water saturation.
   - max_mob_red (MRF): Maximum gas mobility reduction factor.
   - K_c: Lamella coalescence rate constant.
4. Laboratory Boundary Conditions:
   Darcy influx velocity (Neumann) on the Left face with specified Sw and nD,
   and atmospheric Dirichlet pressure on the Right face.

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


def build_ashoori_model(kc: float = 1.0) -> pyfossil.SimulationData:
    """
    Constructs and parameterizes the Ashoori 1D coreflood model.

    Parameters:
    -----------
    kc : float
        Kinetic coalescence / destruction constant (default = 1.0).

    Returns:
    --------
    pyfossil.SimulationData
        Configured simulation container ready for execution.
    """
    sim = pyfossil.SimulationData()

    # =========================================================================
    # 1. GEOMETRY AND SPATIAL DISCRETIZATION
    # =========================================================================
    # 1D coreflood laboratory domain (0.05 m length x 0.005 m width x 0.005 m thickness)
    sim.global_settings.mesh_type = pyfossil.MeshType.ORTHOGONAL_MESH
    sim.global_settings.dimension = 3

    sim.orthogonal_geometry.n_x = 200  # 200 refined cells along the core length (dx = 0.25 mm)
    sim.orthogonal_geometry.n_y = 1    # 1 cell in Y (1D symmetry)
    sim.orthogonal_geometry.n_z = 1    # 1 cell in Z

    sim.orthogonal_geometry.x_init = 0.0
    sim.orthogonal_geometry.x_final = 0.05    # 5 cm length
    sim.orthogonal_geometry.y_init = 0.0
    sim.orthogonal_geometry.y_final = 0.005   # 0.5 cm
    sim.orthogonal_geometry.z_init = 0.0
    sim.orthogonal_geometry.z_final = 0.005   # 0.5 cm

    # =========================================================================
    # 2. FLUID THERMODYNAMICS AND VISCOSITIES
    # =========================================================================
    # SI units (Pa.s, kg/m^3)
    sim.fluid_properties.water_viscosity = 1.0e-3     # Water: 1.0 cP = 1.0e-3 Pa.s
    sim.fluid_properties.gas_viscosity = 2.0e-5       # Gas: 0.02 cP = 2.0e-5 Pa.s
    sim.fluid_properties.water_density = 1000.0       # Water density: 1000 kg/m^3
    sim.fluid_properties.gas_density = 1.165          # Gas density: 1.165 kg/m^3

    # Incompressible flow regime for low-pressure laboratory coreflood
    sim.fluid_properties.gas_compressibility = False

    # =========================================================================
    # 3. EOR FOAM POPULATION BALANCE: ASHOORI ET AL. (2011)
    # =========================================================================
    sim.physical_models.foam_model = pyfossil.FoamModel.ASHOORI
    sim.eor_mechanisms.ashoori_model.A = 400.0             # Lamella division bubble generation
    sim.eor_mechanisms.ashoori_model.sw_critical = 0.37    # Critical capillary water saturation
    sim.eor_mechanisms.ashoori_model.max_mob_red = 18500.0 # Maximum gas mobility reduction factor (MRF)
    sim.eor_mechanisms.ashoori_model.K_c = kc              # Lamella destruction kinetic rate

    # =========================================================================
    # 4. ROCK-FLUID INTERACTIONS: RELATIVE PERMEABILITY & CAPILLARITY
    # =========================================================================
    sim.rock_fluid_interactions.swc = 0.20  # Connate water saturation (Swc = 20%)
    sim.rock_fluid_interactions.sgr = 0.18  # Residual gas saturation (Sgr = 18%)

    # Ashoori empirical quadratic formulations
    sim.rock_fluid_interactions.rel_perm_model = pyfossil.RelativePermeabilityModel.ASHOORI_KR
    sim.rock_fluid_interactions.cap_pressure_model = pyfossil.CapillaryPressureModel.ASHOORI_CP

    # =========================================================================
    # 5. INITIAL RESERVOIR STATE (t = 0)
    # =========================================================================
    # Core is initially saturated with water (Sw = 0.72) and coarse gas bubbles (nD = 1.0)
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.SW].initialization_type = pyfossil.InitializationType.CONSTANT
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.SW].constant_value = 0.72

    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.ND].initialization_type = pyfossil.InitializationType.CONSTANT
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.ND].constant_value = 1.0

    # =========================================================================
    # 6. ROCK PETROPHYSICS (Homogeneous)
    # =========================================================================
    sim.rock_properties.porosity = 0.25               # Porosity = 25%
    sim.rock_properties.perm_x = 1.0e-12              # Absolute permeability = 1 Darcy (1.0e-12 m^2)
    sim.rock_properties.perm_y = 1.0e-12
    sim.rock_properties.perm_z = 1.0e-12

    # =========================================================================
    # 7. EXECUTION CONTROL & NUMERICAL SOLVERS
    # =========================================================================
    # Active PDE conservation variables: Water Saturation and Foam Texture
    sim.execution_control.variables = {pyfossil.Variable.SW, pyfossil.Variable.ND}
    sim.execution_control.foam_behavior = pyfossil.FoamBehavior.COMPUTED

    # Solver tolerances for SUNDIALS CVODE (BDF)
    sim.execution_control.abstol = 1.0e-8
    sim.execution_control.reltol = 1.0e-6

    # Darcy linear solver: UMFPACK (exact direct LU factorization)
    sim.execution_control.darcy_linear_solver = pyfossil.DarcyLinearSolver.UMFPACK
    sim.execution_control.darcy_preconditioner = pyfossil.DarcyPreconditioner.NONE

    # Transport solver: JFNK with GMRES and Block-ILU preconditioner
    sim.execution_control.transport_linear_solver = pyfossil.TransportLinearSolver.GMRES
    sim.execution_control.transport_preconditioner = pyfossil.TransportPreconditioner.BLOCK_ILU

    # Spatial scheme: KNP (Kurganov-Noelle-Petrova central-upwind)
    sim.execution_control.num_method = pyfossil.NumericalMethod.KNP
    sim.execution_control.bounds_check_at_reconstruction = True
    sim.execution_control.num_threads = 4  # OpenMP threads

    # =========================================================================
    # 8. TIME HORIZON AND TIMESTEPPING
    # =========================================================================
    sim.time_data.final_time = 100.0        # Total simulation time: 100 s
    sim.time_data.darcy_time_step = 0.1     # Darcy macro time step: 0.10 s
    sim.time_data.max_time_step = 10.0      # Maximum allowed time step

    # =========================================================================
    # 9. BOUNDARY CONDITIONS (Inflow and Outflow)
    # =========================================================================
    bcs = sim.initial_and_boundary_conditions

    # Impermeable lateral boundaries
    for name in ["Top", "Bottom", "Front", "Back"]:
        bcs[name].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
        bcs[name].darcy_boundary_value = 0.0
        bcs[name].trans_boundary_type = pyfossil.TransportBoundaryType.NO_FLOW

    # Left face (Inflow, x = 0):
    # Constant total Darcy flux injection (u = 2.93e-5 m/s) with specified Sw and nD
    bcs["Left"].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
    bcs["Left"].darcy_boundary_value = 2.93e-5
    bcs["Left"].trans_boundary_type = pyfossil.TransportBoundaryType.INFLOW_DIRICHLET
    bcs["Left"].trans_boundary_values[pyfossil.Variable.SW] = 0.372
    bcs["Left"].trans_boundary_values[pyfossil.Variable.ND] = 0.664

    # Right face (Outflow, x = L):
    # Atmospheric reference pressure (P = 0.0 Pa gauge) with free outflow
    bcs["Right"].darcy_boundary_type = pyfossil.DarcyBoundaryType.DIRICHLET
    bcs["Right"].darcy_boundary_value = 0.0
    bcs["Right"].trans_boundary_type = pyfossil.TransportBoundaryType.OUTFLOW

    return sim


if __name__ == "__main__":
    print("==================================================================")
    print(" FOSSIL Tutorial 1: Ashoori 2011 Coreflood Foam Simulation")
    print("==================================================================")

    # 1. Build model configuration with Kc = 1.0
    sim_data = build_ashoori_model(kc=1.0)

    # 2. Instantiate simulator with output directory
    output_dir = "./output_Ashoori2011"
    simulator = pyfossil.FossilSimulator(sim_data, output_dir)

    # 3. Execute numerical simulation
    try:
        simulator.run()
        print("\n[SUCCESS] Simulation completed successfully!")
        print(f"VTU results saved to: '{output_dir}/'")
        print("To generate comparison plots, execute: python plot.py")
    except Exception as err:
        print(f"\n[SIMULATION ERROR]: {err}")
