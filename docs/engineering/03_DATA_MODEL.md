# Engineering Track: Data Model

Status: initial stub. Baseline: Python >= 3.14.

Envelope proposal:
- headers: metadata, correlation IDs, schema version
- context: execution context, auth, resource hints
- payload: actual data (row, dict, Tensor)

Operators should pass envelope through or transform payload while preserving headers/context when applicable.

Activation:
```python
from eigen.runtime import activate
activate()
```
