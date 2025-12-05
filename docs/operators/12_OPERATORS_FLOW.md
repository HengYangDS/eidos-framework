# Book XII: OPERATORS - The Flow (Sequence)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "Time is what keeps everything from happening at once. Flow is what keeps
> logic from happening in parallel."
> — *The Causal Principle*

## 11.1 The Arrow of Time: Flow (>>)

The **Flow Operator** (`>>`, `__rshift__`) represents the sequential composition
of functions. It establishes the **Causal Order** of events in the Eigen
universe.

$$ (A \gg B) |\psi\rangle = B(A|\psi\rangle) $$

If $A$ emits a particle at time $t_0$, $B$ receives it at $t_1$ (where $t_1 >
t_0$). This enforces causality.

### 11.1.1 Algebraic Definition (The Monoid)

Let $\mathcal{O}$ be the set of all Operators. The pair $(\mathcal{O}, \gg)$
forms a **Monoid**:
1.  **Closure**: If $A, B \in \mathcal{O}$, then $A \gg B \in \mathcal{O}$.
2.  **Associativity**: $(A \gg B) \gg C = A \gg (B \gg C)$.
3.  **Identity**: There exists an identity operator $I$ such that $A \gg I = A$.

```python

# Python 3.14 Implementation
from eigen.logos import Operator, Hamiltonian

class Operator[I, O]:
    def __rshift__[R] -> "Hamiltonian[I, R]":
        return Hamiltonian.compose(self, next_op)

```

## 11.2 Monadic Binding

In functional programming terms, `>>` corresponds to the **Bind** operator
($>>=$) of the Eigen Monad.
It handles the "plumbing" between steps, abstracting away the complexity of:

### 11.2.1 Async Await
If step A is a coroutine, `>>` automatically awaits it before passing the result
to B.
You never write `await` in the top-level composition.

### 11.2.2 Tensor Promotion (Stream Mapping)
If operator $A$ emits a Stream (`AsyncIterator[T]`) and operator $B$ expects a
scalar `T`, the Flow operator automatically **promotes** $B$ to act on the
stream elements.

$$ (Source \gg Map) \cong \text{StreamMap}(Source, Map) $$

This is equivalent to raising the index of the tensor in physics ($T_i \to
T^{ij}$).

```python

# Automatic Stream Handling

# Source emits [1, 2, 3]

# Double expects int -> int

pipeline = Source() >> Double()

# Output: Stream[2, 4, 6]

# The JIT compiler injects the necessary Map logic.

```

## 11.3 Fluid Dynamics (The Calculus of Flow)

When dealing with Streams, the discrete algebraic view ($A \gg B$) is
approximated by the continuous **Fluid Dynamics**.

### 11.3.1 Flow Rate (Current $J$)
The throughput of the system is the Flow Rate:
$$ J = \frac{dQ}{dt} $$
Where $Q$ is the quantity of information (events).

### 11.3.2 Pressure Gradients (Backpressure)
In a pipe, fluid flows from High Pressure to Low Pressure. In Eigen,
**Backpressure** acts as a repulsive force from downstream.
$$ \vec{v} \propto -\nabla P $$
If the downstream operator $B$ is slow (High Resistance), pressure $P_B$ builds
up. This pressure gradient propagates upstream to $A$, slowing down emission
($J_A \downarrow$).
Eigen handles this automatically via `asyncio` buffer limits.

## 11.4 Infinite Streams

Because `>>` supports Async Iterators, it naturally handles infinite streams
(Kafka, Websockets).
The pipeline becomes a **Standing Wave**.

```python

# This runs forever
LiveFeed = KafkaSource("ticks") >> AnomalyDetector() >> AlertSink()

```

## 11.5 Causal Structures (DAGs)

A chain of `>>` operators forms a **Line** (1D Manifold).
However, combined with other operators, it forms a Directed Acyclic Graph (DAG).
The JIT compiler (`Matrix` layer) linearizes this DAG into an optimized
execution path.

### Practice: Flow Dynamics

1.  **Linearity**: Keep flows as linear as possible. Deeply nested flows are
    harder to debug.
2.  **Type Contravariance**: The Output type of $A$ must be covariant with the
    Input type of $B$. The static type checker (MyPy/Pyright) will enforce this.
    $$ Out(A) \subseteq In(B) $$
3.  **Conservation of Mass**: Ensure $J_{in} = J_{out}$ unless you intend to
    drop data (Shedding). Accumulation leads to OOM (Explosion).

> "Sequence is the simplest form of logic."

---
**Eigen Cosmology** | [Previous: Book XI](../foundations/11_MATHEMATICAL_DERIVATIONS.md) | [Index](../00_INDEX.md) | [Next: Book XIII](13_OPERATORS_SUPERPOSITION.md) | *© 2025 The Eigen High Council*