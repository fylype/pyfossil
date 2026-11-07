"""Python programmatic interface for the FOSSIL reservoir simulator"""

from collections.abc import (
    Callable,
    Iterator,
    Mapping,
    Sequence,
    Set
)
from typing import Final, overload


__version_info__: tuple = (1, 0, 0, '-rc.1')

class VariableMap:
    @overload
    def __init__(self) -> None:
        """Default constructor"""

    @overload
    def __init__(self, arg: VariableMap, /) -> None:
        """Copy constructor"""

    @overload
    def __init__(self, arg: dict[Enum_Variable, ConstantOrMap_Double_Double], /) -> None:
        """Construct from a dictionary"""

    def __len__(self) -> int: ...

    def __bool__(self) -> bool:
        """Check whether the map is nonempty"""

    def __repr__(self) -> str: ...

    @overload
    def __contains__(self, arg: Enum_Variable, /) -> bool: ...

    @overload
    def __contains__(self, arg: object, /) -> bool: ...

    def __iter__(self) -> Iterator[Enum_Variable]: ...

    def __getitem__(self, arg: Enum_Variable, /) -> ConstantOrMap_Double_Double: ...

    def __delitem__(self, arg: Enum_Variable, /) -> None: ...

    def clear(self) -> None:
        """Remove all items"""

    def __setitem__(self, arg0: Enum_Variable, arg1: ConstantOrMap_Double_Double, /) -> None: ...

    def update(self, arg: VariableMap, /) -> None:
        """Update the map with element from ``arg``"""

    class ItemView:
        def __len__(self) -> int: ...

        def __iter__(self) -> Iterator[tuple[Enum_Variable, ConstantOrMap_Double_Double]]: ...

    class KeyView:
        @overload
        def __contains__(self, arg: Enum_Variable, /) -> bool: ...

        @overload
        def __contains__(self, arg: object, /) -> bool: ...

        def __len__(self) -> int: ...

        def __iter__(self) -> Iterator[Enum_Variable]: ...

    class ValueView:
        def __len__(self) -> int: ...

        def __iter__(self) -> Iterator[ConstantOrMap_Double_Double]: ...

    def keys(self) -> VariableMap.KeyView:
        """Returns an iterable view of the map's keys."""

    def values(self) -> VariableMap.ValueView:
        """Returns an iterable view of the map's values."""

    def items(self) -> VariableMap.ItemView:
        """Returns an iterable view of the map's items."""

class Enum_MeshType:
    def __init__(self, arg: Enum_MeshType, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_MeshType, /) -> bool: ...

    def __hash__(self) -> int: ...

class MeshType:
    ORTHOGONAL_MESH: Final[Enum_MeshType] = ...
    """(arg: object, /) -> pyfossil.Enum_MeshType"""

    UNSTRUCTURED_MESH: Final[Enum_MeshType] = ...
    """(arg: object, /) -> pyfossil.Enum_MeshType"""

class Enum_DarcyLinearSolver:
    def __init__(self, arg: Enum_DarcyLinearSolver, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_DarcyLinearSolver, /) -> bool: ...

    def __hash__(self) -> int: ...

