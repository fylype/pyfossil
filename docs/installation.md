# Installation Guide

**`pyfossil`** is distributed as a pre-compiled, self-contained **ManyLinux Standalone Wheel** (`.whl`).

All high-performance scientific libraries (**deal.II, PETSc, HYPRE, SUNDIALS, NLopt, SuiteSparse UMFPACK, OpenBLAS, and TBB**) are **bundled and linked internally** within the package. **No C++ compilation, CMake configuration, or manual library installations are required.**

---

## 💻 System Requirements

- **Operating System:** Linux x86_64 (Ubuntu 20.04+, Debian 11+, CentOS/RHEL 8+, Fedora 34+, Arch Linux, etc.).
- **Python:** Versions 3.12 through 3.14 (64-bit).
- **Core Python Dependencies:** `numpy` (>= 1.20) and `matplotlib` (>= 3.3).

---

## 📦 Installation Methods

### Method 1: Direct Installation from GitHub Releases (Recommended)

You can install the wheel matching your Python version directly from the GitHub Releases page:

```bash
# For Python 3.14 (Ubuntu 26.04 / Lubuntu 26.04 Rolling)
pip install https://github.com/fylype/pyfossil/releases/download/v1.1.0/pyfossil-1.1.0-cp314-cp314-manylinux_2_39_x86_64.whl

# For Python 3.13
pip install https://github.com/fylype/pyfossil/releases/download/v1.1.0/pyfossil-1.1.0-cp313-cp313-manylinux_2_39_x86_64.whl

# For Python 3.12 (Ubuntu 24.04 LTS / Windows WSL Ubuntu 24.04)
pip install https://github.com/fylype/pyfossil/releases/download/v1.1.0/pyfossil-1.1.0-cp312-cp312-manylinux_2_39_x86_64.whl
```

> **Tip for Lubuntu / Ubuntu 26.04 Users:**  
> Since Lubuntu defaults to Python 3.14, install the `cp314` wheel above. Alternatively, if you wish to run in a Python 3.12 environment on Lubuntu, create an isolated virtual environment:
> ```bash
> sudo apt install python3.12 python3.12-venv
> python3.12 -m venv ~/fossil_env && source ~/fossil_env/bin/activate
> pip install pyfossil-1.1.0-cp312-*.whl
> ```

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
