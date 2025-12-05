from typing import Any
from ..zero.symbolism.types import Monad, Context

class FS:
    """
    Eidos File System / Data Protocol Utilities.
    """
    @staticmethod
    def wrap(data: Any, meta: dict = None) -> Monad:
        """Wraps raw data into an Monad."""
        ctx = Context(meta=meta or {})
        return Monad(payload=data, context=ctx)

    @staticmethod
    def unwrap(envelope: Monad) -> Any:
        """Extracts payload from Monad."""
        return envelope.payload
