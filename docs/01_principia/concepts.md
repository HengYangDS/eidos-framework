# Book I: Concepts & Terminology

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "The beginning of wisdom is the definition of terms." — Socrates

This document defines the core concepts and vocabulary of **Eidos**, mapping the "Physics of Software" metaphors to concrete engineering terms.

## Core Architectural Concepts

### 1. Eidos Zero (The Kernel)
The microkernel of the system. It contains **no business logic**. Its sole responsibility is to:
1.  **Capture** user intent as an Abstract Syntax Tree (AST).
2.  **Compile** the AST into an optimized Intermediate Representation (IR).
3.  **Dispatch** the IR to the appropriate physical backend (Polars, Ray, etc.).
*   *Analogy*: The Linux Kernel (vmlinuz).

### 2. Eidos-Space (The Userland)
The layer where developers work. It includes the DSL, standard libraries (like `eidos-quant`), and application logic.
*   *Analogy*: Userspace (glibc, bash, apps).

### 3. Eidos-Nous (The Intelligence)
The cognitive subsystem. It includes the **Neuro-Interface (MCP)** and the **Sidecar (Healer)**. It treats AI not as a tool, but as a system component.
*   *Analogy*: The frontal cortex of a biological organism.

---

## The Physics of Execution

### Symbolism (Symbolic Execution)
The separation of definition from execution. In Eidos, writing code (e.g., `a >> b`) does not execute it. It builds a **Symbolic Graph**. This allows for static analysis, optimization, and retargeting before a single byte of data is processed.

### Lazy Evaluation
The execution strategy where computation is deferred until the last possible moment (e.g., when `collect()` or `sink()` is called). This enables **Fusion** (merging multiple operations into one) and **Pushdown** (sending logic to the database).

### Monad Monad (`Monad[T]`)
The standard container for all data moving through the system. It wraps the raw payload (e.g., an Arrow RecordBatch) with metadata:
*   **TraceID**: For distributed tracing.
*   **TenantID**: For multi-tenant isolation.
*   **Effects**: Instructions for side effects (IO, Logging).

---

## The Glossary

### A

#### AST (Abstract Syntax Tree)
A tree representation of the abstract syntactic structure of the pipeline. Eidos compiles this into an execution plan.

#### Adapter
A component in the HAL (Hardware Abstraction Layer) that translates Eidos IR into backend-specific code (e.g., Polars Expressions, Ray Tasks, SQL).

### C

#### Compiler
The component that transforms the Logical Plan (AST) into a Physical Plan. It performs optimizations like Fusion and Predicate Pushdown.

#### Context
Immutable metadata that travels with the data Monad, defining the "environment" of execution (auth, tracing).

### D

#### DSL (Domain Specific Language)
The Python API provided by Eidos (using `>>`, `|`, `&`) to define logic topologies.

### H

#### HAL (Hardware Abstraction Layer)
The runtime layer that abstracts physical compute engines (Polars, Ray, DolphinDB) behind a unified interface.

### J

#### JIT (Just-In-Time) Compilation
The process of compiling the symbolic graph into executable code (machine code or optimized bytecode) at runtime, tailored to the specific data distribution and hardware.

### K

#### Kernel
See **Eidos Zero**.

### M

#### MCP (Model Context Protocol)
The standard protocol used by Eidos to expose its capabilities to Large Language Models (LLMs).

#### Monad
A design pattern used in the Monad to handle side effects and context in a purely functional way.

### N

#### No-GIL (Free-Threading)
Refers to Python 3.13+ feature where the Global Interpreter Lock is optional. Eidos utilizes this for true parallelism in Python UDFs.

### P

#### Polars
A blazing fast DataFrame library implemented in Rust. Eidos uses it as the default vector execution engine.

#### Pushdown
An optimization technique where filters and aggregations are moved "down" to the data source (e.g., the database) to minimize data transfer.

### R

#### Ray
A framework for scaling AI and Python applications. Eidos uses it for distributed cluster scheduling.

### S

#### Sidecar
An autonomous AI agent (Eidos Nous) that runs alongside the kernel, monitoring for errors and performing hot-patches.

#### Substrait
A cross-language serialization format for relational algebra. Eidos uses it as the Intermediate Representation (IR).

### T

#### Topology
The structure of the computation graph. "Code is Topology."

#### Transpiler
A compiler that translates source code from one language to another (e.g., Eidos DSL to SQL).

### Z

#### Zero-Copy
A data transfer method where data is not copied between memory regions. Eidos uses Apache Arrow to achieve zero-copy between Python, Rust, and different processes.
