# Solvers & Numerical Methods Guide

FOSSIL employs a high-order fractional-step (operator-splitting) scheme coupling Darcy hydrodynamics (pressure and velocity) with nonlinear multiphase transport (phase saturations and chemical species).

---

## 🌊 1. Darcy Flow: Hybridized Mixed Finite Elements (H-MFE)

The spatial discretization utilizes Raviart-Thomas ($RT_0$) vector elements for velocity and Discontinuous Galerkin ($DG_0$) scalar elements for cell-centered pressure.

Through **elemental static condensation** (Schur complement reduction), local cell velocities and cell pressures are eliminated analytically at the element level, reducing the indefinite saddle-point system to a sparse global linear system formulated **strictly for trace pressures on inter-element faces**:

$$H \boldsymbol{\Lambda} = \mathbf{R}$$

### 1.1 Mathematical Properties of the Darcy Matrix $H$:
- **Symmetric Positive-Definite (SPD):** Occurs when at least one Dirichlet pressure boundary condition is prescribed or at least one well operates under Bottom-Hole Pressure (BHP) control.
- **Symmetric Positive Semi-Definite (SPSD with Constant Nullspace):** Occurs when all domain boundaries are prescribed Darcy fluxes (pure Neumann) and all wells operate under rate control. FOSSIL automatically projects out the constant null eigenvector ($\mathbf{1}$), guaranteeing mathematical closure and unconditional iterative convergence.

---

### 1.2 Darcy Linear Solvers Catalog:

| Solver | Mathematical Property | Complexity | Practical Recommendation |
| :--- | :--- | :--- | :--- |
| **`CG`** (Conjugate Gradient) | Symmetric positive-definite | Optimal ($O(N)$ with AMG) | **Recommended for the majority of 2D and 3D reservoirs.** |
| **`MINRES`** (Minimal Residual) | Symmetric and indefinite/singular | $O(N)$ | **Recommended for pure Neumann problems without BHP wells.** |
| **`BiCGSTAB`** | Nonsymmetric or slightly indefinite | Robust | Excellent alternative for unstructured meshes with distorted elements. |
| **`GMRES`** | General asymmetric systems | Memory scales with restart size | Ideal for severe petrophysical anisotropy. |
| **`UMFPACK`** | Direct sparse $LU$ factorization | Exact, $O(N^{1.5})$ to $O(N^2)$ | **Recommended for 1D and moderate 2D meshes.** Eliminates iterative convergence tuning. |

---

### 1.3 Darcy Preconditioners:

| Preconditioner | Library | Mechanism | Recommended Use Case |
| :--- | :--- | :--- | :--- |
| **`BOOMER_AMG`** | HYPRE / PETSc | Classical Algebraic Multigrid with parallel coarsening | **Gold standard for large-scale 3D field models.** |
| **`GAMG`** | PETSc | Native Geometric-Algebraic Multigrid | High performance without external HYPRE dependency. |
| **`ICC`** | deal.II / PETSc | Incomplete Cholesky Factorization ($IC(0)$) | Structured 2D grids. |
| **`PARASAILS`** | HYPRE / PETSc | Parallel Sparse Approximate Inverse | Reservoirs where anisotropy degrades AMG coarsening. |
| **`NONE`** | - | No preconditioning | Used with direct UMFPACK or MINRES. |

---

## 🚀 2. Implicit Multiphase Transport: JFNK Formulation

The hyperbolic conservation laws governing water saturation ($S_w$), foam texture ($n_D$), and surfactant ($C_s$) exhibit strong flux nonlinearities and stiff kinetics requiring implicit multi-step time integration (**SUNDIALS CVODE BDF**).

### 2.1 What is JFNK (Jacobian-Free Newton-Krylov)?
In traditional matrix-based implicit methods, each Newton iteration requires assembling, allocating, and storing a massive coupled Jacobian matrix, consuming hundreds of gigabytes of RAM on fine 3D grids.

In **JFNK**, the Krylov subspace solver (GMRES or BiCGStab) **never forms the Jacobian matrix explicitly**. Instead, it evaluates the action of the Jacobian on a search direction $\mathbf{v}$ via a finite-difference directional derivative:

$$J(\mathbf{u}) \mathbf{v} \approx \frac{F(\mathbf{u} + \epsilon \mathbf{v}) - F(\mathbf{u})}{\epsilon}$$

where $\epsilon$ is an optimal perturbation parameter computed dynamically from integrator error tolerances.

### 2.2 Preconditioning in JFNK
To accelerate Krylov convergence while maintaining the memory advantages of matrix-free evaluation, FOSSIL implements **right preconditioning**:

$$[J P^{-1}] (P \mathbf{v}) = -F(\mathbf{u})$$

where $P$ is a sparse coupling matrix:
- **`BLOCK_ILU` (Default & Recommended):** Inverts local block matrices coupling the conservation variables within each single cell (e.g., $S_w, n_D, C_s$). Negligible memory footprint and excellent convergence acceleration.
- **`GLOBAL_ILU`:** Couples inter-element advective fluxes across the full mesh; ideal for large CFL numbers.
- **`BOOMER_AMG`:** Applies algebraic multigrid preconditioning to the transport system.
- **`NONE`:** Pure matrix-free Krylov iteration without preconditioning (ideal for small time steps).
