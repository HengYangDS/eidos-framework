# Book VI: MATRIX - Path Integral Formulation (JIT)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "The particle takes all possible paths simultaneously."
> — *Feynman's Path Integral*

## 6.1 The Need for Compilation

Python is slow (Interpreted).
Physics is fast (Compiled).
To make Eigen fast, we must compile the Operator Graph into a highly optimized
execution kernel.

## 6.2 The Eigen IR (Intermediate Representation)

When you compose Operators (`A >> B`), you are not executing them. You are
building a **Computation Graph** (The Path).
This Graph is the **Eigen IR**.

```python

# This does not run. It builds the graph.
Graph = Source >> Map(f) >> Filter(p) >> Sink

```

## 6.3 Algebraic Rewriting (Graph Optimization)

Before execution, the **Matrix Engine** optimizes the IR using algebraic
identities (Book XVI).

### 6.3.1 Operator Fusion
$$ Map(f) \gg Map(g) \to Map(g \circ f) $$
Merges two loops into one. Reduces memory access overhead.

### 6.3.2 Filter Pushdown
$$ Map(f) \gg Filter(p) \to Filter(p \circ f) \gg Map(f) $$
(If $f$ is expensive, we filter first).

### 6.3.3 Dead Code Elimination (Zero Operator)
$$ A \gg Zero \to Zero $$
If a path leads to nowhere, prune it.

### 6.3.4 Topology Optimization (The Calculus)
Using the **Topology Operator** (`len`, `iter`), the compiler analyzes the
manifold structure.
*   **Loop Unrolling**: `Op * 3` $\to$ `Op >> Op >> Op`.
*   **Branch Pruning**: If `Op1 > Op2` is always False (proven by static
    analysis), remove `Op1`.

## 6.4 Zero-Copy Transport

The compiled kernel does not use Python Objects. It uses **Arrow Arrays**.
Data flows from $A$ to $B$ via pointers, without serialization.
(See Book XIX: Data Relativity).

## 6.5 The Compilation Tiers

1.  **O0 (Interpreted)**: Pure Python. Great for debugging.
2.  **O1 (Vectorized)**: Uses `numpy`/`pandas`. Fast for batch.
3.  **O2 (Fused)**: Generates custom Rust/C++ kernels.
4.  **O3 (Distributed)**: Compiles to Ray/Dask graph.
5.  **O4 (Renormalized)**: Applies **RG Flow** to derive effective parameters
    for macro-scale execution (Automatic Sharding / Consistency Tuning).

```python

# Select optimization level
Pipeline.compile(level="O4").run()

```

## 6.6 The `@jit` Decorator

We can compile individual functions into Atoms.

```python
@jit(input=Tensor[float], output=Tensor[float])
def fast_math(x):
    return x * 2 + 1

```

This compiles the Python bytecode to Machine Code (via Numba or Mojo).

> "Premature optimization is the root of all evil. Just-In-Time optimization is
> the root of all speed."

---
**Eigen Cosmology** | [Previous: Book V](05_MATRIX_HAMILTONIAN.md) | [Index](../00_INDEX.md) | [Next: Book VII](07_MATRIX_PERTURBATION.md) | *© 2025 The Eigen High Council*
