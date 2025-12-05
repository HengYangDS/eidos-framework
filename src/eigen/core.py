from .gauge.symmetry import OperatorMixin
from .dynamics.hamiltonian import Hamiltonian
import numpy as np
from typing import Any

# Alias OperatorMixin to Operator as it's the public API
class Operator(OperatorMixin):
    """
    The Fundamental Particle of Logic (Fermion).
    Everything in Eigen is an Operator.
    """
    pass

class Flow(Hamiltonian):
    """
    A Flow is a sequence of Operators (Hamiltonian).
    """
    pass

class Tensor:
    """
    A multi-dimensional array of data (Fermion).
    Wraps numpy or other backends.
    """
    def __init__(self, data: Any = None, schema: Any = None):
        self.data = np.array(data) if data is not None else np.array([])
        self.schema = schema

    def dot(self, other: Any) -> "Tensor":
        if isinstance(other, Tensor):
            return Tensor(np.dot(self.data, other.data))
        return Tensor(np.dot(self.data, other))

    def __add__(self, other: Any) -> "Tensor":
        if isinstance(other, Tensor):
            return Tensor(self.data + other.data)
        return Tensor(self.data + other)
    
    def __repr__(self):
        return f"Tensor(shape={self.data.shape})"


__all__ = [
    "Operator",
    "Flow",
    "Tensor",
]
