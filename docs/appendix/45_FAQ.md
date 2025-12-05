# Book XLV: FAQ - Questions from the Void

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

## 1. Philosophy

### Q: Why "Eigen"?
**A**: In linear algebra, an **Eigenvector** is a vector that does not change
direction when a transformation is applied. It represents the *essence* of the
transformation. The Eigen Framework aims to find the invariant structures (the
essence) of software engineering amidst the chaos of changing technologies.

### Q: Is this a real framework or a physics textbook?
**A**: Yes. We believe that software engineering *is* applied physics. By
treating code as matter and logic as force, we gain the rigorous predictive
power of thermodynamics and quantum mechanics.

### Q: Is it "Over-Engineered"?
**A**: "Over-engineering" implies complexity without value. Eigen is "Hyper-
Engineered"—it accepts high initial complexity (learning the algebra) to achieve
zero marginal complexity at scale (infinite composability).

---

## 2. Comparison

### Q: How does this compare to LangChain?
**A**: LangChain is a library of *chains* (lists). Eigen is a library of
*tensors* and *operators* (algebra). LangChain is imperative/procedural. Eigen
is declarative/functional. Eigen's `Neural Physics` layer subsumes LangChain's
capabilities but adds thermodynamic cost tracking and self-optimization.

### Q: How does this compare to RxPY / ReactiveX?
**A**: RxPY focuses on the `Observer` pattern. Eigen subsumes ReactiveX via the
`Flow (>>)` and `Entanglement (&)` operators. However, Eigen adds the **Time
Symmetry** and **Renormalization** layers which RxPY lacks.

### Q: How does this compare to Pandas/Polars?
**A**: Pandas is a DataFrame library. Eigen treats Pandas DataFrames as **Heavy
Fermions**. You can use Pandas inside an Eigen `Map` boson. Eigen provides the
*pipeline* and *scheduling* that surrounds the data processing.

---

## 3. Technical

### Q: What is the performance overhead?
**A**:
*   **O0 (Interpreted)**: Python overhead (~10-50us per op).
*   **O3 (JIT)**: Near C++ speed (fused kernels).
*   **O5 (Silicon)**: Zero latency (hardware).

### Q: Can I use this for simple scripts?
**A**: You can, but it's like using a particle accelerator to toast bread. It
works, but the setup cost is high. Eigen shines in complex, distributed,
evolving systems.

### Q: How do I debug a "Negative Latency" error?
**A**: If you see `Latency < 0`, it means the **Prescience** operator predicted
the user's intent *before* they committed it, but the user changed their mind.
This is a **Causality Violation**. Increase the `confidence_threshold` in the
`Void` config.

---
**Eigen Cosmology** | [Previous: Book XLIV](44_DESIGN_PATTERNS.md) | [Index](../00_INDEX.md) | [Next: Book XLVI](46_TROUBLESHOOTING.md) | *© 2025 The Eigen High Council*
