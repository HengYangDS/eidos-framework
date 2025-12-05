# Book VIII: TECHNE - The Fermions (Matter)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "Fermions are the building blocks of matter. They occupy space and cannot
> superimpose in the same state, but they can interact to form the universe."

## 8.1 The Standard Model of Data

In the Eigen cosmology (specifically the **Techne** layer), **Fermions**
represent the material substance of the system: the Data. Unlike **Bosons**
(Operators), which represent forces and transformations, Fermions are the
entities that *are transformed*.

Fermions obey the **Pauli Exclusion Principle** in the context of identity: no
two unique data entities can occupy the same identity space (Primary Key
uniqueness).

### 8.1.1 The Quantum Numbers of Data

Just as physical fermions (electrons, quarks) are defined by quantum numbers
(Spin, Charge, Mass), Eigen Fermions are defined by their intrinsic properties:

1.  **Mass (Size)**: The storage footprint.
    *   **Light Fermions**: `int`, `bool` (Registers).
    *   **Heavy Fermions**: `Image`, `Video`, `Large Language Model Weights`
        (Blobs).
    *   *Implication*: Heavy fermions exert significant **Data Gravity** (see
        8.5).

2.  **Spin (Mutability)**:
    *   **Spin 0 (Immutable)**: Tuples, FrozenSets, Strings. Stable, thread-
        safe, easy to reason about.
    *   **Spin 1/2 (Mutable)**: Lists, Dictionaries, Objects. Reactive,
        stateful, prone to race conditions.
    *   *Best Practice*: Prefer Spin 0 fermions for distributed messages to
        ensure consistency.

3.  **Charge (Type)**:
    *   Determines electromagnetic interaction (Type Compatibility).
    *   A `String` fermion (-1 charge) cannot naturally interact with an
        `Integer` boson (+1 charge) without a mediating transformer (Type
        Casting).

4.  **Isospin (Polymorphism)**:
    *   A `User` fermion and an `Admin` fermion are different states of the same
        underlying `Person` multiplet.

## 8.2 The Particle Zoo

We define a standard library of Fermions, extending the base `Knowledge`
particle defined in the Logos layer.

### 8.2.1 The Lepton Family (Primitive Data)
Leptons are point-like particles with no internal structure relevant to the
architecture.
*   `Scalar`: `int`, `float`, `str`.
*   `Atom`: A single unit of indivisible business logic configuration.

### 8.2.2 The Hadron Family (Composite Data)
Hadrons are composite particles made of quarks (fields).
*   **Baryons (Records)**: Structured data like `Dict`, `Pydantic Model`,
    `Protobuf`.
    *   Example: `User(id=1, name="Alice")`.
*   **Mesons (Relations)**: Transient pairs representing links, e.g.,
    `Edge(source, target)`.

### 8.2.3 The Tensor Family (Field Excitations)
*   `VectorKnowledge`: Embeddings, numerical arrays (NumPy/Torch).
*   `TensorStream`: An infinite flow of Tensors.

## 8.3 Fermion Algebra (Tensor Arithmetic)

Eigen treats data manipulation as algebraic operations on the Hilbert Space of
Fermions.

### 8.3.1 Merging (Addition `+`)
**Constructive Interference**. Merging two fermions creates a richer state.
$$ |F_1\rangle + |F_2\rangle = |F_{combined}\rangle $$

*   **Dictionaries**: Deep merge. `config_default + config_override`.
*   **Lists**: Concatenation. `header + body`.
*   **Text**: String interpolation.
*   **Tensors**: Vector addition (Superposition).

```python
@dataclass
class User(Fermion):
    name: str
    email: str = None

@dataclass
class Session(Fermion):
    token: str

# Algebra of Identity
user = User("Alice")
session = Session("jwt_123")
context = user + session 

# Context now holds both identities: UserWithSession(...)

```

### 8.3.2 Differencing (Subtraction `-`)
**Destructive Interference**. Removing attributes or noise.
$$ |F_{total}\rangle - |F_{noise}\rangle = |F_{signal}\rangle $$

*   **Privacy**: `UserData - PII = AnonymizedData`.
*   **Sets**: `AllUsers - BannedUsers = ActiveUsers`.
*   **Tensors**: `Signal - Noise = CleanSignal`.

```python
full_record = {"id": 1, "password_hash": "...", "name": "Bob"}
safe_record = full_record - "password_hash" 

# Result: {"id": 1, "name": "Bob"}

```

### 8.3.3 Replication (Multiplication `*`)
**Cloning / Broadcasting**.
$$ |F\rangle * N = \sum_{i=1}^N |F\rangle_i $$

*   **Initialization**: `ZeroVector * 1024`.
*   **Broadcasting**: Sending a configuration fermion to N workers.

