# Installation Guide

**`pyfossil`** is distributed as a pre-compiled, self-contained **ManyLinux Standalone Wheel** (`.whl`).

All high-performance scientific libraries (**deal.II, PETSc, HYPRE, SUNDIALS, SuiteSparse UMFPACK, OpenBLAS, and TBB**) are **bundled and linked internally** within the package. **No C++ compilation, CMake configuration, or manual library installations are required.**

---

## 💻 System Requirements

- **Operating System:** Linux `x86_64` with `glibc >= 2.39` (Ubuntu 24.04 LTS+, Debian 13+, Fedora 40+, Arch Linux, etc., matching the `manylinux_2_39_x86_64` tag).
- **Python:** Versions **3.12, 3.13, or 3.14** (64-bit).
- **System Runtime Prerequisites (Ubuntu / Debian):**  
  PETSc, HYPRE, deal.II, SUNDIALS 7.9, SuiteSparse, and OpenBLAS are already bundled inside `pyfossil.libs/` (no `libpetsc-real-dev`, `libdeal.ii-dev`, etc. required), but the wheel depends on the following system runtime libraries:
  ```bash
  sudo apt-get update && sudo apt-get install -y openmpi-bin libx11-6 libgomp1 zlib1g
  ```
  *(If `mpirun` is not needed, `openmpi-bin` can be replaced by `libopenmpi3t64` on Ubuntu 24.04.)*
- **Python Dependencies:** `numpy` (>= 1.20), `matplotlib` (>= 3.3), `pyvista`, and `pandas` (`pyvista` and `pandas` are required by `FossilPlotter` in `plotter.py`).
  ```bash
  pip install numpy matplotlib pyvista pandas
  ```
- **Optional Visualization Tool ([ParaView](https://www.paraview.org/)):** FOSSIL writes standard VTK volume/face files (`volume_vars_*.vtu` / `.pvd`). These can be inspected interactively in ParaView, making ParaView an **optional** visualization tool alongside `FossilPlotter`.

---

## 📦 Installation Methods

### Method 1: Direct Installation from GitHub Releases (Recommended)

You can install the wheel matching your Python version directly from the GitHub Releases page:

```bash
# For Python 3.14
pip install https://github.com/fylype/pyfossil/releases/download/v1.1.0/pyfossil-1.1.0-cp314-cp314-manylinux_2_39_x86_64.whl

# For Python 3.13
pip install https://github.com/fylype/pyfossil/releases/download/v1.1.0/pyfossil-1.1.0-cp313-cp313-manylinux_2_39_x86_64.whl

# For Python 3.12
pip install https://github.com/fylype/pyfossil/releases/download/v1.1.0/pyfossil-1.1.0-cp312-cp312-manylinux_2_39_x86_64.whl
```

---

### Method 2: Installing from a Local Wheel File

If you have downloaded the `.whl` file locally to your machine:

```bash
pip install pyfossil-1.1.0-*.whl
```

---

## ✅ Verifying Installation

Open a terminal and verify that `pyfossil` loads and initializes properly:

```bash
python3 -c "import pyfossil; print(f'pyfossil v{pyfossil.__version__} loaded successfully!'); sim = pyfossil.SimulationData(); print('SimulationData initialization OK!')"
```

Expected output:
```text
pyfossil v1.1.0 loaded successfully!
SimulationData initialization OK!
```

---

## 🛠️ Virtual Environment Setup (venv / conda)

Using an isolated virtual environment is recommended for your simulation workflows:

```bash
# Create a dedicated virtual environment
python3 -m venv ~/envs/fossil_env

# Activate the virtual environment
source ~/envs/fossil_env/bin/activate

# Upgrade pip and install visualization tools
pip install --upgrade pip
pip install numpy matplotlib pyvista pandas

# Install pyfossil
pip install pyfossil-1.1.0-*.whl
```
