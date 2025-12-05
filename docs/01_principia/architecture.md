# Eidos: The Neuro-Symbolic Logic Operating System
**Architecture Whitepaper v1.0**

> **"Logic is separate from Physis."**

## 1. Overview

Eidos follows a strict **Microkernel Architecture**. It is not a monolithic framework but a collection of decoupled systems orchestrating data, logic, and intelligence.

The architecture is divided into four concentric layers:
1.  **L1: Eidos Zero (The Kernel)** - Logic compilation and scheduling.
2.  **L2: Eidos System (The Userland)** - System services and standard libraries.
3.  **L3: Eidos Interface (The I/O)** - Ports for AI, BI, and Web.
4.  **L4: Eidos DX (The Experience)** - Tools for developers.

```mermaid
graph TD
    subgraph "L4: Eidos DX"
        IDE[IDE Plugins] --> CLI[Eidos CLI]
        Eidos Nous[Eidos Nous Sidecar]
    end

    subgraph "L3: Eidos Interface"
        MCP[MCP Port]
        Flight[FlightSQL Port]
        Rest[REST Port]
    end

    subgraph "L2: Eidos System"
        Quant[Eidos Quant]
        FS[Eidos FS]
        Gov[Governance]
    end

    subgraph "L1: Eidos Zero"
        Compiler[Symbolic Compiler] --> Runtime[Hybrid Runtime]
    end

    IDE --> Compiler
    MCP --> Compiler
    Flight --> Runtime
    Compiler --> Gov
    Runtime --> FS
```

## 2. Layer 1: Eidos Zero (The Logic Kernel)

The Kernel is the heart of the OS. It contains **no business logic**.

### 2.1 Symbolic Compiler (The Frontend)
*   **Responsibility**: Captures user intent via Python 3.14 AST reflection.
*   **Mechanism**: Lazy evaluation of `>>`, `|`, `&` operators.
*   **Output**: Logical Plan (DAG) in `Substrait` IR.
*   **Static Analysis**: Performs type checking and cycle detection before execution.

### 2.2 Transpiler Engine (The Middle-end)
*   **Responsibility**: Optimization and translation.
*   **Passes**:
    *   **Fusion**: Merges adjacent `Map`/`Filter` nodes into single kernels.
    *   **Pushdown**: Offloads predicates to SQL/Vector engines.
    *   **Pruning**: Removes dead code branches.

### 2.3 Hybrid Runtime HAL (The Backend)
*   **Vector Lane**: `Polars` (Rust) for high-performance local compute (SIMD).
*   **Cluster Lane**: `Ray` for distributed compute (PB-scale).
*   **Free Lane**: `Python 3.14 No-GIL` for complex UDFs.
*   **Pushdown Lane**: `DolphinDB` / `SQL` for in-database compute.

## 3. Layer 2: Eidos System (System Services)

The Userland provides the primitives for building applications.

### 3.1 Eidos FS (File System)
*   **Monad Monad**: The standard data packet. Wraps payload with `TraceID`, `TenantID`, and `Effects`.
*   **Zero-Copy Bus**: Uses Apache Arrow Plasma store for shared memory transport between processes.

### 3.2 Eidos-Governance (Registry)
*   **Lineage Registry**: Automatically generates column-level lineage graphs at compile time.
*   **Schema Registry**: Enforces data contracts at system boundaries.

### 3.3 Eidos Quant (Standard Library)
*   The "DirectX" of Eidos.
*   Provides high-performance, vectorized financial operators (`RSI`, `MACD`, `Backtest`).
*   Implemented in C++/Rust, exposed via Python wrappers.

## 4. Layer 3: Eidos Interface (I/O)

Connectivity with the external world.

### 4.1 MCP Port (Neuro-Interface)
*   **Auto-Registration**: Pipelines are automatically exposed as MCP Tools.
*   **Semantic Routing**: Maps natural language to pipelines.

### 4.2 FlightSQL Port (Data-Interface)
*   **Headless BI**: Exposes Eidos pipelines as a database to Tableau/Excel.
*   **JIT Execution**: Queries trigger just-in-time compilation and execution.

## 5. Layer 4: Eidos DX (Experience)

### 5.1 Eidos Nous Sidecar (AI Ops)
*   **Role**: An autonomous agent (Ray Actor).
*   **Function**: Monitors kernel error streams.
*   **Action**: Uses LLMs to analyze errors and generate hot-patches (new Adapter nodes) to fix pipeline failures automatically.

### 5.2 Eidos LS (Language Server)
*   Provides topology-aware autocompletion and live graph rendering in IDEs.
