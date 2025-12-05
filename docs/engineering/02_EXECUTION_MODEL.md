# Engineering Track: Execution Model

Status: initial stub. Baseline: Python >= 3.14.

Topics to be detailed:
- Sync vs Async semantics (Operators are async callables)
- Stream vs Batch handling (AsyncIterator vs list vs scalar)
- Backpressure considerations and batching
- Structured concurrency via asyncio.TaskGroup in Ensemble (&)

Activation is explicit:
```python
from eigen.runtime import activate
activate()
```
