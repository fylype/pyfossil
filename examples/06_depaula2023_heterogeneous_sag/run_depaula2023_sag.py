#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
TUTORIAL 6: Surfactant-Alternating-Gas (SAG) vs Coinjection
            (de Paula et al., 2023 - Heterogeneous SPE 10 Layer 36)
================================================================================

Replicates the research study published in de Paula et al. (2023) comparing
two foam-assisted Enhanced Oil Recovery (Foam EOR) strategies in a 2D highly
heterogeneous cross-section extracted from Layer 36 of SPE 10 Model 2:
1. Surfactant-Alternating-Gas (SAG) Injection:
   Alternating cycles where aqueous surfactant solution is injected first,
   followed by pure gas injection. Demonstrates the use of piecewise temporal
   schedules (`ConstantOrMap`) assigned directly via Python dictionaries!
2. Simultaneous Continuous Coinjection:
   Continuous coinjection of gas and liquid at the target volume fraction.

Physical and Numerical Highlights:
----------------------------------
- Heterogeneous Rock: Direct reading of the Layer 36 fine permeability map
  (`spe10_layer_36_rot90_perm.dat`, 220 x 60 cells).
- Piecewise Time Schedules on Boundaries:
  Transient boundary specification using `{t_0: val_0, t_1: val_1}` dictionaries.
- Adaptive Darcy Time Stepping:
  Velocity variation error control (`PAZ_VELOCITY`, Paz et al., 2021).
- Solvers:
  Conjugate Gradient (CG) + BoomerAMG and implicit JFNK with KNP scheme.

