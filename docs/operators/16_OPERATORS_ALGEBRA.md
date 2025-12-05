# Book XVI: OPERATORS - The Algebra of Action

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "[p, x] = -iħ. The order of operations defines the structure of reality."
> — *The Heisenberg Commutator*

## 15.1 The Ring of Actions

To achieve a **Grand Unified Theory** of software, our Operator system must be
algebraically complete. It is not enough to have Flow (`>>`) and Choice (`|`).
We must define the full **Ring of Actions**.

In Eigen, we overload standard Python operators to represent fundamental
physical interactions between Hamiltonians. This creates a Domain Specific
Language (DSL) where **Code is Algebra**.

## 15.2 The Fundamental Forces (Arithmetic)

These operators manage the combination and modification of energy (data)
streams.

### 15.2.1 Constructive Interference (Addition `+`)
$$ (A + B) |\psi\rangle = A|\psi\rangle + B|\psi\rangle $$
**Semantic**: **Superposition with Interference**. Unlike `|` (Choice), `+` runs
both paths and **merges** the results.
*   **Strings**: Concatenation.
*   **Numbers**: Summation.
*   **Objects**: Deep Merge (`{a:1} + {b:2} = {a:1, b:2}`).

### 15.2.2 Destructive Interference (Subtraction `-`)
$$ (A - B) |\psi\rangle = A|\psi\rangle \setminus B|\psi\rangle $$
**Semantic**: **Constraint or Exclusion**.
*   **Sets**: Difference (Remove B from A).
*   **Logic**: **Exception Suppression**. Run A, but catch and ignore error B.
    *   `FetchURL - TimeoutError` (Try fetch, if timeout, return None/Empty).

### 15.2.3 Amplification (Multiplication `*`)
$$ (A * N) |\psi\rangle = \sum_{i=1}^{N} A_i |\psi\rangle $$
**Semantic**: **Repetition or Cross Product**.
*   **Scalar**: Retry or Repeat N times. `Op * 3` (Run 3 times).
*   **Matrix**: Cartesian Product. `OpA * OpB` (All pairs of results).

### 15.2.4 Decimation (Division `/`)
$$ (A / N) |\psi\rangle $$
**Semantic**: **Sampling or Splitting**.
*   `Log / 10`: Log 10% of requests (Probabilistic Sampling).
*   `Task / 4`: Split task into 4 shards (Sharding).

