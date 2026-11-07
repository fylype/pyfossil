#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
TUTORIAL 5: Chen et al. (2010) Coreflood Experiment - Foam & Surfactant
================================================================================

Numerically replicates the laboratory coreflood experiment of Chen et al. (2010)
for simultaneous gas and surfactant injection into Berea sandstone core,
modeled via the Kovscek et al. Local Equilibrium (LE) formulation coupled with
dynamic surfactant transport (Cs).

Physical and Numerical Highlights:
----------------------------------
1. Cylindrical Core Geometry:
   Length L = 0.60 m (60 cm) discretized into 200 cells along the x-axis.
2. Kovscek Foam Model in Local Equilibrium (LE):
   Equilibrium bubble texture evaluation accounting for shear-thinning rheology,
   critical capillary rupture, and surfactant concentration.
3. Kovscek Relative Permeabilities and Capillary Pressure:
   Cubic Corey saturation curves with nw = 3.0 and ng = 3.0.
4. Numerical Solvers:
   - Darcy: UMFPACK direct sparse LU solver.
   - Transport: SUNDIALS CVODE (BDF) with JFNK GMRES and KNP scheme.

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


def build_chen_model() -> pyfossil.SimulationData:
    sim = pyfossil.SimulationData()

    # 1. Core Geometry (0.60 m x 0.01 m x 0.01 m)
    sim.global_settings.mesh_type = pyfossil.MeshType.ORTHOGONAL_MESH
    sim.global_settings.dimension = 3
    sim.orthogonal_geometry.n_x = 200
    sim.orthogonal_geometry.n_y = 1
    sim.orthogonal_geometry.n_z = 1

    sim.orthogonal_geometry.x_init = 0.0
    sim.orthogonal_geometry.x_final = 0.60
    sim.orthogonal_geometry.y_init = 0.0
    sim.orthogonal_geometry.y_final = 0.01
    sim.orthogonal_geometry.z_init = 0.0
    sim.orthogonal_geometry.z_final = 0.01

    # 2. Fluid Thermodynamics
    sim.fluid_properties.water_viscosity = 1.0e-3
    sim.fluid_properties.water_density = 1000.0
    sim.fluid_properties.gas_viscosity = 1.8e-5
    sim.fluid_properties.gas_density = 1.165
    sim.fluid_properties.gas_compressibility = False

    # 3. EOR Mechanism: Kovscek LE Foam
    sim.physical_models.foam_model = pyfossil.FoamModel.KOVSCEK
    sim.eor_mechanisms.n_max = 1.0e12
    sim.eor_mechanisms.kovscek_model.k01 = 1.65e15
    sim.eor_mechanisms.kovscek_model.k0m1 = 10.0
    sim.eor_mechanisms.kovscek_model.krg0 = 1.0
    sim.eor_mechanisms.kovscek_model.ng = 3.0
    sim.eor_mechanisms.kovscek_model.krw0 = 0.7
    sim.eor_mechanisms.kovscek_model.nw = 3.0
    sim.eor_mechanisms.kovscek_model.alpha = 7.4e-18
    sim.eor_mechanisms.kovscek_model.pcStarMax = 3.0e4
    sim.eor_mechanisms.kovscek_model.XtMax = 0.78
    sim.eor_mechanisms.kovscek_model.const_trapping = True
    sim.eor_mechanisms.kovscek_model.refSurf = 0.083

    # 4. Relative Permeability & Capillary Pressure
    sim.rock_fluid_interactions.swc = 0.38
    sim.rock_fluid_interactions.sgr = 0.0
    sim.rock_fluid_interactions.sigma_wg = 0.033
    sim.rock_fluid_interactions.rel_perm_model = pyfossil.RelativePermeabilityModel.KOVSCEK_KR
    sim.rock_fluid_interactions.cap_pressure_model = pyfossil.CapillaryPressureModel.KOVSCEK_CP

    # 5. Initial State (Core pre-saturated with surfactant solution)
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.SW].constant_value = 1.0
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.CS].constant_value = 1.0

    # 6. Rock Properties (Berea Sandstone: ~300 mD, 18% porosity)
    sim.rock_properties.perm_x = 2.96e-13
    sim.rock_properties.perm_y = 2.96e-13
    sim.rock_properties.perm_z = 2.96e-13
    sim.rock_properties.porosity = 0.18

    # 7. Solvers and Execution Control
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
    sim.execution_control.darcy_linear_solver = pyfossil.DarcyLinearSolver.UMFPACK
    sim.execution_control.darcy_preconditioner = pyfossil.DarcyPreconditioner.NONE
    sim.execution_control.transport_linear_solver = pyfossil.TransportLinearSolver.GMRES
    sim.execution_control.transport_preconditioner = pyfossil.TransportPreconditioner.BLOCK_ILU

    # 8. Time Stepping (15,308 seconds)
    sim.time_data.final_time = 15308.0
    sim.time_data.darcy_time_step = 10.0
    sim.time_data.max_time_step = 1000.0

    # 9. Boundary Conditions
    bcs = sim.initial_and_boundary_conditions
    for name in ["Top", "Bottom", "Front", "Back"]:
        bcs[name].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
        bcs[name].darcy_boundary_value = 0.0
        bcs[name].trans_boundary_type = pyfossil.TransportBoundaryType.NO_FLOW

    # Prescribed injection on Left face (u = 1.41e-5 m/s, Sw = 0.55, Cs = 1.0 wt%)
    bcs["Left"].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
    bcs["Left"].darcy_boundary_value = 1.4111e-5
    bcs["Left"].trans_boundary_type = pyfossil.TransportBoundaryType.INFLOW_DIRICHLET
    bcs["Left"].trans_boundary_values[pyfossil.Variable.SW] = 0.55
    bcs["Left"].trans_boundary_values[pyfossil.Variable.CS] = 1.0

    # Atmospheric discharge on Right face
    bcs["Right"].darcy_boundary_type = pyfossil.DarcyBoundaryType.DIRICHLET
    bcs["Right"].darcy_boundary_value = 0.0
    bcs["Right"].trans_boundary_type = pyfossil.TransportBoundaryType.OUTFLOW

    return sim


if __name__ == "__main__":
    print("==================================================================")
    print(" FOSSIL Tutorial 5: Chen et al. (2010) Foam Simulation")
    print("==================================================================")

    model = build_chen_model()
    output_dir = "./output_Chen2010"
    simulator = pyfossil.FossilSimulator(model, output_dir)

    try:
        simulator.run()
        print("\n[SUCCESS] Simulation completed successfully!")
        print(f"Spatial field snapshots saved to: '{output_dir}/'")
        print("Run python plot.py to visualize spatial profiles.")
    except Exception as err:
        print(f"\n[SIMULATION ERROR]: {err}")
