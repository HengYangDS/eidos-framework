from ..core import Operator
from typing import Any
from collections.abc import AsyncIterator

class Stream:
    """
    Factory for creating Data Streams (Fermions).
    """
    @staticmethod
    def from_file(path: str) -> AsyncIterator:
        # Mock
        async def _gen():
            yield "data"
        return _gen()
        
    @staticmethod
    def from_keyboard() -> Any:
        pass
        
    @staticmethod
    def from_fastq(path: str) -> Any:
        pass

class Quantizer(Operator):
    """
    Downsamples a signal.
    """
    def __init__(self, interval: str, method: str):
        self.interval = interval
        self.method = method
        
    async def __call__(self, input: Any) -> Any:
        return input
