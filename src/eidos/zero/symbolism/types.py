from dataclasses import dataclass, field
from typing import Any
from collections.abc import Callable
import uuid
from datetime import datetime, timezone

@dataclass(frozen=True)
class Context:
    """Immutable context carried by the Monad."""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = "default"
    user_id: str | None = None
    meta: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class Effect:
    """Represents a side effect to be executed."""
    type: str
    payload: Any

@dataclass
class Monad[T]:
    """
    The Monad of Eidos.
    Carries data (payload) along with its context and pending effects.
    """
    payload: T
    context: Context = field(default_factory=Context)
    effects: list[Effect] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def map[U](self, fn: Callable[[T], U]) -> "Monad[U]":
        """Functor map."""
        return Monad(
            payload=fn(self.payload),
            context=self.context,
            effects=self.effects,
            timestamp=self.timestamp
        )

    def bind[U](self, fn: Callable[[T], "Monad[U]"]) -> "Monad[U]":
        """Monad bind."""
        return fn(self.payload)