### 8.3.4 Division (Projection `/`)
**Sharding / Partitioning**.
$$ |F\rangle / N = \{ |f_1\rangle, ..., |f_N\rangle \} $$

*   **Data Parallelism**: Splitting a dataset into N chunks for distributed
    processing.
*   **Dimensionality Reduction**: `Embedding / PCA`.

### 8.3.5 Spin Statistics & Ordering
In quantum mechanics, Fermions must obey anti-symmetric statistics. In Eigen,
this translates to **Ordering Guarantees**.

*   **Ordered Streams (Fermi-Dirac)**: Particles must arrive in the exact order
    ($p_1, p_2, ...$) defined by their timestamp (Spin). Swapping two particles
    implies a state change.
    *   Use Case: Financial Ticks, CDC Logs.
*   **Unordered Streams (Bose-Einstein)**: Particles can be swapped without
    changing the macroscopic state.
    *   Use Case: Set of unique users, Bag of words.

### 8.3.6 Pauli Exclusion & Idempotency
The **Exclusion Principle** states that two identical fermions cannot occupy the
same quantum state simultaneously.

$$ \langle \psi | \psi \rangle = 0 \text{ if } \psi_1 = \psi_2 $$

In Distributed Systems, this is **Idempotency**:
*   If we receive Message A, and then receive Message A again, the second
    instance is annihilated or ignored.
*   **Implementation**: `DeduplicationFilter` (a Boson) enforces the Exclusion
    Principle.

### 8.3.7 Antiparticles (Tombstones)
For every Fermion $F$, there exists an Antiparticle $\bar{F}$ such that:

$$ F + \bar{F} = \gamma \text{ (Annihilation)} $$

*   **Semantics**: Soft Delete / Tombstone.
*   **Operation**: When a Compaction process sees a Record ($Key=K, Val=V$) and
    a Tombstone ($Key=K, Val=\emptyset$), they annihilate each other, leaving
    free space (Vacuum).

## 8.4 The Source Protocol (Genesis)

A `Source` operator acts as a **White Hole**, emitting Fermions from the
external vacuum into the Eigen system.
$$ \hat{a}^\dagger |0\rangle = |\psi\rangle $$

### 8.4.1 Asynchronous Genesis
Sources must be asynchronous generators (`AsyncIterator`) to maintain the flow
pressure.

```python
class Source[O]:
    async def __call__(self, _: None) -> AsyncIterator[O]:

        # Implementation dependent
        yield ...

```

### 8.4.2 Intelligent Sources (Pushdown)
A naive source reads everything. An intelligent source accepts a `Boson`
(Filter/Projection) *before* emission, collapsing the wavefunction at the
source.

*   **Predicate Pushdown**: Sending SQL `WHERE` clauses to the DB.
*   **Projection Pushdown**: Sending `SELECT` fields to Parquet reader.

```python

# The Source absorbs the Filter Boson to become a more specific Source
SmartSource = RawSource + Filter("age > 18")

```

## 8.5 The Sink Protocol (Annihilation)

A `Sink` operator acts as a **Black Hole**, absorbing Fermions and converting
their information into side effects (Storage, Network).
$$ \hat{a} |\psi\rangle = |0\rangle $$

### 8.5.1 Batch Annihilation
To optimize entropy generation (heat/cost), Sinks should annihilate Fermions in
batches, not individually.

```python
class DuckDBSink(Sink):
    """
    Absorbs stream, buffers into Vector, writes to Disk.
    """
    async def absorb(self, stream):
        batch = []
        async for particle in stream:
            batch.append(particle)
            if len(batch) > CRITICAL_MASS:
                await self.flush(batch)

```

## 8.6 Data Gravity (General Relativity)

Fermions warp the spacetime of compute around them.

**The Law of Data Gravity**:
$$ F_g = G \frac{M_{data} M_{compute}}{r^2} $$

Where:
*   $M_{data}$: Size of the dataset.
*   $M_{compute}$: Complexity of the logic.
*   $r$: Network latency/distance.

**Implication**:
For massive Fermions (TB-scale logs, Video), you cannot move the data to the
code ($r \to 0$). You must move the code (Bosons) to the data.
*   **Mobile Code**: Sending a Wasm filter to the S3 storage node.
*   **Stored Procedures**: Running logic inside the database.

This is the **Techne** implementation of the **Matrix** Least Action Principle:
Minimize $\int L_{network} dt$.

---
**Eigen Cosmology** | [Previous: Book VII](07_MATRIX_PERTURBATION.md) | [Index](../00_INDEX.md) | [Next: Book IX](09_TECHNE_BOSONS.md) | *© 2025 The Eigen High Council*