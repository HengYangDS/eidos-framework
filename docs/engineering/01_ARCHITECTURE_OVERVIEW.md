# Engineering Track: Architecture Overview

Status: initial stub (will be expanded). Baseline: Python >= 3.14.

- Core modules:
  - Dynamics: `eigen.dynamics` (Hamiltonian, Interference)
  - Gauge: `eigen.gauge` (Field protocol, operator algebra >> | & +)
  - Techne: `eigen.techne` (Sources, Operators, Sinks, Ports)
- Runtime activation is explicit:

```python
from eigen.runtime import activate
activate()
```

- Composition:
  - Flow (A >> B) → sequence into a Hamiltonian
  - Choice (A | B) → fallback on None/exception
  - Ensemble (A & B) → structured concurrency with TaskGroup
  - Interference (A + B) → additive superposition
