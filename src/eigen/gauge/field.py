from typing import Protocol, Any, ContextManager
from contextvars import ContextVar

class Field(Protocol):
    """
    The Field Protocol defines how Operators interact in the Spacetime.
    It governs the physics of interaction (>> , | , &, +).
    """
    def flow(self, left: Any, right: Any) -> Any:
        """ >> Operator: Flow / Evolution """
        ...

    def choice(self, left: Any, right: Any) -> Any:
        """ | Operator: Choice / Fallback """
        ...
    
    def ensemble(self, left: Any, right: Any) -> Any:
        """ & Operator: Ensemble / Parallel """
        ...
        
    def interference(self, left: Any, right: Any) -> Any:
        """ + Operator: Interference / Superposition """
        ...

# The Global Field Context
_vacuum = ContextVar("eigen_field", default=None)

def current_field() -> Field:
    f = _vacuum.get()
    if f is None:
        raise RuntimeError("Vacuum State Detected: No Field is active.")
    return f

def activate_field(field: Field):
    _vacuum.set(field)
