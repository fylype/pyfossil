# `pyfossil`

<div align="center">

**FOam diSplacement SImuLator — Python Interface**  
*High-Performance Multiphase & Foam Flow Simulation in Porous Media*

[![Python](https://img.shields.io/badge/Python-3.12--3.14-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20x86__64-orange.svg)](https://github.com/fylype/pyfossil)
[![Version](https://img.shields.io/badge/Release-v1.1.0-green.svg)](https://github.com/fylype/pyfossil/releases)
[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-blue.svg)](https://fylype.github.io/pyfossil/)
[![License](https://img.shields.io/badge/License-Non--Commercial%20Academic-red.svg)](LICENSE)

</div>

---

## 🌐 Official Documentation Website

Visit our full documentation portal hosted on GitHub Pages:  
👉 [**https://fylype.github.io/pyfossil/**](https://fylype.github.io/pyfossil/)

Includes:
- Complete **Python API Reference** with interactive search.
- Theoretical guide to **Solvers & Preconditioners** (H-MFE, JFNK, BoomerAMG, GAMG, UMFPACK).
- Step-by-step walkthroughs for all 7 simulation benchmarks.
- Publication-quality plotting guide with `FossilPlotter`.

---

## 📌 Overview

**`pyfossil`** is the high-performance Python interface to **FOSSIL** (**FO**am di**S**placement **S**ImuLator), an advanced scientific simulator designed for high-resolution multiphase flow, surfactant transport, and foam displacement in heterogeneous reservoir formations.

Built on top of leading numerical libraries (**deal.II**, **SUNDIALS**, **PETSc**, **HYPRE**, and **NLopt**), `pyfossil` combines:
- **C++17 High Performance**: Hybridized Mixed Finite Elements (H-MFE) and implicit multi-step time integration with OpenMP parallelization.
- **Python Usability**: Simple, declarative, scriptable API for setting up complex geometries, well trajectories, and operational schedules without compiling C++ code.

---

## 🚀 Key Numerical Features

- **Hybridized Mixed Finite Elements (H-MFE)**:
  - Solves Darcy flow for conservative flux fields and cell-centered pressure simultaneously.
  - Linear solvers: **CG**, **GMRES**, **BiCGStab**, **MINRES**, and **UMFPACK** (direct).
  - Advanced preconditioners: **PETSc GAMG** (Geometric-Algebraic Multigrid), **BoomerAMG** (HYPRE), **ICC**, and **ParaSails**.
  - Automatic constant nullspace closure for pure-Neumann problems.

- **Nonlinear Implicit Transport (JFNK)**:
  - **Jacobian-Free Newton-Krylov (JFNK)** integrated into SUNDIALS CVODE (BDF multi-step).
  - Central-Upwind finite volume schemes (**Kurganov-Noelle-Petrova / KNP** and **KPP**) with cubic extrema detection for non-convex fractional flows.
  - Linear Krylov solvers: SUNDIALS **GMRES**, **BiCGStab**, **TFQMR**, and PETSc KSP (**GMRES**, **BiCGStab**, **BCGSL**).
  - Preconditioners: **Block-ILU**, **Global-ILU**, and **BoomerAMG**.

- **Complex Geometries & Unstructured Meshes**:
  - Full support for 1D, 2D, and 3D domains.
  - Cartesian structured grids and unstructured Gmsh (`.msh`) meshes with material ID mappings.

- **Advanced Physical Models**:
  - Foam rheology and texture models (Ashoori et al., Chen et al., Kovscek et al., STARS, Zitha).
  - Peaceman well models with hydrostatic wellbore head, dynamic constraint switching (BHP $\leftrightarrow$ Rate), and real-time mechanical skin factor ($s$) adjustment with instant $WI^*$ re-indexing via pre-Darcy Python callbacks (`set_step_callback`).
  - Direct Python access to all constitutive models (`model_functions`) in physical SI units with 1D NumPy vectorization.
  - Directional petrophysical upscaling (Arithmetic, Harmonic, Geometric, Power-Law).

---

## 📦 Installation

`pyfossil` is distributed as a **standalone ManyLinux wheel** with all scientific dependencies (**deal.II, PETSc, HYPRE, SUNDIALS, NLopt, OpenBLAS, TBB**) pre-compiled and bundled inside the package. **No compilation or external library installation is required.**

### Prerequisites
- Operating System: **Linux x86_64** (Ubuntu 20.04+, Debian 11+, CentOS/RHEL 8+, Fedora 34+, Arch Linux, etc.)
- Python: **3.12, 3.13, or 3.14**
- Basic libraries:
  ```bash
  pip install numpy matplotlib
  ```

### Install from GitHub Releases
Download and install the pre-compiled standalone wheel matching your active Python version:

```bash
# Python 3.14 (Ubuntu 26.04 / Lubuntu 26.04 Rolling)
pip install https://github.com/fylype/pyfossil/releases/download/v1.1.0/pyfossil-1.1.0-cp314-cp314-manylinux_2_39_x86_64.whl

# Python 3.13
pip install https://github.com/fylype/pyfossil/releases/download/v1.1.0/pyfossil-1.1.0-cp313-cp313-manylinux_2_39_x86_64.whl

# Python 3.12 (Ubuntu 24.04 LTS / Windows WSL Ubuntu 24.04)
pip install https://github.com/fylype/pyfossil/releases/download/v1.1.0/pyfossil-1.1.0-cp312-cp312-manylinux_2_39_x86_64.whl
```

Or install from a locally downloaded wheel:
```bash
pip install pyfossil-1.1.0-*.whl
```

> **Tip for Lubuntu / Ubuntu 26.04 Users:**  
> Since Lubuntu defaults to Python 3.14, use the `cp314` wheel above. Alternatively, if you wish to run in a Python 3.12 environment on Lubuntu, create an isolated virtual environment:
> ```bash
> sudo apt install python3.12 python3.12-venv
> python3.12 -m venv ~/fossil_env && source ~/fossil_env/bin/activate
> pip install pyfossil-1.1.0-cp312-*.whl
> ```

To verify the installation:
```python
import pyfossil
print(f"pyfossil version: {pyfossil.__version__}")
```

---

## ⚡ Quick Start

```python
import pyfossil

# 1. Initialize simulation data
sim = pyfossil.SimulationData()

# 2. Configure 2D Cartesian mesh (50 x 20 cells)
sim.global_settings.dimension = 2
sim.global_settings.mesh_type = pyfossil.MeshType.ORTHOGONAL_MESH

sim.orthogonal_geometry.n_x = 50
sim.orthogonal_geometry.n_y = 20
sim.orthogonal_geometry.x_init, sim.orthogonal_geometry.x_final = 0.0, 100.0  # meters
sim.orthogonal_geometry.y_init, sim.orthogonal_geometry.y_final = 0.0, 20.0

# 3. Fluid and petrophysical properties
sim.rock_properties.porosity = 0.20
sim.rock_properties.perm_x = 100.0 * 9.86923e-16  # 100 mD in m^2
sim.rock_properties.perm_y = 100.0 * 9.86923e-16

# 4. Solvers & execution control
sim.execution_control.variables = {pyfossil.Variable.SW}
sim.execution_control.darcy_linear_solver = pyfossil.DarcyLinearSolver.CG
sim.execution_control.darcy_preconditioner = pyfossil.DarcyPreconditioner.BOOMER_AMG
sim.execution_control.transport_linear_solver = pyfossil.TransportLinearSolver.GMRES
sim.execution_control.transport_preconditioner = pyfossil.TransportPreconditioner.BLOCK_ILU

# 5. Boundary conditions: Injection on Left, Production on Right
bcs = sim.initial_and_boundary_conditions.orthogonal_boundaries
bcs.left.darcy_boundary_type = pyfossil.DarcyBoundaryType.DIRICHLET
bcs.left.darcy_boundary_value = 2.0e7  # 200 bar
bcs.left.trans_boundary_type = pyfossil.TransportBoundaryType.INFLOW_DIRICHLET
bcs.left.trans_boundary_values[pyfossil.Variable.SW] = 1.0
bcs.right.darcy_boundary_type = pyfossil.DarcyBoundaryType.DIRICHLET
bcs.right.darcy_boundary_value = 1.0e7  # 100 bar
bcs.right.trans_boundary_type = pyfossil.TransportBoundaryType.OUTFLOW

# 6. Run simulation
sim.time_data.final_time = 3600.0 * 24 * 30  # 30 days
simulator = pyfossil.FossilSimulator(sim, out_dir="./output_quickstart")
simulator.run()
```

---

## 📂 Repository Structure

```text
pyfossil/
├── mkdocs.yml                            # Configuration for GitHub Pages documentation site
├── pyfossil.pyi                          # Type stubs (IDE autocomplete & type checking)
├── plotter.py                            # FossilPlotter publication-grade visualization engine
├── docs/                                 # Documentation sources (Markdown + MathJax)
│   ├── index.md                          # Portal home
│   ├── installation.md                   # Standalone wheel installation guide
│   ├── python_api_reference.md           # Exhaustive API reference
│   ├── solvers_and_numerics.md           # H-MFE, JFNK, and preconditioners guide
│   ├── tutorials_guide.md                # Overview of the 7 tutorials
│   └── plotter_guide.md                  # Visualization engine manual
└── examples/
    ├── 01_ashoori_coreflood_1d/          # 1D coreflood foam displacement (Ashoori et al., 2011)
    ├── 02_unstructured_2d_materials/     # 2D unstructured Gmsh grid with hole & multi-materials
    ├── 03_unstructured_3d_hole/          # 3D tetrahedral unstructured grid with cavity & 7 BCs
    ├── 04_spe10_benchmark_3d/            # 3D SPE 10 Model 2 field reservoir with Peaceman wells
    ├── 05_chen2010_coreflood/            # 1D Berea coreflood with dynamic surfactant (Chen et al., 2010)
    ├── 06_depaula2023_heterogeneous_sag/ # 2D SAG injection in SPE 10 Layer 36 (de Paula et al., 2023)
    └── 07_structured_3d_hole/            # 3D structured curvilinear hexahedral mesh with perforation
```

---

## 📊 Plotting & Post-Processing

`pyfossil` includes [`plotter.py`](plotter.py) providing the `FossilPlotter` class for:
- Well production, BHP, and pressure-drop history curves (`production.dat`/`.csv`, `bhp.dat`/`.csv`, `pressure_drop.dat`/`.csv`).
- 1D spatial profiles of saturation ($S_w$), pressure, and foam texture ($n_D$).
- Clean 2D/3D PyVista spatial field renderings and standalone publication colorbars.

Example:
```python
from plotter import FossilPlotter

plotter = FossilPlotter(output_dir="./output_quickstart", dim=2)
plotter.plot_spatial_1d(
    target_variable="water_saturation",
    time_steps=[10, 50, 100],
    xlabel="Core Length [m]",
    ylabel="Water Saturation [-]",
    save_as="saturation_profiles.pdf"
)
```

---

## 📖 Citation

If you use `pyfossil` or `FOSSIL` in your scientific work or publications, please cite the underlying peer-reviewed papers:

```bibtex
@article{dePaula2024,
  author = {Filipe F. {de Paula} and Iury Igreja and Thiago O. Quinelato and Grigori Chapiro},
  title = {Numerical simulation of foam displacement impacted by kinetic and equilibrium surfactant adsorption},
  journal = {Advances in Water Resources},
  volume = {188},
  pages = {104690},
  year = {2024},
  doi = {10.1016/j.advwatres.2024.104690}
}

@article{dePaula2026,
  author = {Filipe F. {de Paula} and Iury Igreja and Grigori Chapiro},
  title = {Gas-dependent mobility control in foam-assisted injection: Comparative analysis of {CO}$_2$ and {N}$_2$ in heterogeneous reservoirs},
  journal = {Gas Science and Engineering},
  volume = {154},
  pages = {205968},
  year = {2026},
  doi = {10.1016/j.jgsce.2026.205968}
}

@article{dePaula2023,
  author = {Filipe F. {de Paula} and Iury Igreja and Thiago O. Quinelato and Grigori Chapiro},
  title = {A numerical investigation into the influence of the surfactant injection technique on the foam flow in heterogeneous porous media},
  journal = {Advances in Water Resources},
  volume = {171},
  pages = {104358},
  year = {2023},
  doi = {10.1016/j.advwatres.2022.104358}
}
```

---

## 📄 License

`pyfossil` is distributed under the **FOSSIL Non-Commercial Academic & Research License**.

- **Non-Commercial Academic Use:** Free for non-profit education, university degree theses, and academic scientific research.
- **Mandatory Attribution & Credit:** Any scientific publication, dissertation, conference presentation, or technical report using `pyfossil` must cite the author's peer-reviewed papers (`dePaula2024`, `dePaula2026`, `dePaula2023`) and acknowledge `pyfossil`.
- **Commercial Use Strictly Prohibited:** Direct or indirect use by commercial corporations, consulting firms, oil & gas operators, or paid engineering studies requires a separate written commercial license.
- **Proprietary & Closed-Source:** Reverse engineering, decompilation, and unauthorized commercial redistribution are strictly prohibited.

For complete legal terms, see the [LICENSE](LICENSE) file.

---

## 👥 Authors & Contact

- **Filipe F. de Paula** (filipe.paula@ufla.br) — *Lead Developer & Numerical Modeling*
- **Thiago Quinelato** — *High Performance Computing & Numerical Analysis*
- **Iury Igreja** — *Applied Mathematics & Fluid Dynamics*

Developed in collaboration with **Universidade Federal de Lavras (UFLA)**.