class DarcyLinearSolver:
    UMFPACK: Final[Enum_DarcyLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyLinearSolver"""

    GMRES: Final[Enum_DarcyLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyLinearSolver"""

    FGMRES: Final[Enum_DarcyLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyLinearSolver"""

    CG: Final[Enum_DarcyLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyLinearSolver"""

    BiCGSTAB: Final[Enum_DarcyLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyLinearSolver"""

    MINRES: Final[Enum_DarcyLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyLinearSolver"""

class Enum_DarcyTimeStepStrategy:
    def __init__(self, arg: Enum_DarcyTimeStepStrategy, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_DarcyTimeStepStrategy, /) -> bool: ...

    def __hash__(self) -> int: ...

class DarcyTimeStepStrategy:
    NONE: Final[Enum_DarcyTimeStepStrategy] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyTimeStepStrategy"""

    PAZ_VELOCITY: Final[Enum_DarcyTimeStepStrategy] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyTimeStepStrategy"""

    SW_VARIATION: Final[Enum_DarcyTimeStepStrategy] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyTimeStepStrategy"""

class Enum_DarcyPreconditioner:
    def __init__(self, arg: Enum_DarcyPreconditioner, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_DarcyPreconditioner, /) -> bool: ...

    def __hash__(self) -> int: ...

class DarcyPreconditioner:
    NONE: Final[Enum_DarcyPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyPreconditioner"""

    SSOR: Final[Enum_DarcyPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyPreconditioner"""

    JACOBI: Final[Enum_DarcyPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyPreconditioner"""

    BOOMER_AMG: Final[Enum_DarcyPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyPreconditioner"""

    ILU: Final[Enum_DarcyPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyPreconditioner"""

    ICC: Final[Enum_DarcyPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyPreconditioner"""

    GAMG: Final[Enum_DarcyPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyPreconditioner"""

    PARASAILS: Final[Enum_DarcyPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyPreconditioner"""

class Enum_GasStateEquationModel:
    def __init__(self, arg: Enum_GasStateEquationModel, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_GasStateEquationModel, /) -> bool: ...

    def __hash__(self) -> int: ...

class GasStateEquationModel:
    LINEAR: Final[Enum_GasStateEquationModel] = ...
    """(arg: object, /) -> pyfossil.Enum_GasStateEquationModel"""

    EXPONENTIAL: Final[Enum_GasStateEquationModel] = ...
    """(arg: object, /) -> pyfossil.Enum_GasStateEquationModel"""

    IDEAL_GAS: Final[Enum_GasStateEquationModel] = ...
    """(arg: object, /) -> pyfossil.Enum_GasStateEquationModel"""

    IDEAL_GAS_SIMPLIFIED: Final[Enum_GasStateEquationModel] = ...
    """(arg: object, /) -> pyfossil.Enum_GasStateEquationModel"""

    DENSITY_TABLE: Final[Enum_GasStateEquationModel] = ...
    """(arg: object, /) -> pyfossil.Enum_GasStateEquationModel"""

class Enum_CompIncomp:
    def __init__(self, arg: Enum_CompIncomp, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_CompIncomp, /) -> bool: ...

    def __hash__(self) -> int: ...

class CompIncomp:
    COMPRESSIBLE: Final[Enum_CompIncomp] = ...
    """(arg: object, /) -> pyfossil.Enum_CompIncomp"""

    INCOMPRESSIBLE: Final[Enum_CompIncomp] = ...
    """(arg: object, /) -> pyfossil.Enum_CompIncomp"""

class Enum_NumericalMethod:
    def __init__(self, arg: Enum_NumericalMethod, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_NumericalMethod, /) -> bool: ...

    def __hash__(self) -> int: ...

class NumericalMethod:
    UPWIND: Final[Enum_NumericalMethod] = ...
    """(arg: object, /) -> pyfossil.Enum_NumericalMethod"""

    KNP: Final[Enum_NumericalMethod] = ...
    """(arg: object, /) -> pyfossil.Enum_NumericalMethod"""

    KPP: Final[Enum_NumericalMethod] = ...
    """(arg: object, /) -> pyfossil.Enum_NumericalMethod"""

    KT: Final[Enum_NumericalMethod] = ...
    """(arg: object, /) -> pyfossil.Enum_NumericalMethod"""

class Enum_TimeIntegrator:
    def __init__(self, arg: Enum_TimeIntegrator, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_TimeIntegrator, /) -> bool: ...

    def __hash__(self) -> int: ...

class TimeIntegrator:
    BDF: Final[Enum_TimeIntegrator] = ...
    """(arg: object, /) -> pyfossil.Enum_TimeIntegrator"""

    ERK: Final[Enum_TimeIntegrator] = ...
    """(arg: object, /) -> pyfossil.Enum_TimeIntegrator"""

    IDA: Final[Enum_TimeIntegrator] = ...
    """(arg: object, /) -> pyfossil.Enum_TimeIntegrator"""

class Enum_NonlinearSolver:
    def __init__(self, arg: Enum_NonlinearSolver, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_NonlinearSolver, /) -> bool: ...

    def __hash__(self) -> int: ...

class NonlinearSolver:
    NEWTON: Final[Enum_NonlinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_NonlinearSolver"""

    FIXED_POINT: Final[Enum_NonlinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_NonlinearSolver"""

    AUTO: Final[Enum_NonlinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_NonlinearSolver"""

class Enum_TransportLinearSolver:
    def __init__(self, arg: Enum_TransportLinearSolver, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_TransportLinearSolver, /) -> bool: ...

    def __hash__(self) -> int: ...

class TransportLinearSolver:
    GMRES: Final[Enum_TransportLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportLinearSolver"""

    FGMRES: Final[Enum_TransportLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportLinearSolver"""

    BICGSTAB: Final[Enum_TransportLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportLinearSolver"""

    TFQMR: Final[Enum_TransportLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportLinearSolver"""

    GMRES_PETSC: Final[Enum_TransportLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportLinearSolver"""

    FGMRES_PETSC: Final[Enum_TransportLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportLinearSolver"""

    BICGSTAB_PETSC: Final[Enum_TransportLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportLinearSolver"""

    TFQMR_PETSC: Final[Enum_TransportLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportLinearSolver"""

    BCGSL_PETSC: Final[Enum_TransportLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportLinearSolver"""

    BCGSL: Final[Enum_TransportLinearSolver] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportLinearSolver"""

class Enum_TransportPreconditioner:
    def __init__(self, arg: Enum_TransportPreconditioner, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_TransportPreconditioner, /) -> bool: ...

    def __hash__(self) -> int: ...

class TransportPreconditioner:
    NONE: Final[Enum_TransportPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportPreconditioner"""

    BLOCK_ILU: Final[Enum_TransportPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportPreconditioner"""

    GLOBAL_ILU: Final[Enum_TransportPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportPreconditioner"""

    BOOMER_AMG: Final[Enum_TransportPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportPreconditioner"""

    PARASAILS: Final[Enum_TransportPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportPreconditioner"""

    JACOBI: Final[Enum_TransportPreconditioner] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportPreconditioner"""

class Enum_CapillaryPressureModel:
    def __init__(self, arg: Enum_CapillaryPressureModel, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_CapillaryPressureModel, /) -> bool: ...

    def __hash__(self) -> int: ...

class CapillaryPressureModel:
    KOVSCEK_CP: Final[Enum_CapillaryPressureModel] = ...
    """(arg: object, /) -> pyfossil.Enum_CapillaryPressureModel"""

    ASHOORI_CP: Final[Enum_CapillaryPressureModel] = ...
    """(arg: object, /) -> pyfossil.Enum_CapillaryPressureModel"""

    ZITHA_CP: Final[Enum_CapillaryPressureModel] = ...
    """(arg: object, /) -> pyfossil.Enum_CapillaryPressureModel"""

    LEVERETT_J: Final[Enum_CapillaryPressureModel] = ...
    """(arg: object, /) -> pyfossil.Enum_CapillaryPressureModel"""

    TABLE_CP: Final[Enum_CapillaryPressureModel] = ...
    """(arg: object, /) -> pyfossil.Enum_CapillaryPressureModel"""

    NONE_CP: Final[Enum_CapillaryPressureModel] = ...
    """(arg: object, /) -> pyfossil.Enum_CapillaryPressureModel"""

class Enum_RelativePermeabilityModel:
    def __init__(self, arg: Enum_RelativePermeabilityModel, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_RelativePermeabilityModel, /) -> bool: ...

    def __hash__(self) -> int: ...

class RelativePermeabilityModel:
    KOVSCEK_KR: Final[Enum_RelativePermeabilityModel] = ...
    """(arg: object, /) -> pyfossil.Enum_RelativePermeabilityModel"""

    ASHOORI_KR: Final[Enum_RelativePermeabilityModel] = ...
    """(arg: object, /) -> pyfossil.Enum_RelativePermeabilityModel"""

    ZITHA_KR: Final[Enum_RelativePermeabilityModel] = ...
    """(arg: object, /) -> pyfossil.Enum_RelativePermeabilityModel"""

    COREY_BROOKS_KR: Final[Enum_RelativePermeabilityModel] = ...
    """(arg: object, /) -> pyfossil.Enum_RelativePermeabilityModel"""

    CUSTOM_KR: Final[Enum_RelativePermeabilityModel] = ...
    """(arg: object, /) -> pyfossil.Enum_RelativePermeabilityModel"""

    TABLE_KR: Final[Enum_RelativePermeabilityModel] = ...
    """(arg: object, /) -> pyfossil.Enum_RelativePermeabilityModel"""

class Enum_FoamModel:
    def __init__(self, arg: Enum_FoamModel, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_FoamModel, /) -> bool: ...

    def __hash__(self) -> int: ...

class FoamModel:
    KOVSCEK: Final[Enum_FoamModel] = ...
    """(arg: object, /) -> pyfossil.Enum_FoamModel"""

    ASHOORI: Final[Enum_FoamModel] = ...
    """(arg: object, /) -> pyfossil.Enum_FoamModel"""

    ZITHA: Final[Enum_FoamModel] = ...
    """(arg: object, /) -> pyfossil.Enum_FoamModel"""

    STARS: Final[Enum_FoamModel] = ...
    """(arg: object, /) -> pyfossil.Enum_FoamModel"""

    LAMAP: Final[Enum_FoamModel] = ...
    """(arg: object, /) -> pyfossil.Enum_FoamModel"""

    NONE: Final[Enum_FoamModel] = ...
    """(arg: object, /) -> pyfossil.Enum_FoamModel"""

class Enum_DarcyBoundaryType:
    def __init__(self, arg: Enum_DarcyBoundaryType, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_DarcyBoundaryType, /) -> bool: ...

    def __hash__(self) -> int: ...

class DarcyBoundaryType:
    DIRICHLET: Final[Enum_DarcyBoundaryType] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyBoundaryType"""

    NEUMANN: Final[Enum_DarcyBoundaryType] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyBoundaryType"""

    DIRICHLET_COMPUTED: Final[Enum_DarcyBoundaryType] = ...
    """(arg: object, /) -> pyfossil.Enum_DarcyBoundaryType"""

class Enum_TransportBoundaryType:
    def __init__(self, arg: Enum_TransportBoundaryType, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_TransportBoundaryType, /) -> bool: ...

    def __hash__(self) -> int: ...

class TransportBoundaryType:
    INFLOW_NEUMANN: Final[Enum_TransportBoundaryType] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportBoundaryType"""

    INFLOW_NEUMANN_FW: Final[Enum_TransportBoundaryType] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportBoundaryType"""

    INFLOW_DIRICHLET: Final[Enum_TransportBoundaryType] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportBoundaryType"""

    OUTFLOW: Final[Enum_TransportBoundaryType] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportBoundaryType"""

    NO_FLOW: Final[Enum_TransportBoundaryType] = ...
    """(arg: object, /) -> pyfossil.Enum_TransportBoundaryType"""

class Enum_Variable:
    def __init__(self, arg: Enum_Variable, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_Variable, /) -> bool: ...

    def __hash__(self) -> int: ...

class Variable:
    SW: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

    ND: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

    CS: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

    CA_EQ: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

    CA_KIN: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

    PERMX: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

    PERMY: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

    PERMZ: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

    POR: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

    VISC: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

    RHO_G: Final[Enum_Variable] = ...
    """(arg: object, /) -> pyfossil.Enum_Variable"""

class Enum_WellType:
    def __init__(self, arg: Enum_WellType, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_WellType, /) -> bool: ...

    def __hash__(self) -> int: ...

class WellType:
    PRODUCER: Final[Enum_WellType] = ...
    """(arg: object, /) -> pyfossil.Enum_WellType"""

    INJECTOR: Final[Enum_WellType] = ...
    """(arg: object, /) -> pyfossil.Enum_WellType"""

class Enum_WellConstraintType:
    def __init__(self, arg: Enum_WellConstraintType, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_WellConstraintType, /) -> bool: ...

    def __hash__(self) -> int: ...

class WellConstraintType:
    BHP: Final[Enum_WellConstraintType] = ...
    """(arg: object, /) -> pyfossil.Enum_WellConstraintType"""

    FLOW_RATE: Final[Enum_WellConstraintType] = ...
    """(arg: object, /) -> pyfossil.Enum_WellConstraintType"""

class Enum_WellOperation:
    def __init__(self, arg: Enum_WellOperation, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_WellOperation, /) -> bool: ...

    def __hash__(self) -> int: ...

class WellOperation:
    SHUT_IN: Final[Enum_WellOperation] = ...
    """(arg: object, /) -> pyfossil.Enum_WellOperation"""

    OPEN: Final[Enum_WellOperation] = ...
    """(arg: object, /) -> pyfossil.Enum_WellOperation"""

class Enum_AdsorptionBehavior:
    def __init__(self, arg: Enum_AdsorptionBehavior, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_AdsorptionBehavior, /) -> bool: ...

    def __hash__(self) -> int: ...

class AdsorptionBehavior:
    NONE: Final[Enum_AdsorptionBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_AdsorptionBehavior"""

    EQUILIBRIUM: Final[Enum_AdsorptionBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_AdsorptionBehavior"""

    KINETIC: Final[Enum_AdsorptionBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_AdsorptionBehavior"""

    MIXED: Final[Enum_AdsorptionBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_AdsorptionBehavior"""

class Enum_EquilibriumAdsorptionModel:
    def __init__(self, arg: Enum_EquilibriumAdsorptionModel, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_EquilibriumAdsorptionModel, /) -> bool: ...

    def __hash__(self) -> int: ...

class EquilibriumAdsorptionModel:
    NONE: Final[Enum_EquilibriumAdsorptionModel] = ...
    """(arg: object, /) -> pyfossil.Enum_EquilibriumAdsorptionModel"""

    LINEAR: Final[Enum_EquilibriumAdsorptionModel] = ...
    """(arg: object, /) -> pyfossil.Enum_EquilibriumAdsorptionModel"""

    LANGMUIR: Final[Enum_EquilibriumAdsorptionModel] = ...
    """(arg: object, /) -> pyfossil.Enum_EquilibriumAdsorptionModel"""

    SIPS: Final[Enum_EquilibriumAdsorptionModel] = ...
    """(arg: object, /) -> pyfossil.Enum_EquilibriumAdsorptionModel"""

class Enum_KineticAdsorptionModel:
    def __init__(self, arg: Enum_KineticAdsorptionModel, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_KineticAdsorptionModel, /) -> bool: ...

    def __hash__(self) -> int: ...

class KineticAdsorptionModel:
    NONE: Final[Enum_KineticAdsorptionModel] = ...
    """(arg: object, /) -> pyfossil.Enum_KineticAdsorptionModel"""

    LINEAR: Final[Enum_KineticAdsorptionModel] = ...
    """(arg: object, /) -> pyfossil.Enum_KineticAdsorptionModel"""

    LANGMUIR: Final[Enum_KineticAdsorptionModel] = ...
    """(arg: object, /) -> pyfossil.Enum_KineticAdsorptionModel"""

    SIPS: Final[Enum_KineticAdsorptionModel] = ...
    """(arg: object, /) -> pyfossil.Enum_KineticAdsorptionModel"""

    PSEUDO_FIRST_ORDER: Final[Enum_KineticAdsorptionModel] = ...
    """(arg: object, /) -> pyfossil.Enum_KineticAdsorptionModel"""

    PSEUDO_SECOND_ORDER: Final[Enum_KineticAdsorptionModel] = ...
    """(arg: object, /) -> pyfossil.Enum_KineticAdsorptionModel"""

class Enum_FoamBehavior:
    def __init__(self, arg: Enum_FoamBehavior, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_FoamBehavior, /) -> bool: ...

    def __hash__(self) -> int: ...

class FoamBehavior:
    LOCAL_EQUILIBRIUM: Final[Enum_FoamBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_FoamBehavior"""

    FIXED: Final[Enum_FoamBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_FoamBehavior"""

    COMPUTED: Final[Enum_FoamBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_FoamBehavior"""

    NONE: Final[Enum_FoamBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_FoamBehavior"""

class Enum_SurfactantBehavior:
    def __init__(self, arg: Enum_SurfactantBehavior, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_SurfactantBehavior, /) -> bool: ...

    def __hash__(self) -> int: ...

class SurfactantBehavior:
    NONE: Final[Enum_SurfactantBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_SurfactantBehavior"""

    FIXED: Final[Enum_SurfactantBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_SurfactantBehavior"""

    COMPUTED: Final[Enum_SurfactantBehavior] = ...
    """(arg: object, /) -> pyfossil.Enum_SurfactantBehavior"""

class Enum_NonConvexFluxStrategy:
    def __init__(self, arg: Enum_NonConvexFluxStrategy, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_NonConvexFluxStrategy, /) -> bool: ...

    def __hash__(self) -> int: ...

class NonConvexFluxStrategy:
    NONE: Final[Enum_NonConvexFluxStrategy] = ...
    """(arg: object, /) -> pyfossil.Enum_NonConvexFluxStrategy"""

    BRUTE_FORCE: Final[Enum_NonConvexFluxStrategy] = ...
    """(arg: object, /) -> pyfossil.Enum_NonConvexFluxStrategy"""

    NLOPT_OPTIMIZATION: Final[Enum_NonConvexFluxStrategy] = ...
    """(arg: object, /) -> pyfossil.Enum_NonConvexFluxStrategy"""

    STEEPEST_DESCENT: Final[Enum_NonConvexFluxStrategy] = ...
    """(arg: object, /) -> pyfossil.Enum_NonConvexFluxStrategy"""

class Enum_OutputMode:
    def __init__(self, arg: Enum_OutputMode, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_OutputMode, /) -> bool: ...

    def __hash__(self) -> int: ...

class OutputMode:
    PERCENT_INTERVAL: Final[Enum_OutputMode] = ...
    """(arg: object, /) -> pyfossil.Enum_OutputMode"""

    FIXED_TIMES: Final[Enum_OutputMode] = ...
    """(arg: object, /) -> pyfossil.Enum_OutputMode"""

class Enum_InitializationType:
    def __init__(self, arg: Enum_InitializationType, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_InitializationType, /) -> bool: ...

    def __hash__(self) -> int: ...

class InitializationType:
    CONSTANT: Final[Enum_InitializationType] = ...
    """(arg: object, /) -> pyfossil.Enum_InitializationType"""

    FILE: Final[Enum_InitializationType] = ...
    """(arg: object, /) -> pyfossil.Enum_InitializationType"""

class Enum_UpscalingMethod:
    def __init__(self, arg: Enum_UpscalingMethod, /) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...

    def __eq__(self, arg: Enum_UpscalingMethod, /) -> bool: ...

    def __hash__(self) -> int: ...

class UpscalingMethod:
    ARITHMETIC: Final[Enum_UpscalingMethod] = ...
    """(arg: object, /) -> pyfossil.Enum_UpscalingMethod"""

    HARMONIC: Final[Enum_UpscalingMethod] = ...
    """(arg: object, /) -> pyfossil.Enum_UpscalingMethod"""

    GEOMETRIC: Final[Enum_UpscalingMethod] = ...
    """(arg: object, /) -> pyfossil.Enum_UpscalingMethod"""

    POWER_LAW: Final[Enum_UpscalingMethod] = ...
    """(arg: object, /) -> pyfossil.Enum_UpscalingMethod"""

class ConstantOrMap_Double_Double:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, constant_value: float) -> None:
        """Cria um mapa com valor fixo e constante."""

    @overload
    def __init__(self, data_map: Mapping[float, float]) -> None:
        """Cria um mapa variável a partir de um dicionário nativo."""

    @overload
    def __init__(self, prm_string: str) -> None:
        """Cria o mapa a partir da sintaxe string do .prm."""

    def is_constant(self) -> bool:
        """Retorna se o objeto é um valor constante."""

    @overload
    def get_value(self, key: float) -> float:
        """Retorna o valor agendado no tempo/chave especificado."""

    @overload
    def get_value(self) -> float:
        """Retorna o valor agendado no tempo/chave ativo."""

    def at(self, key: float) -> float:
        """Retorna o valor agendado no tempo/chave especificado."""

    def __call__(self, key: float) -> float:
        """Permite chamar o objeto diretamente como com(t)."""

    def __len__(self) -> int: ...

    @overload
    def __eq__(self, arg: float, /) -> bool: ...

    @overload
    def __eq__(self, arg: ConstantOrMap_Double_Double, /) -> bool: ...

    @overload
    def __ne__(self, arg: float, /) -> bool: ...

    @overload
    def __ne__(self, arg: ConstantOrMap_Double_Double, /) -> bool: ...

    def __repr__(self) -> str: ...

class ConstantOrMap_Variable_Double:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, constant_value: float) -> None:
        """Cria um mapa com valor fixo e constante."""

    @overload
    def __init__(self, data_map: Mapping[Enum_Variable, float]) -> None:
        """Cria um mapa variável a partir de um dicionário nativo."""

    @overload
    def __init__(self, prm_string: str) -> None:
        """Cria o mapa a partir da sintaxe string do .prm."""

    def is_constant(self) -> bool:
        """Retorna se o objeto é um valor constante."""

    @overload
    def get_value(self, key: Enum_Variable) -> float:
        """Retorna o valor agendado no tempo/chave especificado."""

    @overload
    def get_value(self) -> float:
        """Retorna o valor agendado no tempo/chave ativo."""

    def at(self, key: Enum_Variable) -> float:
        """Retorna o valor agendado no tempo/chave especificado."""

    def __call__(self, key: Enum_Variable) -> float:
        """Permite chamar o objeto diretamente como com(t)."""

    def __len__(self) -> int: ...

    @overload
    def __eq__(self, arg: float, /) -> bool: ...

    @overload
    def __eq__(self, arg: ConstantOrMap_Variable_Double, /) -> bool: ...

    @overload
    def __ne__(self, arg: float, /) -> bool: ...

    @overload
    def __ne__(self, arg: ConstantOrMap_Variable_Double, /) -> bool: ...

    def __repr__(self) -> str: ...

class ConstantOrMap_Double_DarcyBoundary:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, constant_value: Enum_DarcyBoundaryType) -> None:
        """Cria um mapa com valor fixo e constante."""

    @overload
    def __init__(self, data_map: Mapping[float, Enum_DarcyBoundaryType]) -> None:
        """Cria um mapa variável a partir de um dicionário nativo."""

    @overload
    def __init__(self, prm_string: str) -> None:
        """Cria o mapa a partir da sintaxe string do .prm."""

    def is_constant(self) -> bool:
        """Retorna se o objeto é um valor constante."""

    @overload
    def get_value(self, key: float) -> Enum_DarcyBoundaryType:
        """Retorna o valor agendado no tempo/chave especificado."""

    @overload
    def get_value(self) -> Enum_DarcyBoundaryType:
        """Retorna o valor agendado no tempo/chave ativo."""

    def at(self, key: float) -> Enum_DarcyBoundaryType:
        """Retorna o valor agendado no tempo/chave especificado."""

    def __call__(self, key: float) -> Enum_DarcyBoundaryType:
        """Permite chamar o objeto diretamente como com(t)."""

    def __len__(self) -> int: ...

    @overload
    def __eq__(self, arg: Enum_DarcyBoundaryType, /) -> bool: ...

    @overload
    def __eq__(self, arg: ConstantOrMap_Double_DarcyBoundary, /) -> bool: ...

    @overload
    def __ne__(self, arg: Enum_DarcyBoundaryType, /) -> bool: ...

    @overload
    def __ne__(self, arg: ConstantOrMap_Double_DarcyBoundary, /) -> bool: ...

    def __repr__(self) -> str: ...

class ConstantOrMap_Double_TransBoundary:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, constant_value: Enum_TransportBoundaryType) -> None:
        """Cria um mapa com valor fixo e constante."""

    @overload
    def __init__(self, data_map: Mapping[float, Enum_TransportBoundaryType]) -> None:
        """Cria um mapa variável a partir de um dicionário nativo."""

    @overload
    def __init__(self, prm_string: str) -> None:
        """Cria o mapa a partir da sintaxe string do .prm."""

    def is_constant(self) -> bool:
        """Retorna se o objeto é um valor constante."""

    @overload
    def get_value(self, key: float) -> Enum_TransportBoundaryType:
        """Retorna o valor agendado no tempo/chave especificado."""

    @overload
    def get_value(self) -> Enum_TransportBoundaryType:
        """Retorna o valor agendado no tempo/chave ativo."""

    def at(self, key: float) -> Enum_TransportBoundaryType:
        """Retorna o valor agendado no tempo/chave especificado."""

    def __call__(self, key: float) -> Enum_TransportBoundaryType:
        """Permite chamar o objeto diretamente como com(t)."""

    def __len__(self) -> int: ...

    @overload
    def __eq__(self, arg: Enum_TransportBoundaryType, /) -> bool: ...

    @overload
    def __eq__(self, arg: ConstantOrMap_Double_TransBoundary, /) -> bool: ...

    @overload
    def __ne__(self, arg: Enum_TransportBoundaryType, /) -> bool: ...

    @overload
    def __ne__(self, arg: ConstantOrMap_Double_TransBoundary, /) -> bool: ...

    def __repr__(self) -> str: ...

class ConstantOrMap_Double_WellOperation:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, constant_value: Enum_WellOperation) -> None:
        """Cria um mapa com valor fixo e constante."""

    @overload
    def __init__(self, data_map: Mapping[float, Enum_WellOperation]) -> None:
        """Cria um mapa variável a partir de um dicionário nativo."""

    @overload
    def __init__(self, prm_string: str) -> None:
        """Cria o mapa a partir da sintaxe string do .prm."""

    def is_constant(self) -> bool:
        """Retorna se o objeto é um valor constante."""

    @overload
    def get_value(self, key: float) -> Enum_WellOperation:
        """Retorna o valor agendado no tempo/chave especificado."""

    @overload
    def get_value(self) -> Enum_WellOperation:
        """Retorna o valor agendado no tempo/chave ativo."""

    def at(self, key: float) -> Enum_WellOperation:
        """Retorna o valor agendado no tempo/chave especificado."""

    def __call__(self, key: float) -> Enum_WellOperation:
        """Permite chamar o objeto diretamente como com(t)."""

    def __len__(self) -> int: ...

    @overload
    def __eq__(self, arg: Enum_WellOperation, /) -> bool: ...

    @overload
    def __eq__(self, arg: ConstantOrMap_Double_WellOperation, /) -> bool: ...

    @overload
    def __ne__(self, arg: Enum_WellOperation, /) -> bool: ...

    @overload
    def __ne__(self, arg: ConstantOrMap_Double_WellOperation, /) -> bool: ...

    def __repr__(self) -> str: ...

class CustomRelativePermeability:
    def __init__(self) -> None: ...

    @property
    def ng(self) -> float: ...

    @ng.setter
    def ng(self, arg: float, /) -> None: ...

    @property
    def nw(self) -> float: ...

    @nw.setter
    def nw(self, arg: float, /) -> None: ...

    @property
    def krw0(self) -> float: ...

    @krw0.setter
    def krw0(self, arg: float, /) -> None: ...

    @property
    def krg0(self) -> float: ...

    @krg0.setter
    def krg0(self, arg: float, /) -> None: ...

class CoreyBrooksRelativePermeability:
    def __init__(self) -> None: ...

    @property
    def pore_dist_coeff(self) -> float: ...

    @pore_dist_coeff.setter
    def pore_dist_coeff(self, arg: float, /) -> None: ...

    @property
    def krw0(self) -> float: ...

    @krw0.setter
    def krw0(self, arg: float, /) -> None: ...

    @property
    def krg0(self) -> float: ...

    @krg0.setter
    def krg0(self, arg: float, /) -> None: ...

class CapillaryPressureTableModel:
    def __init__(self) -> None: ...

    @property
    def cp_table(self) -> dict[float, float]: ...

    @cp_table.setter
    def cp_table(self, arg: Mapping[float, float], /) -> None: ...

class LeverettJCapillaryPressureModel:
    def __init__(self) -> None: ...

    @property
    def pore_dist_coeff(self) -> float: ...

    @pore_dist_coeff.setter
    def pore_dist_coeff(self, arg: float, /) -> None: ...

    @property
    def gamma(self) -> float: ...

    @gamma.setter
    def gamma(self, arg: float, /) -> None: ...

class TableRelativePermeability:
    def __init__(self) -> None: ...

    @property
    def krw_table(self) -> dict[float, float]: ...

    @krw_table.setter
    def krw_table(self, arg: Mapping[float, float], /) -> None: ...

    @property
    def krg_table(self) -> dict[float, float]: ...

    @krg_table.setter
    def krg_table(self, arg: Mapping[float, float], /) -> None: ...

class KovscekModel:
    def __init__(self) -> None: ...

    @property
    def k01(self) -> float: ...

    @k01.setter
    def k01(self, arg: float, /) -> None: ...

    @property
    def k0m1(self) -> float: ...

    @k0m1.setter
    def k0m1(self, arg: float, /) -> None: ...

    @property
    def pcStarMax(self) -> float: ...

    @pcStarMax.setter
    def pcStarMax(self, arg: float, /) -> None: ...

    @property
    def refSurf(self) -> float: ...

    @refSurf.setter
    def refSurf(self, arg: float, /) -> None: ...

    @property
    def XtMax(self) -> float: ...

    @XtMax.setter
    def XtMax(self, arg: float, /) -> None: ...

    @property
    def betaT(self) -> float: ...

    @betaT.setter
    def betaT(self, arg: float, /) -> None: ...

    @property
    def krw0(self) -> float: ...

    @krw0.setter
    def krw0(self, arg: float, /) -> None: ...

    @property
    def krg0(self) -> float: ...

    @krg0.setter
    def krg0(self, arg: float, /) -> None: ...

    @property
    def ng(self) -> float: ...

    @ng.setter
    def ng(self, arg: float, /) -> None: ...

    @property
    def nw(self) -> float: ...

    @nw.setter
    def nw(self, arg: float, /) -> None: ...

    @property
    def alpha(self) -> float: ...

    @alpha.setter
    def alpha(self, arg: float, /) -> None: ...

    @property
    def const_trapping(self) -> bool: ...

    @const_trapping.setter
    def const_trapping(self, arg: bool, /) -> None: ...

class AshooriModel:
    def __init__(self) -> None: ...

    @property
    def K_c(self) -> float: ...

    @K_c.setter
    def K_c(self, arg: float, /) -> None: ...

    @property
    def A(self) -> float: ...

    @A.setter
    def A(self, arg: float, /) -> None: ...

    @property
    def max_mob_red(self) -> float: ...

    @max_mob_red.setter
    def max_mob_red(self, arg: float, /) -> None: ...

    @property
    def sw_critical(self) -> float: ...

    @sw_critical.setter
    def sw_critical(self, arg: float, /) -> None: ...

class StarsModel:
    def __init__(self) -> None: ...

    @property
    def sfbet(self) -> float: ...

    @sfbet.setter
    def sfbet(self, arg: float, /) -> None: ...

    @property
    def fmmob(self) -> float: ...

    @fmmob.setter
    def fmmob(self, arg: float, /) -> None: ...

    @property
    def sfdry(self) -> float: ...

    @sfdry.setter
    def sfdry(self, arg: float, /) -> None: ...

    @property
    def fmsurf(self) -> float: ...

    @fmsurf.setter
    def fmsurf(self, arg: float, /) -> None: ...

    @property
    def epsurf(self) -> float: ...

    @epsurf.setter
    def epsurf(self, arg: float, /) -> None: ...

    @property
    def fmcap(self) -> float: ...

    @fmcap.setter
    def fmcap(self, arg: float, /) -> None: ...

    @property
    def epcap(self) -> float: ...

    @epcap.setter
    def epcap(self, arg: float, /) -> None: ...

class LAMAPModel:
    def __init__(self) -> None: ...

    @property
    def muapp_vs_fg(self) -> ConstantOrMap_Double_Double: ...

    @muapp_vs_fg.setter
    def muapp_vs_fg(self, arg: ConstantOrMap_Double_Double, /) -> None: ...

class ZithaModel:
    def __init__(self) -> None: ...

    @property
    def K_g(self) -> float: ...

    @K_g.setter
    def K_g(self, arg: float, /) -> None: ...

    @property
    def K_d(self) -> float: ...

    @K_d.setter
    def K_d(self, arg: float, /) -> None: ...

    @property
    def K_1(self) -> float: ...

    @K_1.setter
    def K_1(self, arg: float, /) -> None: ...

    @property
    def K_2(self) -> float: ...

    @K_2.setter
    def K_2(self, arg: float, /) -> None: ...

    @property
    def m(self) -> float: ...

    @m.setter
    def m(self, arg: float, /) -> None: ...

    @property
    def pore_dist_coeff(self) -> float: ...

    @pore_dist_coeff.setter
    def pore_dist_coeff(self, arg: float, /) -> None: ...

    @property
    def gamma(self) -> float: ...

    @gamma.setter
    def gamma(self, arg: float, /) -> None: ...

    @property
    def k0_rw(self) -> float: ...

    @k0_rw.setter
    def k0_rw(self, arg: float, /) -> None: ...

    @property
    def k0_rf(self) -> float: ...

    @k0_rf.setter
    def k0_rf(self, arg: float, /) -> None: ...

    @property
    def pore_radius(self) -> float: ...

    @pore_radius.setter
    def pore_radius(self, arg: float, /) -> None: ...

    @property
    def theta_angle(self) -> float: ...

    @theta_angle.setter
    def theta_angle(self, arg: float, /) -> None: ...

class IdealGasDensityModel:
    def __init__(self) -> None: ...

    @property
    def gas_ideal_molecular_mass(self) -> float: ...

    @gas_ideal_molecular_mass.setter
    def gas_ideal_molecular_mass(self, arg: float, /) -> None: ...

    @property
    def gas_ideal_temp(self) -> float: ...

    @gas_ideal_temp.setter
    def gas_ideal_temp(self, arg: float, /) -> None: ...

    @property
    def gas_ideal_simp_cte(self) -> float: ...

    @gas_ideal_simp_cte.setter
    def gas_ideal_simp_cte(self, arg: float, /) -> None: ...

    @property
    def gas_constant(self) -> float: ...

    @gas_constant.setter
    def gas_constant(self, arg: float, /) -> None: ...

class LinearDensityModel:
    def __init__(self) -> None: ...

    @property
    def ref_p(self) -> float: ...

    @ref_p.setter
    def ref_p(self, arg: float, /) -> None: ...

    @property
    def ref_rho(self) -> float: ...

    @ref_rho.setter
    def ref_rho(self, arg: float, /) -> None: ...

class ExponentialDensityModel:
    def __init__(self) -> None: ...

    @property
    def ref_p(self) -> float: ...

    @ref_p.setter
    def ref_p(self, arg: float, /) -> None: ...

    @property
    def ref_rho(self) -> float: ...

    @ref_rho.setter
    def ref_rho(self, arg: float, /) -> None: ...

    @property
    def gas_comp(self) -> float: ...

    @gas_comp.setter
    def gas_comp(self, arg: float, /) -> None: ...

class TableDensityModel:
    def __init__(self) -> None: ...

    @property
    def density_table(self) -> dict[float, float]: ...

    @density_table.setter
    def density_table(self, arg: Mapping[float, float], /) -> None: ...

class LinearEquilibriumAdsorptionModel:
    def __init__(self) -> None: ...

    @property
    def k_eq_a(self) -> float: ...

    @k_eq_a.setter
    def k_eq_a(self, arg: float, /) -> None: ...

class LinearNonEquilibriumAdsorptionModel:
    def __init__(self) -> None: ...

    @property
    def k_kin_a(self) -> float: ...

    @k_kin_a.setter
    def k_kin_a(self, arg: float, /) -> None: ...

    @property
    def k_d(self) -> float: ...

    @k_d.setter
    def k_d(self, arg: float, /) -> None: ...

class LangmuirEquilibriumAdsorptionModel:
    def __init__(self) -> None: ...

    @property
    def k_eq_1(self) -> float: ...

    @k_eq_1.setter
    def k_eq_1(self, arg: float, /) -> None: ...

    @property
    def k_eq_2(self) -> float: ...

    @k_eq_2.setter
    def k_eq_2(self, arg: float, /) -> None: ...

class LangmuirNonEquilibriumAdsorptionModel:
    def __init__(self) -> None: ...

    @property
    def k_kin_1(self) -> float: ...

    @k_kin_1.setter
    def k_kin_1(self, arg: float, /) -> None: ...

    @property
    def k_kin_2(self) -> float: ...

    @k_kin_2.setter
    def k_kin_2(self, arg: float, /) -> None: ...

    @property
    def k_d(self) -> float: ...

    @k_d.setter
    def k_d(self, arg: float, /) -> None: ...

class SIPSEquilibriumAdsorptionModel:
    def __init__(self) -> None: ...

    @property
    def k_eq_1(self) -> float: ...

    @k_eq_1.setter
    def k_eq_1(self, arg: float, /) -> None: ...

    @property
    def k_eq_2(self) -> float: ...

    @k_eq_2.setter
    def k_eq_2(self, arg: float, /) -> None: ...

    @property
    def k_eq_3(self) -> float: ...

    @k_eq_3.setter
    def k_eq_3(self, arg: float, /) -> None: ...

class SIPSNonEquilibriumAdsorptionModel:
    def __init__(self) -> None: ...

    @property
    def k_kin_1(self) -> float: ...

    @k_kin_1.setter
    def k_kin_1(self, arg: float, /) -> None: ...

    @property
    def k_kin_2(self) -> float: ...

    @k_kin_2.setter
    def k_kin_2(self, arg: float, /) -> None: ...

    @property
    def k_kin_3(self) -> float: ...

    @k_kin_3.setter
    def k_kin_3(self, arg: float, /) -> None: ...

    @property
    def k_d(self) -> float: ...

    @k_d.setter
    def k_d(self, arg: float, /) -> None: ...

class PseudoFirstOrderNonEquilibriumAdsorptionModel:
    def __init__(self) -> None: ...

    @property
    def kf(self) -> float: ...

    @kf.setter
    def kf(self, arg: float, /) -> None: ...

    @property
    def Kf_1(self) -> float: ...

    @Kf_1.setter
    def Kf_1(self, arg: float, /) -> None: ...

    @property
    def Kf_2(self) -> float: ...

    @Kf_2.setter
    def Kf_2(self, arg: float, /) -> None: ...

    @property
    def Kf_3(self) -> float: ...

    @Kf_3.setter
    def Kf_3(self, arg: float, /) -> None: ...

class PseudoSecondOrderNonEquilibriumAdsorptionModel:
    def __init__(self) -> None: ...

    @property
    def ks(self) -> float: ...

    @ks.setter
    def ks(self, arg: float, /) -> None: ...

    @property
    def Ks_1(self) -> float: ...

    @Ks_1.setter
    def Ks_1(self, arg: float, /) -> None: ...

    @property
    def Ks_2(self) -> float: ...

    @Ks_2.setter
    def Ks_2(self, arg: float, /) -> None: ...

    @property
    def Ks_3(self) -> float: ...

    @Ks_3.setter
    def Ks_3(self, arg: float, /) -> None: ...

class SyntheticRockFieldParameters:
    def __init__(self) -> None: ...

    @property
    def seed(self) -> int:
        """Random seed used to generate the synthetic rock field."""

    @seed.setter
    def seed(self, arg: int, /) -> None: ...

    @property
    def permeability_avg(self) -> float:
        """Target average permeability of the generated field [m²]."""

    @permeability_avg.setter
    def permeability_avg(self, arg: float, /) -> None: ...

    @property
    def porosity_avg(self) -> float:
        """Target average porosity of the generated field [-]."""

    @porosity_avg.setter
    def porosity_avg(self, arg: float, /) -> None: ...

    @property
    def heterogeneity(self) -> float:
        """Controls the intensity of spatial heterogeneity."""

    @heterogeneity.setter
    def heterogeneity(self, arg: float, /) -> None: ...

class GlobalSettings:
    def __init__(self) -> None: ...

    @property
    def mesh_type(self) -> Enum_MeshType: ...

    @mesh_type.setter
    def mesh_type(self, arg: Enum_MeshType, /) -> None: ...

    @property
    def dimension(self) -> int: ...

    @dimension.setter
    def dimension(self, arg: int, /) -> None: ...

class PetrophysicalUpscaling:
    def __init__(self) -> None: ...

    @property
    def method_x(self) -> Enum_UpscalingMethod: ...

    @method_x.setter
    def method_x(self, arg: Enum_UpscalingMethod, /) -> None: ...

    @property
    def method_y(self) -> Enum_UpscalingMethod: ...

    @method_y.setter
    def method_y(self, arg: Enum_UpscalingMethod, /) -> None: ...

    @property
    def method_z(self) -> Enum_UpscalingMethod: ...

    @method_z.setter
    def method_z(self, arg: Enum_UpscalingMethod, /) -> None: ...

    @property
    def por_method(self) -> Enum_UpscalingMethod: ...

    @por_method.setter
    def por_method(self, arg: Enum_UpscalingMethod, /) -> None: ...

    @property
    def power_law_exponent_x(self) -> float: ...

    @power_law_exponent_x.setter
    def power_law_exponent_x(self, arg: float, /) -> None: ...

    @property
    def power_law_exponent_y(self) -> float: ...

    @power_law_exponent_y.setter
    def power_law_exponent_y(self, arg: float, /) -> None: ...

    @property
    def power_law_exponent_z(self) -> float: ...

    @power_law_exponent_z.setter
    def power_law_exponent_z(self, arg: float, /) -> None: ...

    @property
    def power_law_exponent_por(self) -> float: ...

    @power_law_exponent_por.setter
    def power_law_exponent_por(self, arg: float, /) -> None: ...

class RockProperties:
    def __init__(self) -> None: ...

    @property
    def upscaling(self) -> PetrophysicalUpscaling: ...

    @upscaling.setter
    def upscaling(self, arg: PetrophysicalUpscaling, /) -> None: ...

    @property
    def rock_regularization(self) -> bool: ...

    @rock_regularization.setter
    def rock_regularization(self, arg: bool, /) -> None: ...

    @property
    def use_material_ids(self) -> bool: ...

    @use_material_ids.setter
    def use_material_ids(self, arg: bool, /) -> None: ...

    @property
    def permeability_x_map(self) -> dict[int, float]: ...

    @permeability_x_map.setter
    def permeability_x_map(self, arg: Mapping[int, float], /) -> None: ...

    @property
    def permeability_y_map(self) -> dict[int, float]: ...

    @permeability_y_map.setter
    def permeability_y_map(self, arg: Mapping[int, float], /) -> None: ...

    @property
    def permeability_z_map(self) -> dict[int, float]: ...

    @permeability_z_map.setter
    def permeability_z_map(self, arg: Mapping[int, float], /) -> None: ...

    @property
    def porosity_map(self) -> dict[int, float]: ...

    @porosity_map.setter
    def porosity_map(self, arg: Mapping[int, float], /) -> None: ...

    @property
    def permeability_x(self) -> float: ...

    @permeability_x.setter
    def permeability_x(self, arg: float, /) -> None: ...

    @property
    def permeability_y(self) -> float: ...

    @permeability_y.setter
    def permeability_y(self, arg: float, /) -> None: ...

    @property
    def permeability_z(self) -> float: ...

    @permeability_z.setter
    def permeability_z(self, arg: float, /) -> None: ...

    @property
    def porosity(self) -> float: ...

    @porosity.setter
    def porosity(self, arg: float, /) -> None: ...

    @property
    def mass_density(self) -> float: ...

    @mass_density.setter
    def mass_density(self, arg: float, /) -> None: ...

    @property
    def perm_filename(self) -> str: ...

    @perm_filename.setter
    def perm_filename(self, arg: str, /) -> None: ...

    @property
    def por_filename(self) -> str: ...

    @por_filename.setter
    def por_filename(self, arg: str, /) -> None: ...

    @property
    def use_custom_arrays(self) -> bool: ...

    @use_custom_arrays.setter
    def use_custom_arrays(self, arg: bool, /) -> None: ...

    @property
    def custom_porosity(self) -> list[float]: ...

    @custom_porosity.setter
    def custom_porosity(self, arg: Sequence[float], /) -> None: ...

    @property
    def custom_permeability_x(self) -> list[float]: ...

    @custom_permeability_x.setter
    def custom_permeability_x(self, arg: Sequence[float], /) -> None: ...

    @property
    def custom_permeability_y(self) -> list[float]: ...

    @custom_permeability_y.setter
    def custom_permeability_y(self, arg: Sequence[float], /) -> None: ...

    @property
    def custom_permeability_z(self) -> list[float]: ...

    @custom_permeability_z.setter
    def custom_permeability_z(self, arg: Sequence[float], /) -> None: ...

    @property
    def use_python_point_cloud(self) -> bool: ...

    @use_python_point_cloud.setter
    def use_python_point_cloud(self, arg: bool, /) -> None: ...

    @property
    def pc_coords(self) -> list[float]: ...

    @pc_coords.setter
    def pc_coords(self, arg: Sequence[float], /) -> None: ...

    @property
    def pc_porosity(self) -> list[float]: ...

    @pc_porosity.setter
    def pc_porosity(self, arg: Sequence[float], /) -> None: ...

    @property
    def pc_perm_x(self) -> list[float]: ...

    @pc_perm_x.setter
    def pc_perm_x(self, arg: Sequence[float], /) -> None: ...

    @property
    def pc_perm_y(self) -> list[float]: ...

    @pc_perm_y.setter
    def pc_perm_y(self, arg: Sequence[float], /) -> None: ...

    @property
    def pc_perm_z(self) -> list[float]: ...

    @pc_perm_z.setter
    def pc_perm_z(self, arg: Sequence[float], /) -> None: ...

    @property
    def use_synthetic_field(self) -> bool: ...

    @use_synthetic_field.setter
    def use_synthetic_field(self, arg: bool, /) -> None: ...

    @property
    def synthetic_rock_field(self) -> SyntheticRockFieldParameters:
        """Parameters for the synthetic heterogeneous rock field."""

    @synthetic_rock_field.setter
    def synthetic_rock_field(self, arg: SyntheticRockFieldParameters, /) -> None: ...

class GravProperties:
    def __init__(self) -> None: ...

    @property
    def grav_acl_x(self) -> float: ...

    @grav_acl_x.setter
    def grav_acl_x(self, arg: float, /) -> None: ...

    @property
    def grav_acl_y(self) -> float: ...

    @grav_acl_y.setter
    def grav_acl_y(self, arg: float, /) -> None: ...

    @property
    def grav_acl_z(self) -> float: ...

    @grav_acl_z.setter
    def grav_acl_z(self, arg: float, /) -> None: ...

    @property
    def using_gravity_x(self) -> bool: ...

    @using_gravity_x.setter
    def using_gravity_x(self, arg: bool, /) -> None: ...

    @property
    def using_gravity_y(self) -> bool: ...

    @using_gravity_y.setter
    def using_gravity_y(self, arg: bool, /) -> None: ...

    @property
    def using_gravity_z(self) -> bool: ...

    @using_gravity_z.setter
    def using_gravity_z(self, arg: bool, /) -> None: ...

    @property
    def using_gravity(self) -> bool: ...

    @using_gravity.setter
    def using_gravity(self, arg: bool, /) -> None: ...

class GasCompProperties:
    def __init__(self) -> None: ...

    @property
    def compressibility(self) -> bool: ...

    @compressibility.setter
    def compressibility(self, arg: bool, /) -> None: ...

    @property
    def gas_state_equation(self) -> Enum_GasStateEquationModel: ...

    @gas_state_equation.setter
    def gas_state_equation(self, arg: Enum_GasStateEquationModel, /) -> None: ...

    @property
    def exp_density_model(self) -> ExponentialDensityModel: ...

    @exp_density_model.setter
    def exp_density_model(self, arg: ExponentialDensityModel, /) -> None: ...

    @property
    def linear_density_model(self) -> LinearDensityModel: ...

    @linear_density_model.setter
    def linear_density_model(self, arg: LinearDensityModel, /) -> None: ...

    @property
    def ideal_gas_density_model(self) -> IdealGasDensityModel: ...

    @ideal_gas_density_model.setter
    def ideal_gas_density_model(self, arg: IdealGasDensityModel, /) -> None: ...

    @property
    def table_density_model(self) -> TableDensityModel: ...

    @table_density_model.setter
    def table_density_model(self, arg: TableDensityModel, /) -> None: ...

class FluidProperties:
    def __init__(self) -> None: ...

    @property
    def mu_w(self) -> float: ...

    @mu_w.setter
    def mu_w(self, arg: float, /) -> None: ...

    @property
    def rho_w(self) -> float: ...

    @rho_w.setter
    def rho_w(self, arg: float, /) -> None: ...

    @property
    def rho_g(self) -> float: ...

    @rho_g.setter
    def rho_g(self, arg: float, /) -> None: ...

    @property
    def mu_g(self) -> float: ...

    @mu_g.setter
    def mu_g(self, arg: float, /) -> None: ...

    @property
    def grav_acl(self) -> GravProperties: ...

    @grav_acl.setter
    def grav_acl(self, arg: GravProperties, /) -> None: ...

    @property
    def gas_comp_prop(self) -> GasCompProperties: ...

    @gas_comp_prop.setter
    def gas_comp_prop(self, arg: GasCompProperties, /) -> None: ...

class RockFluidInteractions:
    def __init__(self) -> None: ...

    @property
    def swc(self) -> float: ...

    @swc.setter
    def swc(self, arg: float, /) -> None: ...

    @property
    def sgr(self) -> float: ...

    @sgr.setter
    def sgr(self, arg: float, /) -> None: ...

    @property
    def sigma_wg(self) -> float: ...

    @sigma_wg.setter
    def sigma_wg(self, arg: float, /) -> None: ...

    @property
    def cap_pressure_model(self) -> Enum_CapillaryPressureModel: ...

    @cap_pressure_model.setter
    def cap_pressure_model(self, arg: Enum_CapillaryPressureModel, /) -> None: ...

    @property
    def rel_perm_model(self) -> Enum_RelativePermeabilityModel: ...

    @rel_perm_model.setter
    def rel_perm_model(self, arg: Enum_RelativePermeabilityModel, /) -> None: ...

    @property
    def custom_rel_perm(self) -> CustomRelativePermeability: ...

    @custom_rel_perm.setter
    def custom_rel_perm(self, arg: CustomRelativePermeability, /) -> None: ...

    @property
    def corey_brooks_rel_perm(self) -> CoreyBrooksRelativePermeability: ...

    @corey_brooks_rel_perm.setter
    def corey_brooks_rel_perm(self, arg: CoreyBrooksRelativePermeability, /) -> None: ...

    @property
    def table_rel_perm(self) -> TableRelativePermeability: ...

    @table_rel_perm.setter
    def table_rel_perm(self, arg: TableRelativePermeability, /) -> None: ...

    @property
    def cp_table_model(self) -> CapillaryPressureTableModel: ...

    @cp_table_model.setter
    def cp_table_model(self, arg: CapillaryPressureTableModel, /) -> None: ...

    @property
    def leverett_j_cp_model(self) -> LeverettJCapillaryPressureModel: ...

    @leverett_j_cp_model.setter
    def leverett_j_cp_model(self, arg: LeverettJCapillaryPressureModel, /) -> None: ...

class SurfactantProperties:
    def __init__(self) -> None: ...

    @property
    def adsorption_behavior(self) -> Enum_AdsorptionBehavior: ...

    @adsorption_behavior.setter
    def adsorption_behavior(self, arg: Enum_AdsorptionBehavior, /) -> None: ...

    @property
    def equilibrium_adsorption_model(self) -> Enum_EquilibriumAdsorptionModel: ...

    @equilibrium_adsorption_model.setter
    def equilibrium_adsorption_model(self, arg: Enum_EquilibriumAdsorptionModel, /) -> None: ...

    @property
    def non_equilibrium_adsorption_model(self) -> Enum_KineticAdsorptionModel: ...

    @non_equilibrium_adsorption_model.setter
    def non_equilibrium_adsorption_model(self, arg: Enum_KineticAdsorptionModel, /) -> None: ...

    @property
    def linear_equilibrium_model(self) -> LinearEquilibriumAdsorptionModel: ...

    @linear_equilibrium_model.setter
    def linear_equilibrium_model(self, arg: LinearEquilibriumAdsorptionModel, /) -> None: ...

    @property
    def linear_non_equilibrium_model(self) -> LinearNonEquilibriumAdsorptionModel: ...

    @linear_non_equilibrium_model.setter
    def linear_non_equilibrium_model(self, arg: LinearNonEquilibriumAdsorptionModel, /) -> None: ...

    @property
    def langmuir_equilibrium_model(self) -> LangmuirEquilibriumAdsorptionModel: ...

    @langmuir_equilibrium_model.setter
    def langmuir_equilibrium_model(self, arg: LangmuirEquilibriumAdsorptionModel, /) -> None: ...

    @property
    def langmuir_non_equilibrium_model(self) -> LangmuirNonEquilibriumAdsorptionModel: ...

    @langmuir_non_equilibrium_model.setter
    def langmuir_non_equilibrium_model(self, arg: LangmuirNonEquilibriumAdsorptionModel, /) -> None: ...

    @property
    def sips_equilibrium_model(self) -> SIPSEquilibriumAdsorptionModel: ...

    @sips_equilibrium_model.setter
    def sips_equilibrium_model(self, arg: SIPSEquilibriumAdsorptionModel, /) -> None: ...

    @property
    def sips_non_equilibrium_model(self) -> SIPSNonEquilibriumAdsorptionModel: ...

    @sips_non_equilibrium_model.setter
    def sips_non_equilibrium_model(self, arg: SIPSNonEquilibriumAdsorptionModel, /) -> None: ...

    @property
    def p_first_order_non_equilibrium_model(self) -> PseudoFirstOrderNonEquilibriumAdsorptionModel: ...

    @p_first_order_non_equilibrium_model.setter
    def p_first_order_non_equilibrium_model(self, arg: PseudoFirstOrderNonEquilibriumAdsorptionModel, /) -> None: ...

    @property
    def p_sec_order_non_equilibrium_model(self) -> PseudoSecondOrderNonEquilibriumAdsorptionModel: ...

    @p_sec_order_non_equilibrium_model.setter
    def p_sec_order_non_equilibrium_model(self, arg: PseudoSecondOrderNonEquilibriumAdsorptionModel, /) -> None: ...

    @property
    def d_s(self) -> float: ...

    @d_s.setter
    def d_s(self, arg: float, /) -> None: ...

class EORMechanisms:
    def __init__(self) -> None: ...

    @property
    def foam_model(self) -> Enum_FoamModel: ...

    @foam_model.setter
    def foam_model(self, arg: Enum_FoamModel, /) -> None: ...

    @property
    def n_max(self) -> float: ...

    @n_max.setter
    def n_max(self, arg: float, /) -> None: ...

    @property
    def kovscek_model(self) -> KovscekModel: ...

    @kovscek_model.setter
    def kovscek_model(self, arg: KovscekModel, /) -> None: ...

    @property
    def ashoori_model(self) -> AshooriModel: ...

    @ashoori_model.setter
    def ashoori_model(self, arg: AshooriModel, /) -> None: ...

    @property
    def lamap_model(self) -> LAMAPModel: ...

    @lamap_model.setter
    def lamap_model(self, arg: LAMAPModel, /) -> None: ...

    @property
    def stars_model(self) -> StarsModel: ...

    @stars_model.setter
    def stars_model(self, arg: StarsModel, /) -> None: ...

    @property
    def zitha_model(self) -> ZithaModel: ...

    @zitha_model.setter
    def zitha_model(self, arg: ZithaModel, /) -> None: ...

    @property
    def surfactant_properties(self) -> SurfactantProperties: ...

    @surfactant_properties.setter
    def surfactant_properties(self, arg: SurfactantProperties, /) -> None: ...

class OrthogonalGeometry:
    def __init__(self) -> None: ...

    @property
    def x_init(self) -> float: ...

    @x_init.setter
    def x_init(self, arg: float, /) -> None: ...

    @property
    def x_final(self) -> float: ...

    @x_final.setter
    def x_final(self, arg: float, /) -> None: ...

    @property
    def y_init(self) -> float: ...

    @y_init.setter
    def y_init(self, arg: float, /) -> None: ...

    @property
    def y_final(self) -> float: ...

    @y_final.setter
    def y_final(self, arg: float, /) -> None: ...

    @property
    def z_init(self) -> float: ...

    @z_init.setter
    def z_init(self, arg: float, /) -> None: ...

    @property
    def z_final(self) -> float: ...

    @z_final.setter
    def z_final(self, arg: float, /) -> None: ...

    @property
    def block_thickness(self) -> float: ...

    @block_thickness.setter
    def block_thickness(self, arg: float, /) -> None: ...

    @property
    def n_x(self) -> int: ...

    @n_x.setter
    def n_x(self, arg: int, /) -> None: ...

    @property
    def n_y(self) -> int: ...

    @n_y.setter
    def n_y(self, arg: int, /) -> None: ...

    @property
    def n_z(self) -> int: ...

    @n_z.setter
    def n_z(self, arg: int, /) -> None: ...

    def validate(self) -> None: ...

class UnstructuredGeometry:
    def __init__(self) -> None: ...

    @property
    def block_thickness(self) -> float: ...

    @block_thickness.setter
    def block_thickness(self, arg: float, /) -> None: ...

    @property
    def mesh_filename(self) -> str: ...

    @mesh_filename.setter
    def mesh_filename(self, arg: str, /) -> None: ...

class VariableInitialization:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: float, /) -> None: ...

    @property
    def initialization_type(self) -> Enum_InitializationType: ...

    @initialization_type.setter
    def initialization_type(self, arg: Enum_InitializationType, /) -> None: ...

    @property
    def constant_value(self) -> float: ...

    @constant_value.setter
    def constant_value(self, arg: float, /) -> None: ...

    @property
    def filename(self) -> str: ...

    @filename.setter
    def filename(self, arg: str, /) -> None: ...

class InitialState:
    def __init__(self) -> None: ...

    @property
    def initialization(self) -> dict[Enum_Variable, VariableInitialization]: ...

    @initialization.setter
    def initialization(self, arg: Mapping[Enum_Variable, VariableInitialization], /) -> None: ...

    @property
    def pressure_init(self) -> VariableInitialization: ...

    @pressure_init.setter
    def pressure_init(self, arg: VariableInitialization, /) -> None: ...

class OrthoBoundaryPart:
    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def darcy_boundary_type(self) -> ConstantOrMap_Double_DarcyBoundary: ...

    @darcy_boundary_type.setter
    def darcy_boundary_type(self, arg: ConstantOrMap_Double_DarcyBoundary, /) -> None: ...

    @property
    def darcy_boundary_value(self) -> ConstantOrMap_Double_Double: ...

    @darcy_boundary_value.setter
    def darcy_boundary_value(self, arg: ConstantOrMap_Double_Double, /) -> None: ...

    @property
    def trans_boundary_type(self) -> ConstantOrMap_Double_TransBoundary: ...

    @trans_boundary_type.setter
    def trans_boundary_type(self, arg: ConstantOrMap_Double_TransBoundary, /) -> None: ...

    @property
    def trans_boundary_values(self) -> VariableMap: ...

    @trans_boundary_values.setter
    def trans_boundary_values(self, arg: VariableMap, /) -> None: ...

class OrthogonalBoundaryConditions:
    def __init__(self) -> None: ...

    @property
    def top(self) -> OrthoBoundaryPart: ...

    @top.setter
    def top(self, arg: OrthoBoundaryPart, /) -> None: ...

    @property
    def bottom(self) -> OrthoBoundaryPart: ...

    @bottom.setter
    def bottom(self, arg: OrthoBoundaryPart, /) -> None: ...

    @property
    def left(self) -> OrthoBoundaryPart: ...

    @left.setter
    def left(self, arg: OrthoBoundaryPart, /) -> None: ...

    @property
    def right(self) -> OrthoBoundaryPart: ...

    @right.setter
    def right(self, arg: OrthoBoundaryPart, /) -> None: ...

    @property
    def front(self) -> OrthoBoundaryPart: ...

    @front.setter
    def front(self, arg: OrthoBoundaryPart, /) -> None: ...

    @property
    def back(self) -> OrthoBoundaryPart: ...

    @back.setter
    def back(self, arg: OrthoBoundaryPart, /) -> None: ...

class UnstructuredBoundaryPart:
    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def boundary_id(self) -> int: ...

    @boundary_id.setter
    def boundary_id(self, arg: int, /) -> None: ...

    @property
    def darcy_boundary_type(self) -> ConstantOrMap_Double_DarcyBoundary: ...

    @darcy_boundary_type.setter
    def darcy_boundary_type(self, arg: ConstantOrMap_Double_DarcyBoundary, /) -> None: ...

    @property
    def darcy_boundary_value(self) -> ConstantOrMap_Double_Double: ...

    @darcy_boundary_value.setter
    def darcy_boundary_value(self, arg: ConstantOrMap_Double_Double, /) -> None: ...

    @property
    def trans_boundary_type(self) -> ConstantOrMap_Double_TransBoundary: ...

    @trans_boundary_type.setter
    def trans_boundary_type(self, arg: ConstantOrMap_Double_TransBoundary, /) -> None: ...

    @property
    def trans_boundary_values(self) -> VariableMap: ...

    @trans_boundary_values.setter
    def trans_boundary_values(self, arg: VariableMap, /) -> None: ...

class UnstructuredBoundaryConditions:
    def __init__(self) -> None: ...

    @property
    def n_boundaries(self) -> int: ...

    @n_boundaries.setter
    def n_boundaries(self, arg: int, /) -> None: ...

    @property
    def boundaries(self) -> list[UnstructuredBoundaryPart]: ...

    @boundaries.setter
    def boundaries(self, arg: Sequence[UnstructuredBoundaryPart], /) -> None: ...

    @overload
    def setup_dynamic_boundaries(self, n: int) -> None: ...

    @overload
    def setup_dynamic_boundaries(self, names: Sequence[str]) -> None: ...

    @overload
    def setup_dynamic_boundaries(self, named_ids: Sequence[tuple[str, int]]) -> None: ...

    @overload
    def setup_dynamic_boundaries(self, named_ids: Mapping[str, int]) -> None: ...

    @overload
    def __getitem__(self, arg: int, /) -> object: ...

    @overload
    def __getitem__(self, arg: str, /) -> object: ...

class InitialAndBoundaryConditions:
    def __init__(self) -> None: ...

    @property
    def initial_state(self) -> InitialState: ...

    @initial_state.setter
    def initial_state(self, arg: InitialState, /) -> None: ...

    @property
    def orthogonal_boundaries(self) -> OrthogonalBoundaryConditions: ...

    @orthogonal_boundaries.setter
    def orthogonal_boundaries(self, arg: OrthogonalBoundaryConditions, /) -> None: ...

    @property
    def unstructured_boundaries(self) -> UnstructuredBoundaryConditions: ...

    @unstructured_boundaries.setter
    def unstructured_boundaries(self, arg: UnstructuredBoundaryConditions, /) -> None: ...

    @overload
    def setup_dynamic_boundaries(self, n: int) -> None: ...

    @overload
    def setup_dynamic_boundaries(self, names: Sequence[str]) -> None: ...

    @overload
    def setup_dynamic_boundaries(self, named_ids: Sequence[tuple[str, int]]) -> None: ...

    @overload
    def setup_dynamic_boundaries(self, named_ids: Mapping[str, int]) -> None: ...

    @overload
    def __getitem__(self, name: str) -> object:
        """Access boundary by name."""

    @overload
    def __getitem__(self, boundary_id: int) -> object:
        """Access boundary by numeric ID."""

class WellConfig:
    def __init__(self) -> None: ...

    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def well_type(self) -> Enum_WellType: ...

    @well_type.setter
    def well_type(self, arg: Enum_WellType, /) -> None: ...

    @property
    def constraint_type(self) -> Enum_WellConstraintType: ...

    @constraint_type.setter
    def constraint_type(self, arg: Enum_WellConstraintType, /) -> None: ...

    @property
    def well_operation(self) -> ConstantOrMap_Double_WellOperation: ...

    @well_operation.setter
    def well_operation(self, arg: ConstantOrMap_Double_WellOperation, /) -> None: ...

    @property
    def radius(self) -> float: ...

    @radius.setter
    def radius(self, arg: float, /) -> None: ...

    @property
    def skin_factor(self) -> float: ...

    @skin_factor.setter
    def skin_factor(self, arg: float, /) -> None: ...

    @property
    def geo_factor(self) -> float: ...

    @geo_factor.setter
    def geo_factor(self, arg: float, /) -> None: ...

    @property
    def wfrac(self) -> float: ...

    @wfrac.setter
    def wfrac(self, arg: float, /) -> None: ...

    @property
    def use_hydrostatic_head(self) -> bool: ...

    @use_hydrostatic_head.setter
    def use_hydrostatic_head(self, arg: bool, /) -> None: ...

    @property
    def constraint_value(self) -> ConstantOrMap_Double_Double: ...

    @constraint_value.setter
    def constraint_value(self, arg: ConstantOrMap_Double_Double, /) -> None: ...

    @property
    def trajectory_coords(self) -> list[float]: ...

    @trajectory_coords.setter
    def trajectory_coords(self, arg: Sequence[float], /) -> None: ...

    @property
    def injected_fluid(self) -> VariableMap: ...

    @injected_fluid.setter
    def injected_fluid(self, arg: VariableMap, /) -> None: ...

class WellSetConfig:
    def __init__(self) -> None: ...

    @property
    def n_wells(self) -> int: ...

    @n_wells.setter
    def n_wells(self, arg: int, /) -> None: ...

    @property
    def well_vec(self) -> list[WellConfig]: ...

    @well_vec.setter
    def well_vec(self, arg: Sequence[WellConfig], /) -> None: ...

    def setup_dynamic_wells(self, arg: int, /) -> None: ...

class TimeData:
    def __init__(self) -> None: ...

    @property
    def initial_time(self) -> float: ...

    @initial_time.setter
    def initial_time(self, arg: float, /) -> None: ...

    @property
    def final_time(self) -> float: ...

    @final_time.setter
    def final_time(self, arg: float, /) -> None: ...

    @property
    def max_time_step(self) -> float: ...

    @max_time_step.setter
    def max_time_step(self, arg: float, /) -> None: ...

    @property
    def time(self) -> float: ...

    @time.setter
    def time(self, arg: float, /) -> None: ...

    @property
    def darcy_time_step(self) -> float: ...

    @darcy_time_step.setter
    def darcy_time_step(self, arg: float, /) -> None: ...

class ExecutionControl:
    def __init__(self) -> None: ...

    @property
    def darcy_degree_fe(self) -> int: ...

    @darcy_degree_fe.setter
    def darcy_degree_fe(self, arg: int, /) -> None: ...

    @property
    def num_threads(self) -> int: ...

    @num_threads.setter
    def num_threads(self, arg: int, /) -> None: ...

    @property
    def variables(self) -> set[Enum_Variable]: ...

    @variables.setter
    def variables(self, arg: Set[Enum_Variable], /) -> None: ...

    @property
    def foam_behavior(self) -> Enum_FoamBehavior: ...

    @foam_behavior.setter
    def foam_behavior(self, arg: Enum_FoamBehavior, /) -> None: ...

    @property
    def surfactant_behavior(self) -> Enum_SurfactantBehavior: ...

    @surfactant_behavior.setter
    def surfactant_behavior(self, arg: Enum_SurfactantBehavior, /) -> None: ...

    @property
    def time_integrator(self) -> Enum_TimeIntegrator: ...

    @time_integrator.setter
    def time_integrator(self, arg: Enum_TimeIntegrator, /) -> None: ...

    @property
    def nonlinear_solver(self) -> Enum_NonlinearSolver: ...

    @nonlinear_solver.setter
    def nonlinear_solver(self, arg: Enum_NonlinearSolver, /) -> None: ...

    @property
    def max_nonlin_iters(self) -> int: ...

    @max_nonlin_iters.setter
    def max_nonlin_iters(self, arg: int, /) -> None: ...

    @property
    def num_method(self) -> Enum_NumericalMethod: ...

    @num_method.setter
    def num_method(self, arg: Enum_NumericalMethod, /) -> None: ...

    @property
    def reltol(self) -> float: ...

    @reltol.setter
    def reltol(self, arg: float, /) -> None: ...

    @property
    def abstol(self) -> float: ...

    @abstol.setter
    def abstol(self, arg: float, /) -> None: ...

    @property
    def abstol_sw(self) -> float: ...

    @abstol_sw.setter
    def abstol_sw(self, arg: float, /) -> None: ...

    @property
    def fixed_nd(self) -> float: ...

    @fixed_nd.setter
    def fixed_nd(self, arg: float, /) -> None: ...

    @property
    def fixed_cs(self) -> float: ...

    @fixed_cs.setter
    def fixed_cs(self, arg: float, /) -> None: ...

    @property
    def artificial_diff(self) -> float: ...

    @artificial_diff.setter
    def artificial_diff(self, arg: float, /) -> None: ...

    @property
    def bounds_check_at_each_timestep(self) -> bool: ...

    @bounds_check_at_each_timestep.setter
    def bounds_check_at_each_timestep(self, arg: bool, /) -> None: ...

    @property
    def bounds_check_at_reconstruction(self) -> bool: ...

    @bounds_check_at_reconstruction.setter
    def bounds_check_at_reconstruction(self, arg: bool, /) -> None: ...

    @property
    def bounds_check_at_rhs(self) -> bool: ...

    @bounds_check_at_rhs.setter
    def bounds_check_at_rhs(self, arg: bool, /) -> None: ...

    @property
    def verbose_mode(self) -> bool: ...

    @verbose_mode.setter
    def verbose_mode(self, arg: bool, /) -> None: ...

    @property
    def non_convex_flux_strategy(self) -> Enum_NonConvexFluxStrategy: ...

    @non_convex_flux_strategy.setter
    def non_convex_flux_strategy(self, arg: Enum_NonConvexFluxStrategy, /) -> None: ...

    @property
    def darcy_error_tolerance(self) -> float: ...

    @darcy_error_tolerance.setter
    def darcy_error_tolerance(self, arg: float, /) -> None: ...

    @property
    def darcy_extrapolation_degree(self) -> int: ...

    @darcy_extrapolation_degree.setter
    def darcy_extrapolation_degree(self, arg: int, /) -> None: ...

    @property
    def darcy_time_step_strategy(self) -> Enum_DarcyTimeStepStrategy: ...

    @darcy_time_step_strategy.setter
    def darcy_time_step_strategy(self, arg: Enum_DarcyTimeStepStrategy, /) -> None: ...

    @property
    def darcy_linear_solver(self) -> Enum_DarcyLinearSolver: ...

    @darcy_linear_solver.setter
    def darcy_linear_solver(self, arg: Enum_DarcyLinearSolver, /) -> None: ...

    @property
    def darcy_preconditioner(self) -> Enum_DarcyPreconditioner: ...

    @darcy_preconditioner.setter
    def darcy_preconditioner(self, arg: Enum_DarcyPreconditioner, /) -> None: ...

    @property
    def transport_linear_solver(self) -> Enum_TransportLinearSolver: ...

    @transport_linear_solver.setter
    def transport_linear_solver(self, arg: Enum_TransportLinearSolver, /) -> None: ...

    @property
    def transport_preconditioner(self) -> Enum_TransportPreconditioner: ...

    @transport_preconditioner.setter
    def transport_preconditioner(self, arg: Enum_TransportPreconditioner, /) -> None: ...

    def validate(self) -> None: ...

class OutputControl:
    def __init__(self) -> None: ...

    @property
    def write_vtk_volume(self) -> bool: ...

    @write_vtk_volume.setter
    def write_vtk_volume(self, arg: bool, /) -> None: ...

    @property
    def write_vtk_face(self) -> bool: ...

    @write_vtk_face.setter
    def write_vtk_face(self, arg: bool, /) -> None: ...

    @property
    def output_mode(self) -> Enum_OutputMode: ...

    @output_mode.setter
    def output_mode(self, arg: Enum_OutputMode, /) -> None: ...

    @property
    def vtk_output_interval(self) -> float: ...

    @vtk_output_interval.setter
    def vtk_output_interval(self, arg: float, /) -> None: ...

    @property
    def vtk_output_times(self) -> list[float]: ...

    @vtk_output_times.setter
    def vtk_output_times(self, arg: Sequence[float], /) -> None: ...

    @property
    def use_csv_format(self) -> bool: ...

    @use_csv_format.setter
    def use_csv_format(self, arg: bool, /) -> None: ...

    @property
    def write_production_file(self) -> bool: ...

    @write_production_file.setter
    def write_production_file(self, arg: bool, /) -> None: ...

    @property
    def write_bhp_file(self) -> bool: ...

    @write_bhp_file.setter
    def write_bhp_file(self, arg: bool, /) -> None: ...

    @property
    def write_pressure_drop_file(self) -> bool: ...

    @write_pressure_drop_file.setter
    def write_pressure_drop_file(self, arg: bool, /) -> None: ...

    @property
    def write_sim_data_report(self) -> bool: ...

    @write_sim_data_report.setter
    def write_sim_data_report(self, arg: bool, /) -> None: ...

    @property
    def text_output_interval(self) -> float: ...

    @text_output_interval.setter
    def text_output_interval(self, arg: float, /) -> None: ...

class ScalingParameters:
    @property
    def length_ref(self) -> float: ...

    @property
    def velocity_ref(self) -> float: ...

    @property
    def perm_ref(self) -> float: ...

    @property
    def visc_ref(self) -> float: ...

    @property
    def density_ref(self) -> float: ...

    @property
    def surf_fluid_ref(self) -> float: ...

    @property
    def surf_rock_ref(self) -> float: ...

    @property
    def cap_pressure_ref(self) -> float: ...

    @property
    def n_max(self) -> float: ...

    @property
    def time_advective(self) -> float: ...

    @property
    def pressure_ref(self) -> float: ...

    @property
    def mobility_ref(self) -> float: ...

    @property
    def N_g(self) -> float: ...

    @property
    def N_c(self) -> float: ...

class SimulationData:
    def __init__(self) -> None: ...

    @property
    def global_settings(self) -> GlobalSettings: ...

    @global_settings.setter
    def global_settings(self, arg: GlobalSettings, /) -> None: ...

    @property
    def orthogonal_geometry(self) -> OrthogonalGeometry: ...

    @orthogonal_geometry.setter
    def orthogonal_geometry(self, arg: OrthogonalGeometry, /) -> None: ...

    @property
    def unstructured_geometry(self) -> UnstructuredGeometry: ...

    @unstructured_geometry.setter
    def unstructured_geometry(self, arg: UnstructuredGeometry, /) -> None: ...

    @property
    def rock_properties(self) -> RockProperties: ...

    @rock_properties.setter
    def rock_properties(self, arg: RockProperties, /) -> None: ...

    @property
    def fluid_properties(self) -> FluidProperties: ...

    @fluid_properties.setter
    def fluid_properties(self, arg: FluidProperties, /) -> None: ...

    @property
    def rock_fluid_interactions(self) -> RockFluidInteractions: ...

    @rock_fluid_interactions.setter
    def rock_fluid_interactions(self, arg: RockFluidInteractions, /) -> None: ...

    @property
    def eor_mechanisms(self) -> EORMechanisms: ...

    @eor_mechanisms.setter
    def eor_mechanisms(self, arg: EORMechanisms, /) -> None: ...

    @property
    def initial_and_boundary_conditions(self) -> InitialAndBoundaryConditions: ...

    @initial_and_boundary_conditions.setter
    def initial_and_boundary_conditions(self, arg: InitialAndBoundaryConditions, /) -> None: ...

    @property
    def well_set_config(self) -> WellSetConfig: ...

    @well_set_config.setter
    def well_set_config(self, arg: WellSetConfig, /) -> None: ...

    @property
    def time_data(self) -> TimeData: ...

    @time_data.setter
    def time_data(self, arg: TimeData, /) -> None: ...

    @property
    def execution_control(self) -> ExecutionControl: ...

    @execution_control.setter
    def execution_control(self, arg: ExecutionControl, /) -> None: ...

    @property
    def output_control(self) -> OutputControl: ...

    @output_control.setter
    def output_control(self, arg: OutputControl, /) -> None: ...

    @property
    def scaling_parameters(self) -> ScalingParameters: ...

    def validate(self) -> None: ...

    def perform_setup(self) -> None:
        """Executes internal physics and bindings setup."""

    def print_info(self) -> None:
        """
        Prints a detailed summary of the simulation data, solver setup, and physics.
        """

    def load_prm(self, filename: str, skip_undefined: bool = True) -> None:
        """
        Carrega configurações físicas alocando poços e bordas dinâmicas preventivamente.
        """

    def read_prm(self, filename: str, skip_undefined: bool = True) -> None:
        """Alias for load_prm."""

    def save_prm(self, filename: str) -> None:
        """Guarda a configuração atual da memória num ficheiro .prm legível."""

    def set_custom_rel_perm_functions(self, krw_func: Callable[[float, SimulationData], float], krg_func: Callable[[float, SimulationData], float], resolution: int = 100) -> None:
        """
        Discretizes custom Krw and Krg functions into native tables on SimulationData.
        """

    def set_custom_capillary_pressure(self, cp_func: Callable[[float, SimulationData], float], resolution: int = 100) -> None:
        """
        Discretizes custom Capillary Pressure into native table on SimulationData.
        """

    def set_gas_pressure_density(self, rho_func: Callable[[float, SimulationData], float], p_min: float = 100000.0, p_max: float = 50000000.0, resolution: int = 100) -> None:
        """
        Discretizes custom gas equation of state into native density table on SimulationData.
        """

    def set_custom_gas_density(self, rho_func: Callable[[float, SimulationData], float], p_min: float = 100000.0, p_max: float = 50000000.0, resolution: int = 100) -> None:
        """Alias for set_gas_pressure_density."""

    def __repr__(self) -> str: ...

class FossilSimulator2D:
    def __init__(self, data: SimulationData, out_dir: str = 'output') -> None: ...

    def get_mesh_data(self) -> dict:
        """
        Extracts vertices, VTK connectivity, and centroids directly from the simulator.
        """

    def run(self) -> None: ...

    def get_transport_data(self, arg: Enum_Variable, /) -> list[float]: ...

    def get_darcy_data(self) -> dict: ...

    def get_simulation_data(self) -> SimulationData:
        """
        Returns the simulation parameters in physical SI units (dimensional clone).
        """

    def get_dimensional_simulation_data(self) -> SimulationData:
        """Returns the simulation parameters in physical SI units."""

    def get_internal_simulation_data(self) -> SimulationData:
        """Returns the internal dimensionless simulation data used by solvers."""

    def set_step_callback(self, callback: object) -> None:
        """
        Registers a Python function to be executed at the end of each time step.
        """

    def __repr__(self) -> str: ...

    def set_well_bhp(self, well_name: str, bhp_pascal: float) -> None:
        """Sets physical well Bottom-Hole Pressure (BHP) in Pascals [Pa]."""

    def set_well_rate(self, well_name: str, rate_m3_s: float) -> None:
        """Sets physical total volumetric flow rate in [m^3/s]."""

    @overload
    def set_boundary_darcy_value(self, boundary_name: str, physical_value: float) -> None:
        """Sets physical Darcy boundary value (Pa or m/s) by boundary name."""

    @overload
    def set_boundary_darcy_value(self, boundary_id: int, physical_value: float) -> None:
        """Sets physical Darcy boundary value (Pa or m/s) by boundary ID."""

    @overload
    def get_boundary_darcy_value(self, boundary_name: str) -> float:
        """Gets physical Darcy boundary value (Pa or m/s) by boundary name."""

    @overload
    def get_boundary_darcy_value(self, boundary_id: int) -> float:
        """Gets physical Darcy boundary value (Pa or m/s) by boundary ID."""

    @overload
    def set_boundary_darcy_type(self, boundary_name: str, boundary_type: Enum_DarcyBoundaryType) -> None:
        """Sets Darcy boundary type (DIRICHLET or NEUMANN) by boundary name."""

    @overload
    def set_boundary_darcy_type(self, boundary_id: int, boundary_type: Enum_DarcyBoundaryType) -> None:
        """Sets Darcy boundary type (DIRICHLET or NEUMANN) by boundary ID."""

    @overload
    def get_boundary_darcy_type(self, boundary_name: str) -> Enum_DarcyBoundaryType:
        """Gets Darcy boundary type (DIRICHLET or NEUMANN) by boundary name."""

    @overload
    def get_boundary_darcy_type(self, boundary_id: int) -> Enum_DarcyBoundaryType:
        """Gets Darcy boundary type (DIRICHLET or NEUMANN) by boundary ID."""

    @overload
    def set_boundary_transport_value(self, boundary_name: str, var: Enum_Variable, physical_value: float) -> None:
        """Sets physical transport boundary condition by boundary name."""

    @overload
    def set_boundary_transport_value(self, boundary_id: int, var: Enum_Variable, physical_value: float) -> None:
        """Sets physical transport boundary condition by boundary ID."""

    @overload
    def get_boundary_transport_value(self, boundary_name: str, var: Enum_Variable) -> float:
        """Gets physical transport boundary condition value by boundary name."""

    @overload
    def get_boundary_transport_value(self, boundary_id: int, var: Enum_Variable) -> float:
        """Gets physical transport boundary condition value by boundary ID."""

    @overload
    def set_boundary_transport_type(self, boundary_name: str, boundary_type: Enum_TransportBoundaryType) -> None:
        """Sets transport boundary type by boundary name."""

    @overload
    def set_boundary_transport_type(self, boundary_id: int, boundary_type: Enum_TransportBoundaryType) -> None:
        """Sets transport boundary type by boundary ID."""

    @overload
    def get_boundary_transport_type(self, boundary_name: str) -> Enum_TransportBoundaryType:
        """Gets transport boundary type by boundary name."""

    @overload
    def get_boundary_transport_type(self, boundary_id: int) -> Enum_TransportBoundaryType:
        """Gets transport boundary type by boundary ID."""

    def get_boundary_names(self) -> list[str]:
        """Returns a list of all boundary names in the model."""

    def get_well_names(self) -> list[str]:
        """Returns a list of all active well names."""

    def get_well_operation(self, well_name: str) -> Enum_WellOperation:
        """Returns the operational state (OPEN or SHUT_IN) of the well."""

    def set_well_operation(self, well_name: str, operation: Enum_WellOperation) -> None:
        """Changes the operational state of a well."""

    def get_current_well_bhp(self, well_name: str) -> float:
        """
        Returns the instantaneous Bottom-Hole Pressure (BHP) of the well in Pascals [Pa].
        """

    def get_current_well_rate(self, well_name: str) -> float:
        """Returns the instantaneous volumetric flow rate of the well in [m^3/s]."""

    def get_current_pressure_drop(self) -> dict:
        """
        Returns instantaneous reservoir pressure drop statistics in Pascals [Pa].
        """

    def get_current_production_data(self) -> dict:
        """
        Returns instantaneous global production/injection rates and fluid inventories.
        """

    def set_custom_rel_perm_functions(self, krw_func: Callable[[float, SimulationData], float], krg_func: Callable[[float, SimulationData], float], resolution: int = 100) -> None:
        """
        Injects custom Krw and Krg functions evaluating them with the standard FOSSIL signature (sw, sim_data).
        """

    def set_custom_capillary_pressure(self, cp_func: Callable[[float, SimulationData], float], resolution: int = 100) -> None:
        """
        Injects a custom Capillary Pressure function evaluating with (sw, sim_data) returning [Pa].
        """

    def set_gas_pressure_density(self, rho_func: Callable[[float, SimulationData], float], p_min: float = 100000.0, p_max: float = 50000000.0, resolution: int = 100) -> None:
        """
        Injects a custom gas equation of state rho_g(P) discretizing it into a native C++ table.
        """

    def set_custom_gas_density(self, rho_func: Callable[[float, SimulationData], float], p_min: float = 100000.0, p_max: float = 50000000.0, resolution: int = 100) -> None:
        """Alias for set_gas_pressure_density."""

class FossilSimulator3D:
    def __init__(self, data: SimulationData, out_dir: str = 'output') -> None: ...

    def get_mesh_data(self) -> dict:
        """
        Extracts vertices, VTK connectivity, and centroids directly from the simulator.
        """

    def run(self) -> None: ...

    def get_transport_data(self, arg: Enum_Variable, /) -> list[float]: ...

    def get_darcy_data(self) -> dict: ...

    def get_simulation_data(self) -> SimulationData:
        """
        Returns the simulation parameters in physical SI units (dimensional clone).
        """

    def get_dimensional_simulation_data(self) -> SimulationData:
        """Returns the simulation parameters in physical SI units."""

    def get_internal_simulation_data(self) -> SimulationData:
        """Returns the internal dimensionless simulation data used by solvers."""

    def set_step_callback(self, callback: object) -> None:
        """
        Registers a Python function to be executed at the end of each time step.
        """

    def __repr__(self) -> str: ...

    def set_well_bhp(self, well_name: str, bhp_pascal: float) -> None:
        """Sets physical well Bottom-Hole Pressure (BHP) in Pascals [Pa]."""

    def set_well_rate(self, well_name: str, rate_m3_s: float) -> None:
        """Sets physical total volumetric flow rate in [m^3/s]."""

    @overload
    def set_boundary_darcy_value(self, boundary_name: str, physical_value: float) -> None:
        """Sets physical Darcy boundary value (Pa or m/s) by boundary name."""

    @overload
    def set_boundary_darcy_value(self, boundary_id: int, physical_value: float) -> None:
        """Sets physical Darcy boundary value (Pa or m/s) by boundary ID."""

    @overload
    def get_boundary_darcy_value(self, boundary_name: str) -> float:
        """Gets physical Darcy boundary value (Pa or m/s) by boundary name."""

    @overload
    def get_boundary_darcy_value(self, boundary_id: int) -> float:
        """Gets physical Darcy boundary value (Pa or m/s) by boundary ID."""

    @overload
    def set_boundary_darcy_type(self, boundary_name: str, boundary_type: Enum_DarcyBoundaryType) -> None:
        """Sets Darcy boundary type (DIRICHLET or NEUMANN) by boundary name."""

    @overload
    def set_boundary_darcy_type(self, boundary_id: int, boundary_type: Enum_DarcyBoundaryType) -> None:
        """Sets Darcy boundary type (DIRICHLET or NEUMANN) by boundary ID."""

    @overload
    def get_boundary_darcy_type(self, boundary_name: str) -> Enum_DarcyBoundaryType:
        """Gets Darcy boundary type (DIRICHLET or NEUMANN) by boundary name."""

    @overload
    def get_boundary_darcy_type(self, boundary_id: int) -> Enum_DarcyBoundaryType:
        """Gets Darcy boundary type (DIRICHLET or NEUMANN) by boundary ID."""

    @overload
    def set_boundary_transport_value(self, boundary_name: str, var: Enum_Variable, physical_value: float) -> None:
        """Sets physical transport boundary condition by boundary name."""

    @overload
    def set_boundary_transport_value(self, boundary_id: int, var: Enum_Variable, physical_value: float) -> None:
        """Sets physical transport boundary condition by boundary ID."""

    @overload
    def get_boundary_transport_value(self, boundary_name: str, var: Enum_Variable) -> float:
        """Gets physical transport boundary condition value by boundary name."""

    @overload
    def get_boundary_transport_value(self, boundary_id: int, var: Enum_Variable) -> float:
        """Gets physical transport boundary condition value by boundary ID."""

    @overload
    def set_boundary_transport_type(self, boundary_name: str, boundary_type: Enum_TransportBoundaryType) -> None:
        """Sets transport boundary type by boundary name."""

    @overload
    def set_boundary_transport_type(self, boundary_id: int, boundary_type: Enum_TransportBoundaryType) -> None:
        """Sets transport boundary type by boundary ID."""

    @overload
    def get_boundary_transport_type(self, boundary_name: str) -> Enum_TransportBoundaryType:
        """Gets transport boundary type by boundary name."""

    @overload
    def get_boundary_transport_type(self, boundary_id: int) -> Enum_TransportBoundaryType:
        """Gets transport boundary type by boundary ID."""

    def get_boundary_names(self) -> list[str]:
        """Returns a list of all boundary names in the model."""

    def get_well_names(self) -> list[str]:
        """Returns a list of all active well names."""

    def get_well_operation(self, well_name: str) -> Enum_WellOperation:
        """Returns the operational state (OPEN or SHUT_IN) of the well."""

    def set_well_operation(self, well_name: str, operation: Enum_WellOperation) -> None:
        """Changes the operational state of a well."""

    def get_current_well_bhp(self, well_name: str) -> float:
        """
        Returns the instantaneous Bottom-Hole Pressure (BHP) of the well in Pascals [Pa].
        """

    def get_current_well_rate(self, well_name: str) -> float:
        """Returns the instantaneous volumetric flow rate of the well in [m^3/s]."""

    def get_current_pressure_drop(self) -> dict:
        """
        Returns instantaneous reservoir pressure drop statistics in Pascals [Pa].
        """

    def get_current_production_data(self) -> dict:
        """
        Returns instantaneous global production/injection rates and fluid inventories.
        """

    def set_custom_rel_perm_functions(self, krw_func: Callable[[float, SimulationData], float], krg_func: Callable[[float, SimulationData], float], resolution: int = 100) -> None:
        """
        Injects custom Krw and Krg functions evaluating them with the standard FOSSIL signature (sw, sim_data).
        """

    def set_custom_capillary_pressure(self, cp_func: Callable[[float, SimulationData], float], resolution: int = 100) -> None:
        """
        Injects a custom Capillary Pressure function evaluating with (sw, sim_data) returning [Pa].
        """

    def set_gas_pressure_density(self, rho_func: Callable[[float, SimulationData], float], p_min: float = 100000.0, p_max: float = 50000000.0, resolution: int = 100) -> None:
        """
        Injects a custom gas equation of state rho_g(P) discretizing it into a native C++ table.
        """

    def set_custom_gas_density(self, rho_func: Callable[[float, SimulationData], float], p_min: float = 100000.0, p_max: float = 50000000.0, resolution: int = 100) -> None:
        """Alias for set_gas_pressure_density."""

def FossilSimulator(data: SimulationData, out_dir: str = 'output') -> FossilSimulator2D | FossilSimulator3D: ...

def print_info(data: SimulationData) -> None:
    """
    Prints a detailed summary of the simulation data, solver setup, and physics.
    """
