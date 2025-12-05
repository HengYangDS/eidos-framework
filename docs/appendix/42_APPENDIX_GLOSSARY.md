# Book XLII: Appendix - The Eigen Glossary

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "The beginning of wisdom is the definition of terms." — Socrates

This glossary maps concepts from Physics, Mathematics, and Philosophy to their
specific meanings in the Eigen Framework.

## A

### Action ($S$)
*   **Physics**: The integral of the Lagrangian over time. $S = \int L dt$.
    Nature minimizes this quantity.
*   **Eigen**: The "cost" or "effort" of a computation. The Scheduler minimizes
    Action (Compute + Latency) when routing tasks.
*   **Code**: `Action = CostFunction(Latency, Price)`.

### Adjoint ($\dagger$)
*   **Math**: The conjugate transpose of a matrix.
*   **Eigen**: The inverse or compensatory operation. If $A$ is "Reserve Funds",
    $A^\dagger$ is "Release Funds".
*   **Code**: `~Operator`.

### Atom
*   **Physics**: The smallest unit of ordinary matter.
*   **Eigen**: A pure function or minimal unit of logic decorated with `@atom`.
    It has no internal structure visible to the Scheduler.
*   **Code**: `@atom def add(a, b): ...`

### Autopoiesis
*   **Biology**: A system capable of reproducing and maintaining itself.
*   **Eigen**: The property of a system to heal (Retry), grow (Scale), and
    evolve (Biogenesis) without external intervention.

## B

### Big Bang
*   **Cosmology**: The initial singularity from which the universe expanded.
*   **Eigen**: The execution of `import eigen` or the start of the Event Loop.

### Black Hole
*   **Physics**: A region of spacetime where gravity is so strong that nothing
    can escape.
*   **Eigen**: A Data Lake or Sink where data enters but is difficult to query
    (High Entropy).
*   **Code**: `Sink`.

### Boson
*   **Physics**: Force-carrying particles (Integer spin).
*   **Eigen**: Operators. They mediate interactions between Data (Fermions).
    They obey Bose-Einstein statistics (can be stacked/composed).
*   **Code**: `Operator`, `Map`, `Filter`.

## C

### Calculus
*   **Math**: The study of continuous change.
*   **Eigen**: The set of operators (`d`, `integral`) used for Optimization and
    Gradient Descent.
*   **Code**: `eigen.calculus`.

### Causality
*   **Physics**: The relationship between cause and effect. $t_{cause} <
    t_{effect}$.
*   **Eigen**: The ordering of events enforced by the Flow Operator (`>>`).
*   **Code**: `A >> B`.

### Choice (`|`)
*   **Physics**: Superposition / Branching.
*   **Eigen**: The operator for logical disjunction, fallback, or branching.
*   **Code**: `A | B`.

### Circuit Breaker
*   **Engineering**: A switch that opens to protect a circuit from overload.
*   **Eigen**: A Phase Transition from Conductor to Insulator based on Error
    Temperature.
*   **Code**: `CircuitBreaker()`.

### Collapse
*   **Physics**: The reduction of a wavefunction to a single state upon
    measurement.
*   **Eigen**: The resolution of a `Choice` or `Future` into a concrete value or
    error.

### Context
*   **Linguistics**: The setting for an event.
*   **Eigen**: The Gauge Field (`%`) that permeates the execution.
*   **Code**: `Operator % Context`.

### Cost Hamiltonian
*   **Physics**: The energy function of a system.
*   **Eigen**: The objective function used to optimize cloud spend and latency.

## D

### Data Gravity
*   **Physics**: Mass attracts mass.
*   **Eigen**: Large datasets attract compute. It is cheaper to move Code to
    Data than Data to Code.

### Dead Code
*   **Software**: Code that is never executed.
*   **Eigen**: A region of the Hilbert Space with zero probability amplitude.
    The RG Compiler prunes this (Vacuum Energy).

### Differentiable Programming
*   **CS**: Programming where the code itself can be differentiated to find
    gradients.
*   **Eigen**: The ability to use `d(Op)` to optimize parameters.

### Duality
*   **Philosophy**: Two aspects of the same reality.
*   **Eigen**: The equivalence between Code (Classical) and AI (Neural), or Wave
    (Stream) and Particle (Batch).

## E

### Eigen
*   **German**: "Own", "Proper", "Characteristic".
*   **Math**: Eigenvalue, Eigenvector.
*   **Framework**: The Unified Field Theory of Software.

### Entanglement (`&`)
*   **Physics**: Quantum states that cannot be described independently.
*   **Eigen**: Concurrency or Parallelism. Operations that happen together.
*   **Code**: `A & B`.

### Entropy ($S$)
*   **Physics**: A measure of disorder.
*   **Eigen**: A measure of Technical Debt or Code Complexity.

