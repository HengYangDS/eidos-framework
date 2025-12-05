# Book XLIV: Design Patterns - The Isomorphisms

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

## 1. The Algebraic Correspondence

As stated in **Axiom IV**, every software design pattern corresponds to an
algebraic operator. This appendix provides the canonical mapping between classic
Gang of Four (GoF) patterns, Enterprise Integration Patterns (EIP), and Eigen
Operators.

---

## 2. Gang of Four (GoF) Mappings

### 2.1 Behavioral Patterns

| Pattern | Eigen Equivalent | Explanation |
| :--- | :--- | :--- |
| **Chain of Responsibility** | `Op1 >> Op2 >> Op3` | Sequential composition (`Flow`) passes data down the chain. |
| **Strategy** | `Op1 | Op2` | The `Choice` operator dynamically selects the strategy (path) to execute. |
| **Observer** | `Op1 & Op2` | `Entanglement` allows multiple observers (Op2) to react to the same input as Op1. |
| **State** | `Tensor` | State is not hidden in classes but explicit in the `WorldTensor`. |
| **Command** | `Atom` | Every `Operator` is a reified Command that can be executed (`.run()`). |
| **Iterator** | `Stream` | Async streams are the fundamental data transport in Eigen. |
| **Interpreter** | `Compiler` | The entire Eigen graph is an AST interpreted or compiled by `Techne`. |
| **Template Method** | `Hamiltonian` | The `Hamiltonian` defines the skeleton; `Atoms` fill the implementation. |

### 2.2 Structural Patterns

| Pattern | Eigen Equivalent | Explanation |
| :--- | :--- | :--- |
| **Decorator** | `@atom` / Higher-Order Op | Wrappers like `Log(Op)` or `Retry(Op)` are functional decorators. |
| **Adapter** | `Port` | `Ports` (Book X) adapt external protocols (HTTP, CLI) to internal logic. |
| **Composite** | `Operator` Graph | An `Operator` can be composed of other `Operators` recursively. |
| **Facade** | `Service` | A high-level `Operator` exposing a clean API over a complex graph. |
| **Proxy** | `Field` / `Ghost` | `Fields` act as proxies for context; `Ghosts` proxy remote actors. |

### 2.3 Creational Patterns

| Pattern | Eigen Equivalent | Explanation |
| :--- | :--- | :--- |
| **Factory** | `Genesis` | The `Genesis` epoch (Book XXXIX) deals with object creation/autopoiesis. |
| **Singleton** | `ConstantAtom` | An atom with immutable, singular state. |
| **Builder** | `>>=` (Bind) | Building pipelines incrementally: `pipe >>= step1; pipe >>= step2`. |

---

## 3. Enterprise Integration Patterns (EIP)

Eigen is natively an integration framework.

| Pattern | Eigen Equivalent | Logic |
| :--- | :--- | :--- |
| **Pipes and Filters** | `>>` | `Source >> Filter >> Sink` |
| **Content-Based Router** | `Choice` / `Switch` | `(A if cond else B)` |
| **Splitter** | `Fork` / `Iter` | Breaks stream into particles. |
| **Aggregator** | `Gather` / `+` | Recombines particles (`Interference`). |
| **Wire Tap** | `Op @ Probe` | Measurement operator (`Observability`). |
| **Message Translator** | `Map` | Transforms schema frames (Relativity). |

---

## 4. Cloud Native Patterns

| Pattern | Eigen Equivalent | Logic |
| :--- | :--- | :--- |
| **Circuit Breaker** | `Op | Fallback` | `Choice` handles failure paths naturally. |
| **Retry** | `Op * N` | `Amplification` repeats the operation. |
| **Sidecar** | `Op & Sidecar` | `Entanglement` runs the sidecar in parallel. |
| **Saga** | `Transaction` | `Void` or `Compensate` operators manage long-running states. |
| **Bulkhead** | `Partition` | Resource isolation via Tensor sharding. |

---
**Eigen Cosmology** | [Previous: Book XLIII](43_API_REFERENCE.md) | [Index](../00_INDEX.md) | [Next: Book XLV](45_FAQ.md) | *© 2025 The Eigen High Council*
