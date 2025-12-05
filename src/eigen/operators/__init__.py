from ..core import Operator
from typing import Any
from collections.abc import AsyncIterator

class Window(Operator):
    """
    Accumulates items into a window (Time or Count).
    """
    def __init__(self, size: str):
        self.size = size
        
    async def __call__(self, input: Any) -> Any:
        # Mock windowing
        return input

__all__ = ["Window"]
