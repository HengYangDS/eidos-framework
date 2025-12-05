from collections.abc import AsyncIterator
from typing import Any
from ...gauge.symmetry import OperatorMixin
import csv
from pathlib import Path
import asyncio

class CSVSink(OperatorMixin):
    """
    A Fermion that collapses a quantum state (Stream) into a CSV file.
    Type: Operator[AsyncIterator[dict] | list[dict], Path]
    """
    def __init__(self, file_path: str, headers: list[str] = None):
        self.file_path = Path(file_path)
        self.headers = headers
        self.name = f"CSVSink({self.file_path.name})"

    async def __call__(self, input: AsyncIterator[dict] | list[dict] | dict) -> Path:
        mode = 'w'
        # We need to handle the file opening.
        # For streaming, we keep file open.
        
        count = 0
        with open(self.file_path, mode, newline='', encoding='utf-8') as f:
            writer = None
            
            async def write_item(item):
                nonlocal writer, count
                if writer is None:
                    fieldnames = self.headers or item.keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                writer.writerow(item)
                count += 1

            if isinstance(input, AsyncIterator):
                async for item in input:
                    await write_item(item)
            elif isinstance(input, list):
                for item in input:
                    await write_item(item)
            else:
                # Single item?
                await write_item(input)
                
        print(f"[{self.name}] Wrote {count} records.")
        return self.file_path