### Epoch
*   **Cosmology**: A distinct period in the history of the universe.
*   **Eigen**: A stage of optimization (e.g., Epoch I: Algebra, Epoch V:
    Silicon).

### Event Horizon
*   **Physics**: The boundary beyond which events cannot affect an observer.
*   **Eigen**: The Interface (Port) of a service. Outside the horizon, the
    internal logic is invisible (Holographic).

## F

### Fermion
*   **Physics**: Matter particles (Half-integer spin).
*   **Eigen**: Data. It occupies memory and has identity (Pauli Exclusion).
*   **Code**: `Knowledge`, `Record`.

### Field
*   **Physics**: A physical quantity that has a value for each point in space
    and time.
*   **Eigen**: Context or Configuration injected into the runtime.
*   **Code**: `Field`, `Config`.

### Flow (`>>`)
*   **Physics**: The movement of a fluid.
*   **Eigen**: The operator for sequential composition.
*   **Code**: `A >> B`.

### Flux
*   **Physics**: The rate of flow through a surface.
*   **Eigen**: The throughput of a pipeline (Events/Second).

## G

### Gauge Invariance
*   **Physics**: The Lagrangian remains unchanged under local transformations.
*   **Eigen**: The Business Logic remains valid regardless of Infrastructure
    changes (e.g., switching DBs).

### Gradient ($\nabla$)
*   **Calculus**: The vector of partial derivatives.
*   **Eigen**: The direction of steepest ascent for optimization.
*   **Code**: `d(Op)`.

### Grand Unification
*   **Physics**: The unification of Strong, Weak, and Electromagnetic forces.
*   **Eigen**: The unification of Code, AI, and Physics metaphors into one
    framework.

## H

### Hamiltonian ($H$)
*   **Physics**: The operator corresponding to the total energy of the system.
*   **Eigen**: The central object representing the Logic/Program. It drives the
    time evolution of Data.

### Heisenberg Uncertainty
*   **Physics**: $\Delta x \Delta p \ge \hbar/2$.
*   **Eigen**: The trade-off between Observability (Logs) and Performance
    (Speed).

### Holographic Principle
*   **Physics**: Information in a volume is encoded on the boundary.
*   **Eigen**: The Logic (Internal) is projected onto the Type Signature
    (Interface).

## I

### Impedance Matching
*   **Electronics**: Matching input and output resistance to maximize power
    transfer.
*   **Eigen**: Aligning Data Types (Schemas) between services to minimize
    serialization overhead.

### Interference
*   **Physics**: The combination of waves.
*   **Eigen**: The combination of Logic. Constructive (`+`) or Destructive
    (`-`).

### Isotope
*   **Chemistry**: Variants of an element with different neutron counts.
*   **Eigen**: Different implementations of the same abstract Operator (e.g.,
    `PostgresSource` vs `MySQLSource`).

## J

### JIT (Just-In-Time)
*   **CS**: Compilation during execution.
*   **Eigen**: The Matrix layer that optimizes the Operator Graph at runtime.

## K

### Kernel
*   **Math**: The set of vectors mapping to zero.
*   **Eigen**: The core execution engine.

## L

### Lagrangian ($L$)
*   **Physics**: $L = T - V$ (Kinetic - Potential Energy).
*   **Eigen**: The function describing the system's dynamics, used to derive the
    Path of Least Action.

### Latency
*   **Engineering**: Time delay.
*   **Eigen**: Space-time interval.

### Light Cone
*   **Relativity**: The path that a flash of light travels through spacetime.
*   **Eigen**: The causal boundary of an event.

### Logos
*   **Greek**: Word, Reason, Plan.
*   **Eigen**: The Axiomatic Layer (Interfaces/Protocols).

## M

### Manifold
*   **Math**: A topological space that locally resembles Euclidean space.
*   **Eigen**: The geometry of the data space (e.g., the Lakehouse Manifold).

### Matrix
*   **Math**: A rectangular array of numbers.
*   **Eigen**: The Compiler Layer (JIT/Optimization).

### Maxwell's Demon
*   **Thermodynamics**: An entity that sorts particles to decrease entropy.
*   **Eigen**: The Refactorer, Linter, or Garbage Collector.

### Metric Tensor ($g_{\mu\nu}$)
*   **Relativity**: Defines distance in spacetime.
*   **Eigen**: Defines the cost/distance in storage (Row vs Column).

### Microservice
*   **Software**: A small, independent service.
*   **Eigen**: A Gas Particle.

### Monad
*   **Functional Programming**: A design pattern for pipeline composition.
*   **Eigen**: The Operator is a Monad (bind = `>>`).

