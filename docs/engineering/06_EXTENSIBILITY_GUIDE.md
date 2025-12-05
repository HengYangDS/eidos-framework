# Engineering Track: Extensibility Guide

Status: initial stub. Baseline: Python >= 3.14.

How to add new components:
- Operator: implement `async def __call__(self, input) -> output` and inherit `OperatorMixin` protocol implicitly by signature.
- Source: an Operator that ignores input and returns a value/AsyncIterator.
- Sink: an Operator that persists input and returns a final Path/ID.
- Port: boundary adaptors (e.g., HTTPPort) that bind a pipeline and expose it externally.

Conventions:
- Use collections.abc types for AsyncIterator/Awaitable/Callable in annotations.
- Ensure non-blocking behavior (no long CPU in event loop).
- Support both Stream (AsyncIterator) and List when applicable.

Activation:
```python
from eigen.runtime import activate
activate()
```
