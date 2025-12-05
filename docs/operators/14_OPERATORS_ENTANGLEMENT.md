# Book XIV: OPERATORS - The Entanglement (Concurrency)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "Spooky action at a distance. In Eigen, entanglement allows distinct processes
> to execute independently yet remain bound as a single quantum state."

## 13.1 The Algebra of Concurrency

The **Entanglement Operator** (Ampersand `&`, `__and__`) represents
**Concurrency**, **Parallelism**, and **Aggregation**.
In the Algebra of Action, it corresponds to the **Tensor Product**.

$$ \hat{H} = \hat{A} \otimes \hat{B} $$

Unlike Choice (`|`) which selects *one* path, Entanglement executes *all* paths
and fuses their results into a compound state (Tuple).

### 13.1.1 The Tensor Product State

If operator $A$ produces state $|a\rangle$ and operator $B$ produces state
$|b\rangle$, then $A \& B$ produces the product state:
$$ |a\rangle \otimes |b\rangle \equiv (a, b) $$

This is the basis of the **Scatter-Gather** pattern.

## 13.2 Concurrency vs. Parallelism

In Eigen, `&` abstracts away the mechanism of execution (Threads, Processes,
Coroutines).

### 13.2.1 Coroutine Entanglement (Concurrent)
By default, `&` schedules standard Python coroutines on the same event loop.
*   **Physics**: Two electrons in the same orbital with opposite spin.
*   **Mechanism**: `asyncio.gather(A(), B())`.
*   **Cost**: Low overhead, shared memory.

### 13.2.2 Isolate Entanglement (Parallel)
If the operators are CPU-bound (Heavy Fermions), the JIT compiler can dispatch
them to separate cores.
*   **Physics**: Spatially separated particles.
*   **Mechanism**: `ProcessPoolExecutor`.
*   **Cost**: Serialization overhead (Impedance).

## 13.3 Interactions with Other Forces

How does Entanglement interact with other operators?

### 13.3.1 Distributivity of Flow
Flow distributes over Entanglement (sometimes).
$$ (A \& B) \gg C \equiv C(A_{out}, B_{out}) $$
Operator $C$ must accept a tuple (arity=2). This is a **Join** or **Reduce**
operation.

### 13.3.2 Entanglement vs. Choice
*   **Choice (`|`)**: **OR** logic. Sum of subspaces ($V \oplus W$). Result is
    $A$ *or* $B$.
*   **Entanglement (`&`)**: **AND** logic. Product of subspaces ($V \otimes W$).
    Result is $A$ *and* $B$.

## 13.4 Distributed Entanglement (Quantum Teleportation)

When $A$ and $B$ are on different nodes, `&` performs **Distributed Scatter-
Gather**.

```python

# The Query is sent to Shard1 and Shard2 simultaneously
GlobalSearch = Shard1Search & Shard2Search

```

This implies a **Non-Local Interaction**. The `GlobalSearch` operator doesn't
finish until *both* shards return. The state is entangled across the network.

### 13.4.1 The Collapse of the Whole
If *one* particle in an entangled pair collapses to Error, the *entire* state
collapses.
$$ Error \otimes B = Error $$
This is the default behavior (Fail Fast).

To survive partial failure, wrap individual components in **Shields** (Choice).
$$ (A | Default) \& (B | Default) $$

## 13.5 Engineering Patterns

### 13.5.1 The Fan-Out / Fan-In
This is the most common use case.
1.  **Fan-Out**: Split the flow into $N$ entangled paths.
2.  **Fan-In**: Gather the results with a Reduce operator.

```python

# 1. Get User ID

# 2. Fetch Profile AND Orders in parallel

# 3. Format the Report
Pipeline = GetUserID >> (GetProfile & GetOrders) >> FormatReport

```

### 13.5.2 The Sidecar (Background Entanglement)
Sometimes you want to entangle a task but not wait for it (Fire and Forget).
This requires a special **Detached Entanglement**.

$$ A \&_{async} B $$

Use the `Background` wrapper for this.

```python

# Process request AND log to analytics (don't wait for log)
Serve = ProcessRequest & Background(LogAnalytics)

```

## 13.6 Best Practices

1.  **Granularity**: Don't entangle trivial tasks (`1 + 1`). The overhead of the
    Tensor Product (Context Switching) outweighs the gain.
2.  **Stragglers**: The speed of `A & B` is determined by the *slowest*
    component.
    $$ T_{total} = \max(T_A, T_B) $$
    Use Timeouts on individual branches to prevent one straggler from hanging
    the universe.
3.  **Deadlocks**: Avoid entangling operators that depend on each other
    (Circular Dependency). This creates a **Closed Timelike Curve**, which is
    forbidden by causality.

---
**Eigen Cosmology** | [Previous: Book XIII](13_OPERATORS_SUPERPOSITION.md) | [Index](../00_INDEX.md) | [Next: Book XV](15_OPERATORS_FIELD.md) | *© 2025 The Eigen High Council*
