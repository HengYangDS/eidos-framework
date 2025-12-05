# Book XLIII: API Reference (Stable Public API v1.0)

Author: HENG Yang <hengyang.2003@tsinghua.org.cn>

This document is the authoritative reference for the current, production-focused API surface of Eigen. It reflects the modern baseline and avoids legacy or speculative symbols.

- Baseline: Python >= 3.14
- Style: async-first, modern typing (collections.abc), explicit runtime activation

## 0. Quick Start (Public API)

```python
from eigen import activate, Operator, Flow, Tensor, Map, Filter, Batch, Interference

activate()  # set the active Field (QuantumField)
```

- Operator algebra (implemented semantics):
  - a >> b → sequential composition (Flow/Hamiltonian)
  - a | b → fallback/choice (try a; on error or None, use b)
  - a & b → ensemble/parallel (structured concurrency; safe tee for async streams)
  - a + b → interference/superposition (additive combine of results)

## 1. Core

Module: `eigen.core`

- class Operator: marker base for all operators (Protocol via OperatorMixin)
- class Flow: alias of Hamiltonian (sequence of operators)
- class Tensor: thin ndarray wrapper with + and dot

Module: `eigen.runtime`

- activate(field: Field | None = None) -> None
  - Set the current Field; defaults to QuantumField.

Module: `eigen.gauge.symmetry`

- Protocol OperatorMixin[I, O]
  - Overloads >>, |, &, + by delegating to the active Field

Module: `eigen.gauge.field`

- Protocol Field
  - flow(left, right) → sequential composition
  - choice(left, right) → fallback/choice
  - ensemble(left, right) → parallel ensemble
  - interference(left, right) → additive superposition
- activate_field(field), current_field()
