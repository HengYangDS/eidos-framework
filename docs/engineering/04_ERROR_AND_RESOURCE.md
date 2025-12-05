# Engineering Track: Error & Resource Semantics

Status: initial stub. Baseline: Python >= 3.14.

- Timeouts: wrap awaits with asyncio.wait_for where needed (HTTPPort supports optional timeout)
- Retries: compose with Choice (|) and custom retry operators (future)
- Cancellation: cooperative via asyncio; operators should not block the loop
- Idempotency: recommend idempotent sinks; add idempotency keys in envelope (future)

Activation:
```python
from eigen.runtime import activate
activate()
```
