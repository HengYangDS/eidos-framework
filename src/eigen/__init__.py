"""
Eigen: The Physics of Software.

Public API (stable):
- Core types: Operator, Flow, Tensor
- Runtime: activate
- Common operators: Map, Filter, Batch
- Physics constructs: Interference
"""

from .core import Operator, Flow, Tensor
from .runtime import activate
from .bosons import Map, Filter, Batch
from .physics import Interference

__all__ = [
    "Operator",
    "Flow",
    "Tensor",
    "activate",
    "Map",
    "Filter",
    "Batch",
    "Interference",
]