### Multiverse
*   **Cosmology**: Hypothetical set of infinite universes.
*   **Eigen**: Epoch X. The execution of parallel timelines for fault tolerance.

## N

### Negative Latency
*   **Omega Point**: Prediction of a result before the request.

### Neural Physics
*   **Eigen**: The study of AI Agents using physical principles.

## O

### Observer Effect
*   **Physics**: Measurement disturbs the system.
*   **Eigen**: Logging slows down the code.

### Omega Point
*   **Teilhard de Chardin**: The ultimate goal of evolution.
*   **Eigen**: The Void. The end of code.

### Operator
*   **Math**: A mapping from one space to another.
*   **Eigen**: The fundamental unit of logic (Boson).

## P

### Phase Space
*   **Physics**: A space in which all possible states of a system are
    represented.
*   **Eigen**: The set of all possible variable configurations.

### Phase Transition
*   **Physics**: Change of state (Solid -> Liquid).
*   **Eigen**: Sudden change in system behavior (e.g., Circuit Breaker Open).

### Pipeline
*   **Software**: A chain of processors.
*   **Eigen**: A Geodesic through the Operator Manifold.

### Potential ($V$)
*   **Physics**: Stored energy.
*   **Eigen**: The definition of "Done" or "Correct". The Logic pulls data
    towards the Potential.

### Prescience
*   **Sci-Fi**: Foreknowledge.
*   **Eigen**: Predictive pre-computation.

## Q

### Quantization
*   **Physics**: Discretization of energy.
*   **Eigen**: Batching a stream. `Stream // Batch`.

### Quantum Suicide
*   **Thought Experiment**: Surviving via branching universes.
*   **Eigen**: Fault tolerance via Multiverse forking.

### Quine
*   **CS**: A program that outputs its source code.
*   **Eigen**: The goal of the Genesis epoch.

## R

### Renormalization Group (RG)
*   **Physics**: Mathematical apparatus that allows systematic investigation of
    changes in a physical system as viewed at different scales.
*   **Eigen**: The compiler pass that optimizes consistency and latency across
    micro/macro scales.

### Resonance
*   **Physics**: Large amplitude vibration at specific frequencies.
*   **Eigen**: When the Code structure perfectly matches the Domain structure.

## S

### Singularity
*   **Cosmology**: A point of infinite density.
*   **Eigen**: The point where Code and AI merge.

### Spacetime
*   **Relativity**: The fusion of space and time.
*   **Eigen**: The execution environment (Nodes + Clock).

### Spin
*   **Physics**: Intrinsic angular momentum.
*   **Eigen**: Mutability (Spin 0 = Immutable, Spin 1/2 = Mutable).

### Superposition
*   **Quantum Mechanics**: A system being in multiple states at once.
*   **Eigen**: The `Choice` operator (`|`) before collapse.

## T

### Techne
*   **Greek**: Art, Craft, Skill.
*   **Eigen**: The Implementation Layer (Fermions, Bosons, Hardware).

### Temperature ($T$)
*   **Thermodynamics**: Average kinetic energy.
*   **Eigen**: Error Rate or Team Velocity.

### Tensor
*   **Math**: A geometric object that maps vectors to scalars.
*   **Eigen**: A high-dimensional data structure.

### Tunneling
*   **Quantum Mechanics**: Passing through a potential barrier.
*   **Eigen**: Error handling (`try/catch`) or bypassing a filter.

## U

### Uncertainty Principle
*   **Heisenberg**: Limit on precision of pairs of variables.
*   **Eigen**: Limit on Observability vs Performance.

### Universal Solvent
*   **Alchemy**: A substance that dissolves all materials.
*   **Eigen**: The Algebra of Operators, which absorbs all other libraries.

## V

### Vacuum
*   **Physics**: Space devoid of matter.
*   **Eigen**: The state before execution.

### Vector
*   **Math**: Quantity with magnitude and direction.
*   **Eigen**: An embedding of knowledge.

## W

### Wavefunction ($\Psi$)
*   **Quantum Mechanics**: Mathematical description of the quantum state.
*   **Eigen**: The total state of the running program.

### Wormhole
*   **Relativity**: Shortcut through spacetime.
*   **Eigen**: Zero-Copy transport (Arrow).

## Z

### Zero-Copy
*   **Systems**: Moving data without CPU copy.
*   **Eigen**: Wormhole transport.

### Zero-Point Energy
*   **Physics**: Lowest possible energy of a quantum system.
*   **Eigen**: The base cost of an empty loop.

---
**Eigen Cosmology** | [Previous: Cookbook XIII](../examples/COOKBOOK_13_METAVERSE_PHYSICS.md) | [Index](../00_INDEX.md) | [Next: Book XLIII](43_API_REFERENCE.md) | *© 2025 The Eigen High Council*
