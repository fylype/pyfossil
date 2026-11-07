# `pyfossil` Official Documentation (v1.0.0)

Welcome to the documentation for **`pyfossil`**, the high-performance Python interface to **FOSSIL** (**FO**am di**S**placement **S**ImuLator). FOSSIL is a state-of-the-art scientific simulation engine designed for multiphase fluid flow, reactive surfactant transport, and foam displacement in heterogeneous petroleum reservoirs and porous media.

---

## 🎯 Simulator Architecture

`pyfossil` provides the optimal combination of computational speed and modeling flexibility:

1. **C++17 High-Performance Core:**
   - **Darcy Flow Discretization:** Hybridized Mixed Finite Elements (**H-MFE**) with Raviart-Thomas ($RT_0$) velocity fields and Discontinuous Galerkin ($DG_0$) cell-centered pressure fields.
   - **Coupled Stiff Transport:** Fully implicit formulation using **Jacobian-Free Newton-Krylov (JFNK)** integrated with the **SUNDIALS CVODE** suite (variable-order, variable-step multi-step BDF methods).
   - **Modern Solvers & Preconditioners:** Krylov subspace solvers and algebraic multigrid preconditioners from **deal.II**, **PETSc**, **HYPRE BoomerAMG**, **PETSc GAMG**, and **SuiteSparse UMFPACK**.
   - **Parallel Acceleration:** Multi-threaded shared-memory parallelism using **OpenMP**.

2. **Python Scripting Usability:**
   - Declarative and intuitive configuration through the unified `SimulationData` container.
   - **Zero-copy NumPy array interoperability** for direct injection of heterogeneous petrophysical maps, initial state distributions, and PVT tables.
   - Native support for Cartesian structured meshes and 2D/3D unstructured **Gmsh** grids (`.msh`).
   - Dynamic real-time execution hooks (`set_step_callback`) for intelligent well controllers, physics-informed machine learning, and optimization algorithms.

---

## 📚 Documentation Contents

- [**Installation Guide**](installation.md): Step-by-step instructions for installing the pre-compiled ManyLinux standalone `.whl` package.
- [**Python API Reference**](python_api_reference.md): Detailed documentation of all configuration modules, data classes, enums, properties, and simulator methods.
- [**Solvers & Numerical Methods**](solvers_and_numerics.md): Theoretical and practical guide to selecting Darcy linear solvers, algebraic multigrid preconditioners, and JFNK transport schemes.
- [**Tutorials & Benchmarks**](tutorials_guide.md): Comprehensive walkthroughs of the 7 research benchmarks located in the `examples/` directory.
- [**Visualization Guide (`plotter.py`)**](plotter_guide.md): Automated post-processing, 1D spatial profile extraction, time-series history plots, and 2D/3D PyVista rendering.

---

## 💡 Quick Start Example

```python
import pyfossil

# 1. Instantiate the configuration container
sim = pyfossil.SimulationData()

# 2. Configure a 2D Cartesian mesh (40 x 20 cells, 100 m x 50 m)
sim.global_settings.dimension = 2
sim.global_settings.mesh_type = pyfossil.MeshType.ORTHOGONAL_MESH
sim.orthogonal_geometry.n_x = 40
sim.orthogonal_geometry.n_y = 20
sim.orthogonal_geometry.x_final = 100.0
sim.orthogonal_geometry.y_final = 50.0

# 3. Define petrophysical properties
sim.rock_properties.porosity = 0.20
sim.rock_properties.perm_x = 100.0 * 9.86923e-16 # 100 mD in m^2
sim.rock_properties.perm_y = 100.0 * 9.86923e-16

# 4. Configure solvers
sim.execution_control.darcy_linear_solver = pyfossil.DarcyLinearSolver.CG
sim.execution_control.darcy_preconditioner = pyfossil.DarcyPreconditioner.BOOMER_AMG
sim.execution_control.transport_linear_solver = pyfossil.TransportLinearSolver.GMRES
sim.execution_control.transport_preconditioner = pyfossil.TransportPreconditioner.BLOCK_ILU

# 5. Initialize and execute the simulation engine
simulator = pyfossil.FossilSimulator(sim, "./output_quickstart")
simulator.run()
```
