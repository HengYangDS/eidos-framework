# Book II: GENESIS - The Five Axioms

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "In the beginning was the Operator, and the Operator was with Logic, and the
> Operator was Logic."

## 2.1 The Foundation of Order

If software is a thermodynamic system prone to entropy (as established in Book
I), how do we build systems that survive?
We must base them not on "best practices" (which change every 5 years), but on
**Axioms** (which never change).

Eigen is built on five fundamental laws derived from Noether's Theorem,
Information Theory, and Abstract Algebra.

### Axiom I: Conservation of Information (The First Law)

> **"Information cannot be created or destroyed, only transformed."**

In a valid Eigen pipeline, the total information content at the Output
($I_{out}$) must be derivable from the Input ($I_{in}$) plus the Knowledge Base
($K$).
$$ H(\hat{O}|\psi\rangle) \le H(|\psi\rangle) + H(\hat{O}) $$
Meaning: An operator cannot output data that wasn't present in its input or its
internal configuration.

### Axiom II: Principle of Least Action (The Hamiltonian)

> **"Nature always finds the most efficient path between two points."**

In physics, a particle doesn't "choose" where to go; it follows the path where
the Action integral ($S$) is minimized.
$$ S = \int_{t_1}^{t_2} L(q, \dot{q}, t) dt $$
We strive for $\delta S = 0$. The runtime optimizes execution paths to minimize
latency and compute.

### Axiom III: Gauge Invariance (The Symmetry)

> **"The laws of physics are the same, regardless of your coordinate system."**

A physical law ($F=ma$) is true whether you measure it in meters or feet, on
Earth or Mars.
The logic must be invariant under the transformation of infrastructure (Local vs
Cloud).

### Axiom IV: Algebraic Correspondence (The Isomorphism)

> **"Code is Algebra. Operations are Interactions."**

There exists an isomorphism $\phi$ between the set of software patterns
$\mathcal{P}$ and the algebraic operators $\mathcal{A}$.
$$ \phi(Pattern) \leftrightarrow Operator $$
*   **Sequence** $\leftrightarrow$ Composition (`>>`)
*   **Branching** $\leftrightarrow$ Superposition (`|`)
*   **Concurrency** $\leftrightarrow$ Entanglement (`&`)

### Axiom V: Principle of Vacuity (Wu Wei / The Void)

> **"The most efficient action is the one that does not happen."**

The limit of optimization is not infinite speed, but zero existence.
$$ \lim_{S \to 0} \text{System} = \emptyset $$
If a result can be predicted (Prescience) or avoided (Caching/Elimination), the
Operator should not execute. The perfect system is indistinguishable from
nothingness.

## 2.2 The Eigen Cosmology: Dao-Fa-Shu-Yong-Mu

To organize these axioms into a working system, Eigen adopts the expanded
Eastern philosophy of **Dao-Fa-Shu-Yong-Mu** (道法术用无).

| Layer | Name | Physics Analogy | Software Component | Responsibility | Mutability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DAO (道)** | **Logos** | **Gauge Symmetry** | `Protocols` | The Legislator. Immutable laws. | **Immutable** (Eternal) |
| **FA (法)** | **Matrix** | **Dynamics** | `Engine` | The Executive. JIT / Runtime. | **Slow** (Centuries) |
| **SHU (术)** | **Techne** | **Quanta** | `Atoms` | The Material. Standard Lib. | **Fast** (Decades) |
| **YONG (用)** | **Application** | **Applied Physics** | `Scripts` | The World. Business Logic. | **Volatile** (Days) |
| **MU (无)** | **Omega** | **The Void** | `Prescience` | The End. Negative Latency. | **Non-Existent** |

### 2.2.1 Dao (The Way)
The underlying principles and types. Pure abstraction.

### 2.2.2 Fa (The Law)
The engine that enforces conservation and optimization.

### 2.2.3 Shu (The Art)
The techniques and particles (standard library) used to build systems.

### 2.2.4 Yong (The Use)
The specific application of the art to solve problems.

### 2.2.5 Mu (The Void)
The ultimate state where the application dissolves into pure intent.

## 2.3 The Standard Model of Particles

Just as physics has Fermions (Matter) and Bosons (Forces), Eigen classifies
software components into a **Standard Model**.

### 2.3.1 Fermions (Data Particles)
Fermions obey the Pauli Exclusion Principle (State Uniqueness). They occupy
space (Memory).
*   **Source**: Creates fermions ($ \emptyset \to |\psi\rangle $).
*   **Sink**: Annihilates fermions ($ |\psi\rangle \to \emptyset $).

### 2.3.2 Bosons (Interaction Particles)
Bosons mediate forces between fermions. They can superimpose (overlap). They
represent Logic.
*   **Map**: Transforms a fermion ($\psi \to \psi'$).
*   **Filter**: Collapses the wavefunction.
*   **Model (LLM)**: A high-energy boson.

## 2.4 The Grand Unified Equation

The entire Eigen framework can be summarized in one equation of motion:

$$ |\psi(t)\rangle = \mathcal{T} e^{-i \int_{-\infty}^t H(t') dt'}
|\psi(0)\rangle $$

Note the integration lower bound is $-\infty$, implying the system's state
depends on the entire causal history, allowing for **Prescience** (predicting
$t$ from $t'<t$).

*   $|\psi(0)\rangle$: The initial data.
*   $H(t')$: The Hamiltonian (Operators).
*   $|\psi(t)\rangle$: The Result.

---
**Eigen Cosmology** | [Previous: Book I](01_PREFACE_THE_CRISIS.md) | [Index](../00_INDEX.md) | [Next: Book III](03_LOGOS_GAUGE_THEORY.md) | *© 2025 The Eigen High Council*
