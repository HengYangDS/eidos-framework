# Book XLVI: Troubleshooting - Debugging Reality

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

## 1. General Principles

Debugging in Eigen is not about "fixing bugs"; it is about **restoring
symmetry**. When a system fails, it implies a violation of a conservation law
(Information, Energy, or Causality).

### 1.1 The Debugging Hamiltonian
The general procedure is to apply the **Debugger Operator**:

$$ \hat{D} = \text{Trace} \otimes \text{Replay} \otimes \text{Diff} $$

1.  **Trace**: Measure the state ($\psi$) at every interaction vertex.
2.  **Replay**: Use Time Symmetry to rewind and replay the event.
3.  **Diff**: Compare the observed trajectory with the expected Hamiltonian.

---

## 2. Common Error Codes

### `E101: Entropy Overflow`
**Symptom**: System slows down, memory usage spikes, logs become verbose.

**Cause**: The system is generating information faster than it can annihilate it
(Sink). The **Heat Death** is approaching.
**Solution**:
*   Insert `Filter` (Maxwell's Demon) to reduce incoming entropy.
*   Increase `Batch` size in Sinks.
*   Apply `Renormalization` to coarse-grain the data.

### `E202: Causality Violation`
**Symptom**: `FutureEvent` arrives before `PastEvent`.

**Cause**:
*   Distributed clock skew (Relativity).
*   Misconfigured `Prescience` operator (Void layer).
**Solution**:
*   Enforce `CausalOrdering` in streams.
*   Reduce `lookahead_window` in Prescience.

### `E303: Vacuum Decay`
**Symptom**: The `State` of an actor spontaneously resets to `None`.

**Cause**: A "False Vacuum" collapse. The state was stored in a volatile field
(Memory) and the container restarted.
**Solution**:
*   Move state to a Stable Field (Redis/Postgres).
*   Implement `Checkpoint` boson.

### `E404: Particle Not Found`
**Symptom**: Reference to a Fermion ID fails.

**Cause**: The particle was annihilated by a Tombstone or Filter before reaching
the vertex.
**Solution**:
*   Check `Filter` predicates upstream.
*   Verify `AntiJoin` logic.

### `E500: Hamiltonian Divergence`
**Symptom**: `Cost` or `Error` approaches infinity during Optimization.

**Cause**: Learning Rate ($\eta$) too high or Gradient Explosion.

**Solution**:
*   Apply `GradientClipping`.
*   Reduce learning rate.

---

## 3. Diagnostic Procedures

### 3.1 The Trace Tensor
Inject a specialized Tracer Isotope into the stream.

```python

# Inject tracer
Stream.inject(TraceParticle(id="debug-1"))

# Watch logs

# [INFO] Vertex A absorbed debug-1

# [INFO] Vertex B emitted debug-1

```

### 3.2 Time Travel Debugging
If `TimeSymmetry` is enabled (Book XXVIII):

```python

# Rewind to the crash timestamp
DebugContext.seek("2024-11-14T10:00:00Z")

# Step forward
DebugContext.step()

```

### 3.3 The Quantum Eraser
If observation slows down the system (Heisenberg Limit):

```python

# Only log if an error occurs (Retroactive Logging)
with QuantumEraser():
    try:
        Pipeline.run()
    except Exception:

        # The logs materialized only now
        print(QuantumEraser.collapse())

```

---
**Eigen Cosmology** | [Previous: Book XLV](45_FAQ.md) | [Index](../00_INDEX.md) | [Next: Book XLVII](47_PHYSICS_CONSTANTS.md) | *© 2025 The Eigen High Council*
