# Book III: LOGOS - Gauge Theory & Protocols

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "The laws of logic are the geometry of the mind."

## 3.1 The Logos Layer (Dao)

The **Logos** (Dao) is the highest layer of the Eigen hierarchy. It defines the
**Gauge Symmetry** of the system—the protocols that must hold true regardless of
implementation.

**Strict Rules for Logos:**
1.  **Zero Dependencies**: Logos must depend ONLY on the Python Standard
    Library. No `pydantic`, no `numpy`.
2.  **Pure Abstraction**: Logos contains no implementation logic (except default
    mixin behavior).
3.  **Type Safety**: All definitions must be statically type-checkable.

## 3.2 The Universal Operator

The fundamental particle of Eigen is the `Operator`. In Quantum Field Theory, an
operator acts on a state to transform it. In Eigen, it acts on Data.

### The Protocol Definition (Python 3.14)

We use PEP 695 Generics to define the Universal Operator.

```python
from typing import Protocol, runtime_checkable, Self, Any, overload
from abc import abstractmethod

@runtime_checkable
class Operator[I, O]:
    """
    The Fundamental Gauge Boson.
    Transmutes Input I into Output O.
    """
    
    @abstractmethod
    async def __call__(self, input: I, /) -> O:
        """
        The Action.
        Collapse the wavefunction of I to produce O.
        """
        ...

    # ----------------------------------------------------------------

    # The Ring of Actions (Algebraic Overloads)

    # ----------------------------------------------------------------

    # --- Flow (Sequence) ---
    def __rshift__[R] -> "Operator[I, R]":
        """Flow (>>): Composition f(g(x)). Causality."""
        ...

    def __lshift__[R] -> "Operator[R, O]":
        """Feedback (<<): Cybernetic Loop."""
        ...

    # --- Choice (Superposition) ---
    def __or__(self, other: "Operator[I, O]") -> "Operator[I, O]":
        """Choice (|): Alternative Paths (A or B)."""
        ...
    
    def __xor__(self, other: "Operator[I, O]") -> "Operator[I, O]":
        """Interrupt (^): Preemption or Exclusive Or."""
        ...

    # --- Ensemble (Parallelism) ---
    def __and__[R] -> "Operator[I, tuple[O, R]]":
        """Entanglement (&): Tensor Product (A and B)."""
        ...

    # --- Arithmetic (Interference) ---
    def __add__(self, other: "Operator[I, O]") -> "Operator[I, O]":
        """Addition (+): Constructive Interference (Merge)."""
        ...

    def __sub__(self, other: "Operator[I, Any]") -> "Operator[I, O]":
        """Subtraction (-): Destructive Interference (Constraint/Filter)."""
        ...

    def __mul__(self, factor: int | "Operator") -> "Operator[I, list[O]]":
        """Multiplication (*): Amplification or Cartesian Product."""
        ...

    def __truediv__(self, divisor: int) -> "Operator[I, list[O]]":
        """Division (/): Sampling or Sharding."""
        ...
        
    def __floordiv__(self, divisor: Any) -> "Operator[I, Any]":
        """Quantization (//): Batching or Discretization."""
        ...

    # --- Optics (Lensing) ---
    def __getitem__(self, key: Any) -> "Operator[I, Any]":
        """Lens ([]): Projection, Slicing, or Type Casting."""
        ...

    # --- Logic (Demons) ---
    def __gt__(self, other: Any) -> "Operator[I, bool]":
        """Threshold (>): High-pass Filter."""
        ...

    def __lt__(self, other: Any) -> "Operator[I, bool]":
        """Threshold (<): Low-pass Filter."""
        ...

    # --- Field (Context) ---
    def __mod__(self, context: dict[str, Any]) -> "Operator[I, O]":
        """Gauge Field (%): Context Binding / Parameter Injection."""
        ...

    def __matmul__(self, observer: Any) -> "Operator[I, O]":
        """Measurement (@): Projection to Sink / Logging."""
        ...
    
    # --- Symmetries (Unary) ---
    def __invert__(self) -> "Operator[I, O]":
        """Antimatter (~): Logical NOT or Undo."""
        ...
    
    def __neg__(self) -> "Operator[I, O]":
        """Time Reversal (-): Inverse Operation."""
        ...
    
    def __pos__(self) -> "Operator[I, O]":
        """Normalization (+): Unitary Enforcement."""
        ...

```

### 3.2.1 The Symmetry Mixin

