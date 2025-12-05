from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar, Dict, List, Optional
import uuid
from datetime import datetime

T = TypeVar("T")

@dataclass(frozen=True)
class Context:
    """Immutable context carried by the Monad."""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default"
    user_id: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Effect:
    """Represents a side effect to be executed."""
    type: str
    payload: Any

@dataclass
class Monad(Generic[T]):
    """
    The Monad of Eidos.
    Carries data (payload) along with its context and pending effects.
    """
    payload: T
    context: Context = field(default_factory=Context)
    effects: List[Effect] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def map(self, fn) -> "Monad":
        """Functor map."""
        return Monad(
            payload=fn(self.payload),
            context=self.context,
            effects=self.effects,
            timestamp=self.timestamp
        )

    def bind(self, fn) -> "Monad":
        """Monad bind."""
        return fn(self.payload)
