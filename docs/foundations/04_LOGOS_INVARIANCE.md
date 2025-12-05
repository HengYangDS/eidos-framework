# Book IV: LOGOS - Invariance & Conservation

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "Invariance is the only thing that remains when everything else changes."

## 4.1 The Gauge Principle

In physics, a Gauge Theory is a type of field theory in which the Lagrangian is
invariant under a continuous group of local transformations.
In Eigen, this translates to **Infrastructure Agnosticism**.

**The Gauge Principle of Software:**
> "The correctness of Business Logic must be invariant under the transformation
> of Infrastructure."

If you change your database from SQLite to Postgres, your logic (Hamiltonian)
must not change. If it does, you have broken Gauge Symmetry.

## 4.2 The Zero-Dependency Law

To ensure the Logos layer acts as a universal standard (like the Meter or the
Second), it must obey the **Zero-Dependency Law**.

**Law:**
The `eigen.logos` package must have **zero** third-party dependencies. It can
only import:
1.  `typing`
2.  `abc`
3.  `dataclasses`
4.  `contextvars`
5.  `datetime` / `uuid`

**Why?**
If Logos depends on `pydantic`, then every user of Eigen is forced to use
`pydantic`. If `pydantic` breaks backward compatibility, Eigen breaks.
By keeping Logos pure, we ensure that the "Constitution" of the framework can
survive for decades, regardless of the rise and fall of specific libraries
("Isotopes").

## 4.3 Conservation of Information: Formal Proof

We stated in Book II that Information cannot be created. How do we prove this in
code?
We use **Property-Based Testing** (PBT).

Instead of writing "Example Tests" (`assert f(2) == 4`), we write "Invariant
Tests" (`assert f(x) > x for all x`).

### 4.3.1 Hypothesis Strategy for Operators

We can use the `hypothesis` library to generate random operators and states to
verify conservation laws.

```python

# tests/gauge/test_conservation.py
from hypothesis import given, strategies as st
from eigen.logos import Operator, Knowledge

class IdentityOp(Operator[int, int]):
    async def __call__(self, x: int) -> int:
        return x

@given(st.integers())
async def test_identity_conservation(x):
    """
    Theorem: The Identity Operator preserves Information Entropy.
    H(I|x>) = H(|x>)
    """
    op = IdentityOp()
    result = await op(x)
    assert result == x

class LossyOp(Operator[str, int]):
    async def __call__(self, x: str) -> int:
        return len(x)

@given(st.text())
async def test_lossy_operator(text):
    """
    Theorem: A Map Operator transforms information but maintains traceability.
    Here, we prove that output is deterministic based on input.
    """
    op = LossyOp()
    res1 = await op(text)
    res2 = await op(text)
    assert res1 == res2  # Determinism

```

### 4.3.2 Associativity of Flow

One of the key invariants of Eigen is that the Flow Operator `>>` is
Associative.
$$ (A \gg B) \gg C \equiv A \gg (B \gg C) $$

This means the grouping of operators does not affect the result.

```python
@given(st.integers())
async def test_associativity(x):
    A = AddOne()
    B = Double()
    C = Square()
    
    # (A >> B) >> C
    path1 = (A >> B) >> C
    res1 = await path1(x)
    
    # A >> (B >> C)
    path2 = A >> (B >> C)
    res2 = await path2(x)
    
    assert res1 == res2

```

## 4.4 The Holographic Principle

The **Holographic Principle** states that the information contained in a volume
of space can be represented by a theory on the boundary of that space.

In Eigen, this means **The Type Signature is the UI**.

Because our Operators are strictly typed (`Operator[I, O]`), we can inspect the
"Boundary" (Types) to reconstruct the "Bulk" (User Interface).

```python
class DateFilter(Operator[list[Record], list[Record]]):
    """Filters records by date."""
    def __init__(self, start: datetime, end: datetime): ...

```

By reflecting on `__init__`, we see `start: datetime` and `end: datetime`.
The Holographic engine (`eigen.holography`) can automatically generate a UI with
two Date Pickers.

**Implication:**
You never write UI code. You define the Physics (Types), and the Universe (UI)
projects itself automatically.

## 4.5 Testing Symmetries

We can define a test suite that verifies if a user's custom Operator adheres to
the Standard Model.

```python
def verify_symmetry(op: Operator):
    """
    Runs a battery of physics tests on an operator.
    """
    check_commutativity(op)  # If applicable
    check_idempotency(op)    # If applicable
    check_serializability(op)

```

This ensures that the ecosystem of Eigen plugins remains mathematically
consistent.

---
**Eigen Cosmology** | [Previous: Book III](03_LOGOS_GAUGE_THEORY.md) | [Index](../00_INDEX.md) | [Next: Book V](05_MATRIX_HAMILTONIAN.md) | *© 2025 The Eigen High Council*
