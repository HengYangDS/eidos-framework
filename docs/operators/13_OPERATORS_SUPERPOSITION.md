# Book XIII: OPERATORS - The Choice (Superposition)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "In the quantum world, a particle takes all possible paths simultaneously. In
> Eigen, the Choice Operator `|` allows logic to exist in a superposition of
> states until observed."

## 12.1 The Algebra of Choice

The **Choice Operator** (Pipe `|`, `__or__`) represents **Logical Disjunction**,
**Fallback**, or **Branching**. In the Algebra of Action, it corresponds to the
**Sum over Histories**.

$$ \hat{H} = \hat{A} | \hat{B} $$

Physically, this creates a **Superposition**: The system is in state $|A\rangle$
*and* state $|B\rangle$ simultaneously (in terms of potentiality). The
wavefunction collapses to a single reality $|R\rangle$ upon execution.

### 12.1.1 Collapse Mechanics

The collapse of the wavefunction $\Psi = A | B$ follows specific rules based on
the **Energy Barrier** (Error State) of the operators.

1.  **Least Action Principle**: The path of least resistance is chosen.
2.  **Success**: If $A$ executes successfully (Low Energy), $\Psi \to A$.
3.  **Tunneling**: If $A$ hits a barrier (Exception/Failure), the particle
    **tunnels** to $B$.
    $$ A \xrightarrow{Error} B $$
4.  **Gate**: If a `Filter` (Potential Barrier) blocks $A$, flow moves to $B$.

## 12.2 The Try-Catch Isomorphism

Classical programming relies on `try/catch` blocks, which disrupt the linear
flow of logic. Eigen applies **Axiom IV (Algebraic Correspondence)** to
demonstrate that `try/catch` is topologically isomorphic to a Choice operation.

### The Topological Transform

*   **Classical**: Control flow jumps to a separate block.
*   **Eigen**: Data flow diverges and converges.

```python

# Classical Mechanics (Imperative)
def get_config():
    try:
        return load_from_db()
    except DBError:
        return default_config()

# Quantum Mechanics (Declarative)
GetConfig = LoadFromDB | DefaultConfig

```

The error is not an "Exception" (a rupture in space-time); it is simply a
particle hitting a wall and bouncing into the alternative channel.

## 12.3 Branching Strategies

The `|` operator is polymorphic. Its behavior depends on the **Phase** of the
interaction.

### 12.3.1 Priority Choice (Lazy Sequential)
This is the default behavior for `A | B`.
$$ P(A) \gg P(B) $$
*   **Logic**: Attempt $A$. If successful, return $A$. Else, attempt $B$.
*   **Physics**: The particle attempts to traverse Path A. Only if blocked does
    it reflect to Path B.
*   **Use Case**: Caching (Cache | DB), Resilience (Primary | Backup).

### 12.3.2 Race Choice (Constructive Parallelism)
This corresponds to the `Race` wrapper.
$$ A \parallel B $$
*   **Logic**: Execute $A$ and $B$ simultaneously. Return the first non-error
    result.
*   **Physics**: The particle travels both slits at once. The detector clicks
    for the first arrival.
*   **Use Case**: Hedging (Querying multiple replicas).

```python

# Quantum Hedging
FindUser = Race(Replica1, Replica2, Replica3)

```

### 12.3.3 Probabilistic Choice (Radioactive Decay)
This splits the beam based on probability amplitudes.
$$ |\Psi\rangle = \alpha|A\rangle + \beta|B\rangle $$
where $|\alpha|^2 + |\beta|^2 = 1$.

*   **Logic**: Route to A with probability $p$, else B.
*   **Physics**: Beam Splitter.
*   **Use Case**: Canary Deployments, A/B Testing.

```python

# 5% traffic to Canary
Serve = (Canary @ 0.05) | Stable

```

## 12.4 The Quantum Zeno Effect (Timeouts)

In quantum physics, the **Quantum Zeno Effect** states that continuous
observation of an unstable system prevents it from decaying. Conversely, the
**Anti-Zeno Effect** forces a change.

In Eigen, we use **Timeouts** as a forced measurement operator.

$$ \hat{O}_{timeout} |\Psi\rangle $$

If the computation $A$ does not collapse (finish) within time $t$, the Observer
forces a collapse to the Error state (which then flows to the fallback).

```python

# If API takes > 5s, the wave collapses to None
SafeCall = (ExternalAPI & Timeout(5.0)) | Constant(None)

```

## 12.5 Pattern Matching (Diffraction)

Choice can be combined with **Filters** (Potential Barriers) to create complex
routing logic, analogous to a **Diffraction Grating**.

The input beam is split into different angles (Paths) based on its wavelength
(Content/Type).

```python
from eigen.bosons import Filter

# Define the Potential Barriers
IsAdmin = Filter(lambda u: u.role == "admin")
IsUser  = Filter(lambda u: u.role == "user")

# The Diffraction Pattern
Process = (
    (IsAdmin >> AdminHandler) |
    (IsUser  >> UserHandler)  |
    (GuestHandler)            # The 0th order maxima (Default)
)

```

This replaces the nested `if/elif/else` structure with a flat, algebraic
expression.

## 12.6 Engineering Best Practices

### 12.6.1 Flatten the Hierarchy
Avoid deeply nested choices `(A | (B | (C | D)))`. The algebra is associative:
`A | B | C | D`.
This creates a "Flat Topology" that is easier to reason about.

### 12.6.2 Idempotency (Conservation of Charge)
When using `|` for retries or fallbacks, ensure that the failed attempt $A$
didn't leave partial side effects (Charge).
If $A$ is "dirty", you must wrap it in a Transaction or use the Antimatter
operator `~A` (Undo) before the pipe.

$$ (A \gg \text{Commit}) \mid (\sim A \gg B) $$

### 12.6.3 Observability (The Trace)
While the choice happens in superposition, the collapse event must be recorded.
"Why did we fall back to B?"
Use the `@` operator (Measurement) to log the path taken.

```python
ReliableOp = (
    (Primary @ Log("Primary Success")) |
    (Backup  @ Log("Fallback Triggered"))
)

```

This preserves the **History** of the particle for debugging.

---
**Eigen Cosmology** | [Previous: Book XII](12_OPERATORS_FLOW.md) | [Index](../00_INDEX.md) | [Next: Book XIV](14_OPERATORS_ENTANGLEMENT.md) | *© 2025 The Eigen High Council*