Authors: Filipe F. de Paula, Thiago Quinelato, Iury Igreja (UFLA)
================================================================================
"""

import os
import sys
from enum import Enum

# Attempt importing installed pyfossil; fallback to local build directory
try:
    import pyfossil
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_build = os.path.abspath(os.path.join(script_dir, "../../../build"))
    if local_build not in sys.path:
        sys.path.append(local_build)
    import pyfossil


class InjectionMode(Enum):
    SAG = 1         # Surfactant-Alternating-Gas (cyclical injection)
    COINJECTION = 2 # Simultaneous continuous coinjection


def build_model(mode: InjectionMode = InjectionMode.SAG,
                slug_duration: float = 4000.0,
                enable_foam: bool = True) -> pyfossil.SimulationData:
    """
    Constructs the simulation model for SPE 10 Layer 36.

    Parameters:
    -----------
    mode : InjectionMode
        SAG or COINJECTION.
    slug_duration : float
        For SAG: Surfactant cycle duration before switching to gas [s].
        For COINJECTION: Injected water saturation fraction (e.g., 0.20).
    enable_foam : bool
        Enables or disables Kovscek foam physics (for baseline comparisons).
    """
    sim = pyfossil.SimulationData()

    # 1. Layer 36 Geometry (3.67 m x 1.0 m pilot scale, 220 x 60 cells)
    sim.global_settings.mesh_type = pyfossil.MeshType.ORTHOGONAL_MESH
    sim.global_settings.dimension = 2

    sim.orthogonal_geometry.n_x = 220
    sim.orthogonal_geometry.n_y = 60
    sim.orthogonal_geometry.x_init = 0.0
    sim.orthogonal_geometry.x_final = 3.67
    sim.orthogonal_geometry.y_init = 0.0
    sim.orthogonal_geometry.y_final = 1.0
    sim.orthogonal_geometry.block_thickness = 0.01

    # 2. Fluid Thermodynamics
    sim.fluid_properties.water_viscosity = 1.0e-3
    sim.fluid_properties.water_density = 1000.0
    sim.fluid_properties.gas_viscosity = 1.8e-5
    sim.fluid_properties.gas_density = 1.165
    sim.fluid_properties.gas_compressibility = False

    # 3. Kovscek Foam Model
    if enable_foam:
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
        sim.eor_mechanisms.kovscek_model.XtMax = 0.0
        sim.eor_mechanisms.kovscek_model.const_trapping = True
        sim.eor_mechanisms.kovscek_model.refSurf = 0.083
    else:
        sim.physical_models.foam_model = pyfossil.FoamModel.NONE

    # 4. Rock and Interactions
    sim.rock_fluid_interactions.swc = 0.38
    sim.rock_fluid_interactions.sgr = 0.0
    sim.rock_fluid_interactions.sigma_wg = 0.033
    sim.rock_fluid_interactions.rel_perm_model = pyfossil.RelativePermeabilityModel.KOVSCEK_KR
    sim.rock_fluid_interactions.cap_pressure_model = pyfossil.CapillaryPressureModel.KOVSCEK_CP

    # 5. Initial Conditions
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.SW].constant_value = 1.0
    sim.initial_and_boundary_conditions.initial_state.initialization[pyfossil.Variable.CS].constant_value = 0.0

    # 6. Heterogeneous Permeability of Layer 36
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sim.rock_properties.perm_filename = os.path.join(script_dir, "spe10_layer_36_rot90_perm.dat")
    sim.rock_properties.porosity = 0.18
    sim.rock_properties.rock_regularization = False

    # 7. Solvers and Execution
    if enable_foam:
        sim.execution_control.variables = {
            pyfossil.Variable.SW,
            pyfossil.Variable.ND,
            pyfossil.Variable.CS
        }
        sim.execution_control.foam_behavior = pyfossil.FoamBehavior.LOCAL_EQUILIBRIUM
        sim.execution_control.surfactant_behavior = pyfossil.SurfactantBehavior.COMPUTED
    else:
        sim.execution_control.variables = {pyfossil.Variable.SW}
        sim.execution_control.foam_behavior = pyfossil.FoamBehavior.NONE
        sim.execution_control.surfactant_behavior = pyfossil.SurfactantBehavior.NONE

    sim.execution_control.abstol = 1.0e-6
    sim.execution_control.reltol = 1.0e-4
    sim.execution_control.bounds_check_at_reconstruction = True
    sim.execution_control.num_threads = 4
    sim.execution_control.num_method = pyfossil.NumericalMethod.KNP
    sim.execution_control.time_integrator = pyfossil.TimeIntegrator.BDF
    sim.execution_control.darcy_linear_solver = pyfossil.DarcyLinearSolver.CG
    sim.execution_control.darcy_preconditioner = pyfossil.DarcyPreconditioner.BOOMER_AMG
    sim.execution_control.transport_linear_solver = pyfossil.TransportLinearSolver.GMRES
    sim.execution_control.transport_preconditioner = pyfossil.TransportPreconditioner.BLOCK_ILU

    # Adaptive Darcy time stepping (Paz et al., 2021)
    sim.execution_control.darcy_extrapolation_degree = 0
    sim.execution_control.darcy_time_step_strategy = pyfossil.DarcyTimeStepStrategy.PAZ_VELOCITY

    # 8. Time Stepping (20,000 s total)
    sim.time_data.final_time = 20000.0
    sim.time_data.darcy_time_step = 10.0
    sim.time_data.max_time_step = 10000.0

    # 9. Transient Boundary Conditions
    bcs = sim.initial_and_boundary_conditions
    for name in ["Top", "Bottom"]:
        bcs[name].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
        bcs[name].darcy_boundary_value = 0.0
        bcs[name].trans_boundary_type = pyfossil.TransportBoundaryType.NO_FLOW

    # Influx on Left Face:
    bcs["Left"].darcy_boundary_type = pyfossil.DarcyBoundaryType.NEUMANN
    bcs["Left"].darcy_boundary_value = 1.446759e-5
    bcs["Left"].trans_boundary_type = pyfossil.TransportBoundaryType.INFLOW_NEUMANN_FW

    # DEMONSTRATION OF ConstantOrMap:
    if mode == InjectionMode.COINJECTION:
        # Continuous injection of water and surfactant
        bcs["Left"].trans_boundary_values[pyfossil.Variable.SW] = slug_duration
        bcs["Left"].trans_boundary_values[pyfossil.Variable.CS] = slug_duration
    elif mode == InjectionMode.SAG:
        # SAG Cycle: Begins with water + surfactant (Sw=1.0, Cs=1.0) until t = slug_duration,
        # then switches to gas injection (Sw=0.0, Cs=0.0):
        bcs["Left"].trans_boundary_values[pyfossil.Variable.SW] = {0.0: 1.0, slug_duration: 0.0}
        bcs["Left"].trans_boundary_values[pyfossil.Variable.CS] = {0.0: 1.0, slug_duration: 0.0}

    # Outflow on Right Face:
    bcs["Right"].darcy_boundary_type = pyfossil.DarcyBoundaryType.DIRICHLET
    bcs["Right"].darcy_boundary_value = 0.0
    bcs["Right"].trans_boundary_type = pyfossil.TransportBoundaryType.OUTFLOW

    # 10. Periodic VTU snapshots
    sim.output_control.output_mode = pyfossil.OutputMode.FIXED_TIMES
    sim.output_control.vtk_output_times = [
        0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 10000, 15000, 20000
    ]
    sim.output_control.write_vtk_volume = True
    sim.output_control.write_production_file = True

    return sim


if __name__ == "__main__":
    print("==================================================================")
    print(" FOSSIL Tutorial 6: de Paula et al. (2023) SAG Simulation")
    print("==================================================================")

    # Run SAG simulation with 4,000 s slug cycle
    model = build_model(mode=InjectionMode.SAG, slug_duration=4000.0, enable_foam=True)
    output_dir = "./output_dePaula2023_SAG_4000"
    simulator = pyfossil.FossilSimulator(model, output_dir)

    try:
        simulator.run()
        print("\n[SUCCESS] SAG simulation completed successfully!")
        print(f"VTU results and production files saved to: '{output_dir}/'")
    except Exception as err:
        print(f"\n[SIMULATION ERROR]: {err}")
