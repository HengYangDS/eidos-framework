# Book XV: OPERATORS - The Field (Context)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "A Field permeates all of space-time. Particles move through it, and their
> behavior is modified by the field's potential, even without direct contact."

## 14.1 The Gauge Principle of Context

In classical programming, we pass context explicitly (`func(ctx, data)`). This
breaks the **Gauge Invariance** of the function—it now depends on the geometry
of the context.

In Eigen, we treat Context as a **Gauge Field** (`%`, `__mod__`).
*   The Operator (Particle) moves through the Field.
*   The Field modifies the Operator's behavior (Trajectory).
*   The Operator signature remains invariant ($I \to O$).

$$ \hat{H}_{bound} = \hat{H}_0 \% \Phi $$

## 14.2 The Field Operator (%)

The **Modulus Operator** `%` is used to bind a Context (Field) to an Operator.

```python

# The Generic Operator (Gauge Symmetric)
FetchData = DatabaseSource()

# The Field (Configuration)
ProductionConfig = {"db_url": "postgres://..."}

# Binding (Gauge Fixing)

# The operator now knows *where* to fetch, but its signature is unchanged.
ProductionFetch = FetchData % ProductionConfig

```

### 14.2.1 Local Gauge Invariance
Local Gauge Invariance means we can change the Field locally without affecting
the global topology.

```python

# Running the SAME logic in two different fields simultaneously
with TestField:
    ResultA = Pipeline.run()

with ProdField:
    ResultB = Pipeline.run()

```

This is the theoretical basis for **Dependency Injection** (DI). DI is not a
design pattern; it is a geometric property of the code.

## 14.3 Types of Fields

### 14.3.1 The Scalar Field (Configuration)
A constant value pervasive in a region.
*   **Examples**: `Config`, `FeatureFlags`, `EnvVars`.
*   **Physics**: Like the Higgs Field (gives mass/properties to particles).

### 14.3.2 The Vector Field (Request Scope)
A field that has direction and magnitude, changing with every request.
*   **Examples**: `TraceID`, `UserSession`, `AuthToken`.
*   **Physics**: Like the Electromagnetic Field (directs the flow).

### 14.3.3 The Tensor Field (Observability)
A high-dimensional field measuring the curvature of execution.
*   **Examples**: `OpenTelemetry Span`, `Logger`.
*   **Physics**: Like the Metric Tensor ($g_{\mu\nu}$).

## 14.4 Dynamic Fields (ContextVars)

Eigen uses Python's `contextvars` to implement thread-safe, async-safe local
fields.

```python

# Defining a Field
UserID = Field("user_id", default=None)

# The Operator reads the Field implicitly
@atom
def GetProfile(data):
    uid = UserID.get() # Measurement of the field
    return db.fetch(uid)

# Injecting the Field
Pipeline = GetProfile
run(Pipeline % {"user_id": 42})

```

## 14.5 Engineering Best Practices

### 14.5.1 Explicit vs Implicit
While Fields are powerful, overusing them leads to "Spooky Action at a Distance"
(Hidden Dependencies).
*   **Rule**: Use Fields for *Infrastructure* (Logging, DB Conn, Auth).
*   **Rule**: Use Arguments for *Domain Data* (Price, Quantity, SKU).

### 14.5.2 Field Propagation
Fields must propagate through **Entanglement** boundaries (`&`).
When you spawn a background task or a new thread, the Field values must be
copied (Teleported) to the new manifold. Eigen handles this automatically via
`contextvars.copy_context()`.

### 14.5.3 The Null Field (Vacuum State)
Always define a sensible default (Vacuum State) for your fields.
If `Config` is missing, the operator should either:
1.  Fail fast (Vacuum Decay).
2.  Use a local default (Spontaneous Symmetry Breaking).

## 14.6 Mathematical Formalism

The binding operation `%` is non-commutative.
$$ A \% F \neq F \% A $$
(An operator bound to a field is meaningful; a field bound to an operator is
nonsense).

It distributes over Flow:
$$ (A \gg B) \% F \equiv (A \% F) \gg (B \% F) $$
The field applies to the entire pipeline.

---
**Eigen Cosmology** | [Previous: Book XIV](14_OPERATORS_ENTANGLEMENT.md) | [Index](../00_INDEX.md) | [Next: Book XVI](16_OPERATORS_ALGEBRA.md) | *© 2025 The Eigen High Council*
