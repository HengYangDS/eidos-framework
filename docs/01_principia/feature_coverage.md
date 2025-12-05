# Feature Coverage & Migration Guide

This document maps traditional data engineering features and legacy Eidos concepts to the new **Eidos** architecture.

## 1. Execution Models

| Legacy / Traditional | Eidos Concept | Mechanism |
| :--- | :--- | :--- |
| **Batch Processing** (Spark/Pandas) | **Vector Lane** | Compiled to `polars.LazyFrame`. Executed on single node or cluster. |
| **Stream Processing** (Flink/Kafka) | **Stream Source** | `Source("kafka://")` returns an Infinite Stream. Compiler switches backend to Streaming Engine. |
| **Hybrid / Lambda** | **Unified DSL** | Same code (`>>`) works for both. No rewrite needed. |

## 2. Concurrency & Parallelism

| Feature | Eidos Implementation |
| :--- | :--- |
| **Multiprocessing** | **Free Lane (No-GIL)** | Python UDFs run in true parallel threads on Python 3.14+. |
| **Distributed Computing** | **Cluster Lane (Ray)** | Large DAGs are partitioned and scheduled on Ray cluster. |
| **Task Parallelism** | **Ensemble Operator (`&`)** | `OpA() & OpB()` compiles to parallel tasks. |
| **Data Parallelism** | **Auto-Sharding** | Compiler automatically shards `Map` operations over data partitions. |

## 3. State & Time

| Feature | Eidos Implementation |
| :--- | :--- |
| **Windowing** | `Window(size, slide)` | Native operator. Compiles to `rolling` (Polars) or State Store (Ray). |
| **Watermarks** | `Watermark(col, delay)` | Handles late data in infinite streams. |
| **Stateful Processing** | `StatefulMap` | Allows an operator to maintain a persistent state (via Ray Actor). |
| **Point-in-Time Join** | `AsOfJoin` | Optimized for financial time-series alignment. |

## 4. Reliability & Governance

| Feature | Eidos Implementation |
| :--- | :--- |
| **Retries** | Configurable in Node | `Map(retry=3)`. Handled by the Runtime Supervisor. |
| **Backpressure** | `Throttle` / Automatic | Ray object store pressure triggers automatic upstream throttling. |
| **Lineage** | **Compile-Time** | Generated from AST before execution. 100% accurate. |
| **Schema Validation** | **Pydantic** | Enforced at every node boundary. |

## 5. AI Integration

| Feature | Eidos Implementation |
| :--- | :--- |
| **LLM Invocation** | `Map(llm_call)` | Trivial to implement. Sidecar optimizes batching. |
| **RAG** | **Vector Store Source** | `Source("chroma://")` to read embeddings. |
| **Auto-Coding** | **Eidos Nous Sidecar** | AI writes the DSL for you. |

## 6. Legacy Migration (Eidos v1/v2)

| Legacy Concept | New Equivalent | Note |
| :--- | :--- | :--- |
| `Hamiltonian` | `Graph` (AST) | Now lazy and immutable. |
| `QuantumField` | `Compiler` | Logic that transforms symbols to physis. |
| `OperatorMixin` | `Operator` class | Simpler Protocol. |
| `HTTPPort` | `RestPort` | Now generates OpenAPI spec. |
| `SQLServerSource` | `Source("db://")` | Generic URI support. |

## 7. Missing Features?

If you find a feature "missing", it is likely **abstracted away**.
*   **Where is the Scheduler?** It's implied. The Runtime schedules tasks based on data availability.
*   **Where is the Connector?** It's in the HAL Adapter.