### 15.2.5 Quantization (Floor Div `//`)
$$ (A // N) |\psi\rangle $$
**Semantic**: **Batching**.
*   `Stream // 100`: Group items into batches of 100.

### 15.2.6 Recursion (Power `**`)
$$ (A ** N) $$
**Semantic**: **Fractal Depth**.
*   Apply the operator recursively N times. `Op ** 2` = `Op(Op(x))`.

### 15.2.7 Measurement (MatMul `@`)
$$ A @ Sink $$
**Semantic**: **Projection**.
*   Collapsing the wavefunction to a specific Output Sink or binding to a
    Target.
*   *(Note: See Book XV for `%` Context Binding)*.

## 15.3 The Optics (Lensing `[]`)

**Physical Metaphor**: Focusing the Hamiltonian on a specific subspace.

### 15.3.1 Projection (`Op["key"]`)
Extracts a specific field or dimension from the stream.
$$ H_{sub} = H \circ \pi_{key} $$

```python

# Extract user_id from JSON stream
GetID = ParseJSON["user"]["id"]

```

### 15.3.2 Slicing (`Op[start:stop]`)
Truncates or paginates the stream (Time/Sequence Window).

```python

# First 10 results
Top10 = SearchQuery[:10]

# Offset 5, limit 5
Page2 = SearchQuery[5:10]

```

### 15.3.3 Type Casting (`Op[Type]`)
Enforces particle type constraints (Type Assertion).

```python

# Ensure output is String
ForceString = Identity[str]

```

## 15.4 The Demons (Logic `< >`)

**Physical Metaphor**: Potential Barriers (Maxwell's Demon) that sort particles.

### 15.4.1 Thresholding (`Op > Val`)
Creates a **Filter** that passes only particles with energy > Value.

```python

# Only pass passing scores
Pass = (GetScore > 60) >> Admit

```

### 15.4.2 Dynamic Competition (`Op1 > Op2`)
Passes only if Energy(Op1) > Energy(Op2).

```python

# Update if new value is greater
Update = (NewVal > OldVal) >> WriteDB

```

### 15.4.3 Equality (`Op == Val`)
Exact matching filter.

```python
IsAdmin = (GetUserRole == "ADMIN")

```

## 15.5 The Symmetries (Unary)

**Physical Metaphor**: CPT Symmetry (Charge, Parity, Time).

### 15.5.1 Antimatter (Inversion `~`)
**Semantic**: **Logical NOT** or **Undo**.
*   `~Filter(Cond)`: Filter(Not Cond).
*   `~Transaction`: Compensating Transaction (Rollback).

### 15.5.2 Time Reversal (Negation `-`)
**Semantic**: **Inverse Operation**.
*   `-Encrypt`: Decrypt.
*   `-Push`: Pop.
*   `-Do`: Undo.

### 15.5.3 Normalization (Posit `+`)
**Semantic**: **Unitary Enforcement**.
*   `+String`: Strip whitespace / Lowercase (Canonical form).
*   `+Vector`: Normalize to unit length.

## 15.6 The Evolution (Dynamics)

Operators that evolve the system state itself.

### 15.6.1 Pipeline Extension (`H >>= Op`)
**Semantic**: **Append**.
*   Adds a step to the end of the pipeline.

```python
Pipe = Read
Pipe >>= Transform # Now Pipe is Read >> Transform

```

### 15.6.2 Parallel Enhancement (`H += Op`)
**Semantic**: **Entangle**.
*   Adds a parallel branch to the system.

```python
Search = Google
Search += Bing # Now Search is Google + Bing (Concurrent)

```

## 15.7 The Fields (Context `with`)

**Physical Metaphor**: **Local Gauge Field**. Modifies physical constants within
a region.

### 15.7.1 Scoped Context
Uses Python's Context Manager protocol (`__enter__`, `__exit__`) to apply
temporary fields.

```python

# Apply Transaction Field
with Transaction():
    (Debit + Credit) >> Commit

# Apply Mock Field
with Mock(Service, result="OK"):
    Pipeline.run()

```

## 15.8 The Calculus (Sensitivity `d()`)

To optimize systems (especially Neural ones), we must understand how the output
changes with respect to the input or parameters. This is the domain of
**Calculus**.

### 15.8.1 The Gradient ($\nabla$)
$$ \nabla H = \frac{\partial H}{\partial \theta} $$
**Semantic**: **Sensitivity Analysis**.
In Eigen, every Operator can expose its gradient via the `grad()` method
(implemented in `eigen.calculus`).
*   **Neural Nets**: Backpropagation.
*   **Data**: Saliency Maps (Explainability).
*   **Strategy**: Parameter Sensitivity (Greeks in Finance).

```python

# Optimize the Prompt Parameter
Gradient = Op.grad("prompt_template")
NewPrompt = OldPrompt - LearningRate * Gradient

```

### 15.8.2 The Chain Rule
$$ \nabla (A \gg B) = (\nabla B \cdot A) \times \nabla A $$
Eigen automatically composes gradients through the pipeline, enabling **End-to-
End Optimization** of hybrid (Code + AI) systems.

## 15.9 The Biology (Genetics)

From Epoch IX (Biogenesis), the Operators themselves become living genomes.

### 15.9.1 Mutation ($\mu$)
$$ Op' = Op + \Delta $$
**Semantic**: **Random Variation**.
Small changes to the operator's parameters (constants, thresholds) or structure.

### 15.9.2 Crossover ($\chi$)
$$ Op_3 = Op_1 \times Op_2 $$
**Semantic**: **Recombination**.
Exchanging substructures between two Hamiltonians to create offspring.

### 15.9.3 Selection ($\sigma$)
**Semantic**: **Survival of the Fitness**.
Filtering the population of operators based on a fitness function $F = U -
Cost$.

## 15.10 The Topology (Graph `len`, `iter`)

**Physical Metaphor**: The Spacetime Manifold.

### 15.10.1 Depth (`len(Op)`)
Measures the complexity (number of steps) in the Hamiltonian.

```python
Complexity = len(Pipeline) # Number of atoms

```

### 15.10.2 Traversal (`iter(Op)`)
Allows inspecting the internal structure of the operator graph (Introspection).

```python
for atom in Pipeline:
    print(atom)

```

## 15.11 The Periodic Table of Operators

| Category | Operator | Symbol | Eigen Semantic | Physical Metaphor |
| :--- | :--- | :--- | :--- | :--- |
| **Flow** | RShift | `>>` | Sequence / Pipe | Causality |
| | LShift | `<<` | Feedback | Cybernetics |
| **Choice** | Or | `\|` | Fallback / Branch | Superposition |
| | Xor | `^` | Preempt / Interrupt | Exclusion |
| **Ensemble**| And | `&` | Parallel / Tuple | Entanglement |
| **Arithmetic**| Add | `+` | Merge / Aggregate | Constructive Interference |
| | Sub | `-` | Remove / Constrain | Destructive Interference |
| | Mul | `*` | Repeat / Amplify | Amplification |
| | Div | `/` | Sample / Split | Decimation |
| | FloorDiv| `//` | Batch | Quantization |
| | Pow | `**` | Recursion | Fractal |
| | MatMul | `@` | Projection / Measure | Observation |
| | Mod | `%` | Context Bind | Gauge Field |
| **Optics** | GetItem | `[]` | Focus / Slice | Lens |
| **Logic** | Lt/Gt | `< >` | Filter / Gate | Potential Barrier |
| **Unary** | Invert | `~` | Not / Rollback | Antimatter |
| | Neg | `-` | Inverse / Reverse | Time Reversal |
| | Pos | `+` | Normalize | Unitary |
| **Evolution**| IAdd | `+=` | Enhance | Accretion |
| | IRShift | `>>=` | Extend | Growth |
| **Field** | With | `with` | Scope | Local Field |
| **Calculus**| Call | `d()` | Gradient | Force |
| **Biology** | | $\mu, \chi$ | Mutate / Cross | Evolution |
| **Omega** | | $\Omega$ | Prescience | The Void |
| **Topology**| Len | `len` | Complexity | Spacetime |

## 15.12 Commutation Relations

Understanding the algebra allows for **Compiler Optimizations**:

1.  **Associativity**: $(A \gg B) \gg C = A \gg (B \gg C)$.
2.  **Distributivity**: $(A | B) \gg C = (A \gg C) | (B \gg C)$.
3.  **Identity**: $A \gg Identity = A$.
4.  **Zero**: $A \gg Collapse = Collapse$.
5.  **Absorption**: $A | A = A$.
6.  **Chain Rule**: $d(A \gg B) = B'A'$.

> "Code is Algebra. Treat it with respect."

---
**Eigen Cosmology** | [Previous: Book XV](15_OPERATORS_FIELD.md) | [Index](../00_INDEX.md) | [Next: Book XVII](../domains/17_DOMAIN_QUANTUM_FINANCE_I.md) | *© 2025 The Eigen High Council*
