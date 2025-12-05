from collections.abc import AsyncIterator
from typing import Any
from pathlib import Path
import asyncio
from ...gauge.symmetry import OperatorMixin

class FileSource(OperatorMixin):
    """
    A Fermion that reads data from a local file.
    Type: Operator[Any, AsyncIterator[str]]
    """
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.path = Path(path)
        self.encoding = encoding
        self.name = f"FileSource({self.path.name})"

    async def __call__(self, _: Any) -> AsyncIterator[str]:
        if not self.path.exists():
            raise FileNotFoundError(f"{self.path} does not exist")
        return self._stream()

    async def _stream(self) -> AsyncIterator[str]:
        # Synchronous read wrapped in async generator
        with open(self.path, "r", encoding=self.encoding) as f:
            for line in f:
                # Simulate async yield to allow event loop to breathe
                await asyncio.sleep(0) 
                yield line.strip()
