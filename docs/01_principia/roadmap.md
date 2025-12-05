# The Road to Singularity: Eidos Implementation Roadmap

> "The journey of a thousand miles begins with a single step." — Lao Tzu

This document outlines the strategic plan for implementing **Eidos**, moving from a prototype kernel to a fully-fledged Neuro-Symbolic Logic Operating System.

## Phase 1: Ignition (The Kernel)
**Timeline**: Month 1 - Month 3
**Goal**: Build the `Eidos Zero` microkernel and prove the "Logic Compiler" concept with high-performance local execution.

### Milestone 1.1: The Symbolic Frontend (Completed)
- [x] **AST Core**: Define immutable `Node`, `Graph`, and `OpType` structures in `eidos.zero.symbolism`.
- [x] **DSL Implementation**: Overload `>>`, `|`, `&` operators to support Lazy Evaluation.
- [x] **Type System**: Implement `Monad[T]` Monad and Pydantic-based schema validation.
- [x] **Static Analysis**: Implement basic cycle detection and type checking in the frontend.

### Milestone 1.2: The Polars Transpiler (Completed)
- [x] **Transpiler Engine**: Build the core compiler loop (AST -> IR -> Physical Plan).
- [x] **Polars Backend**: Implement the `PolarsCompiler` to translate `Map`, `Filter`, `Source`, `Sink` to `pl.LazyFrame`.
- [x] **UDF Serialization**: Implement `FunctionSerializer` using `cloudpickle` to handle Python closures.
- [x] **Verification**: Benchmark against native Polars code (Target: < 5% overhead).

### Milestone 1.3: Alpha Release (Completed)
- [x] **Packaging**: Release `eidos-zero` v0.1 to PyPI.
- [x] **Documentation**: Complete Book I-VI of the Eidos Canon.
- [x] **Demo**: "10GB ETL Challenge" - Process a large dataset on a laptop using Eidos.

---

## Phase 2: Expansion (The Ecosystem)
**Timeline**: Month 4 - Month 6
**Goal**: Scale out to distributed clusters and provide domain-specific capabilities.

### Milestone 2.1: The Cluster Lane (Completed)
- [x] **Ray Backend**: Implement `RayCompiler` to partition DAGs into distributed tasks.
- [x] **Eidos FS**: Implement the Zero-Copy Bus using Arrow Plasma store.
- [x] **Hybrid Scheduling**: Implement logic to auto-route small tasks to Polars and large tasks to Ray.

### Milestone 2.2: Eidos Quant (In Progress)
- [x] **Standard Library**: Port 10+ core indicators (RSI, MACD, BBands, SMA, etc.) to Eidos operators.
- [x] **DolphinDB Adapter**: Implement SQL Pushdown for DolphinDB data sources (`src/eidos/zero/compiler/dolphindb_backend.py`).
- [x] **Governance**: Implement `LineageRegistry` to auto-generate lineage JSON at compile time.

### Milestone 2.3: Beta Release (Upcoming)
- [ ] **Release**: `eidos-os` v0.5.
- [ ] **CLI**: Release `eidos` command-line tool for project creation and deployment.
- [ ] **Quant Demo**: "Alpha101" - Run full factor calculation on a cluster.

---

## Phase 3: Awakening (The Intelligence)
**Timeline**: Month 7 - Month 9
**Goal**: Integrate AI and turn the system into a self-healing organism.

### Milestone 3.1: The Neuro-Interface (In Progress)
- [x] **MCP Port**: Implement auto-registration of pipelines as MCP Tools.
- [ ] **Semantic Routing**: Implement vector-based routing for natural language queries.
- [ ] **FlightSQL Port**: Implement Arrow Flight server for BI integration.

### Milestone 3.2: The Sidecar (Upcoming)
- [ ] **Healer Daemon**: Build the independent Ray Actor for monitoring.
- [ ] **ECI Protocol**: Define and implement the `CognitiveDriver` protocol.
- [ ] **Self-Healing**: Implement the "Error -> Analyze -> Patch" loop with OpenAI/Claude.

### Milestone 3.3: GA Release (Upcoming)
- [ ] **Release**: `eidos-os` v1.0 GA.
- [ ] **IDE Plugin**: Release PyCharm/VSCode plugins with LSP support.
- [ ] **Singularity**: The system can modify its own code in response to environment changes.
