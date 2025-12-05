from typing import Protocol, runtime_checkable, Any, TypeVar
from .field import current_field

I = TypeVar("I")
O = TypeVar("O")
R = TypeVar("R")

@runtime_checkable
class OperatorMixin(Protocol[I, O]):
    """
    Gauge Symmetry Protocol: Defines the invariant laws of operators.
    Delegates the actual interaction physics to the active Field.
    """
    async def __call__(self, input: I) -> O: ...

    def __rshift__(self, other: "OperatorMixin[O, R]") -> "OperatorMixin[I, R]":
        """ >> Operator: Flow / Evolution """
        return current_field().flow(self, other)

    def __or__(self, other: "OperatorMixin[I, O]") -> "OperatorMixin[I, O]":
        """ | Operator: Fallback / Choice """
        return current_field().choice(self, other)
    
    def __and__(self, other: "OperatorMixin[I, O]") -> "OperatorMixin[I, list[O]]":
        """ & Operator: Ensemble / Parallel """
        return current_field().ensemble(self, other)
        
    def __add__(self, other: "OperatorMixin[I, O]") -> "OperatorMixin[I, O]":
        """ + Operator: Interference / Superposition """
        return current_field().interference(self, other)