To avoid implementing these magic methods in every class, we provide a
`Symmetry` mixin. This is the **Gauge Transform Generator**.

```python
class Symmetry[I, O]:
    """
    Mixin that provides default implementations for the Algebra of Action.
    Inherit from this to become a Citizen of the Eigen Universe.
    """

    # Flow
    def __rshift__(self, other): return Hamiltonian.compose(self, other)
    def __lshift__(self, other): return Hamiltonian.feedback(self, other)
    
    # Choice
    def __or__(self, other): return Hamiltonian.choose(self, other)
    def __xor__(self, other): return Hamiltonian.interrupt(self, other)
    
    # Ensemble
    def __and__(self, other): return Hamiltonian.entangle(self, other)
    
    # Arithmetic
    def __add__(self, other): return Hamiltonian.merge(self, other)
    def __sub__(self, other): return Hamiltonian.constrain(self, other)
    def __mul__(self, other): return Hamiltonian.amplify(self, other)
    def __truediv__(self, other): return Hamiltonian.sample(self, other)
    def __floordiv__(self, other): return Hamiltonian.batch(self, other)
    
    # Optics
    def __getitem__(self, key): return Hamiltonian.project(self, key)
    
    # Logic
    def __gt__(self, other): return Hamiltonian.filter(self, ">", other)
    def __lt__(self, other): return Hamiltonian.filter(self, "<", other)
    
    # Field
    def __mod__(self, context): return Hamiltonian.bind(self, context)
    def __matmul__(self, observer): return Hamiltonian.measure(self, observer)
    
    # Unary
    def __invert__(self): return Hamiltonian.invert(self)
    def __neg__(self): return Hamiltonian.reverse(self)
    def __pos__(self): return Hamiltonian.normalize(self)

```

## 3.3 The Knowledge Tensor (State)

If `Operator` is the Boson, then `Knowledge` is the Fermion. It is the immutable
state carrier.

In Eigen, we treat Knowledge not as a dictionary, but as a **Tensor** in a high-
dimensional semantic space.

```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4, UUID

@dataclass(frozen=True, slots=True)
class Knowledge[T]:
    """
    The Fermion.
    An immutable quantum of information.
    """
    content: T
    id: UUID = field(default_factory=uuid4)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    vector: list[float] | None = None  # The semantic embedding
    metadata: dict[str, Any] = field(default_factory=dict)

    def __add__(self, other: "Knowledge[T]") -> "Knowledge[T]":
        """Fusion: Merges two knowledge particles."""
        return Knowledge(
            content=self.content + other.content,
            metadata={**self.metadata, **other.metadata}
        )
        
    def __mul__(self, weight: float) -> "Knowledge[T]":
        """Scaling: Adjusts the importance (Action) of the particle."""
        return Knowledge(
            content=self.content,
            vector=[v * weight for v in self.vector] if self.vector else None,
            metadata=self.metadata
        )

```

## 3.4 The Field Protocol (Context)

A `Field` is a pervasive entity that exists everywhere in space-time (the
execution context). Examples include `Config`, `TraceID`, `UserSession`.

```python
@runtime_checkable
class Field[T]:
    """
    A Scalar or Vector Field.
    Provides context to Operators without explicit passing.
    """
    def get(self) -> T: ...
    
    def set(self, value: T) -> None: ...
    
    def context(self) -> Any:
        """Returns a context manager for scope-bound values."""
        ...

```

## 3.5 Static Analysis & Type Checking

Eigen leverages Python 3.14's advanced typing features to prove correctness at
compile time (Static Analysis).

### The Covariance of Output
The Output `O` is **Covariant**. If an operator produces `Dog`, it can be used
where `Animal` is expected.

```python
class Producer[+O](Protocol): ...

```

### The Contravariance of Input
The Input `I` is **Contravariant**. If an operator expects `Animal`, it can
handle `Dog`.

```python
class Consumer[-I](Protocol): ...

```

The Operator is thus a **Profunctor**: `Operator[-I, +O]`.
$$ Operator: I^{op} \times O \to Set $$

This mathematical rigor ensures that `source >> process >> sink` is only valid
if the types align perfectly, preventing "Runtime Entropy".

---
**Eigen Cosmology** | [Previous: Book II](02_GENESIS_AXIOMS.md) | [Index](../00_INDEX.md) | [Next: Book IV](04_LOGOS_INVARIANCE.md) | *© 2025 The Eigen High Council*