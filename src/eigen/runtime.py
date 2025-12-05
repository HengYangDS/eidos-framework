from .gauge.field import activate_field, Field
from .dynamics.hamiltonian import QuantumField

def activate(field: Field | None = None) -> None:
    """
    Activate the Eigen runtime by setting the current Field.
    Defaults to QuantumField if no field is provided.
    """
    activate_field(field or QuantumField())

__all__ = ["activate"]
