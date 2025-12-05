# Eidos: The Neuro-Symbolic Logic Operating System

> **"Code is Topology. Execution is Physis. Intelligence is Control."**

Eidos (formerly Eigen Framework, see [Evolution](docs/01_principia/evolution_from_eigen.md)) is a next-generation logic operating system designed to decouple business logic from physical execution. It enables **"Write Once, Run Optimally"** across local vectors, distributed clusters, and databases.

## 🌟 Key Features

*   **Logic Compiler (Eidos Zero)**: Define pipelines as immutable Abstract Syntax Trees (AST) using a lazy Python DSL (`>>`).
*   **Hybrid Runtime**:
    *   **Vector Lane**: High-performance local processing via **Polars** (Rust).
    *   **Cluster Lane**: Distributed execution via **Ray**.
    *   **Pushdown Lane**: SQL generation for **DolphinDB** / **ClickHouse**.
    *   **Free Lane**: True parallelism for Python UDFs using **Python 3.14 (No-GIL)**.
*   **Enterprise Grade**:
    *   **Observability**: Built-in **OpenTelemetry** tracing (`@trace_span`).
    *   **Type Safety**: Runtime verification via **Beartype**.
    *   **Configuration**: 12-Factor App compliant via **Pydantic Settings**.
*   **Neuro-Symbolic Interface**:
    *   **MCP Port**: Automatically exposes pipelines as tools to LLMs (Claude/GPT).
    *   **Sidecar**: AI-driven self-healing daemon that diagnoses and patches runtime errors.
*   **System Services**:
    *   **Governance**: Compile-time lineage extraction.
    *   **Quant Library**: High-performance financial indicators (`RSI`, `MACD`, `Backtest`).

## 📚 Documentation (The Eidos Canon)

See [docs/00_INDEX.md](docs/00_INDEX.md) for the complete specification.

*   **Book I**: Principia (Architecture, Manifesto)
*   **Book II**: Eidos Zero (Kernel Specs)
*   **Book III**: System Services (StdLib, Governance)
*   **Book IV**: Interfaces (MCP, FlightSQL)
*   **Book V**: Developer Experience (CLI, IDE)
*   **Book VI**: Extensions (Quant, Ecosystem)

## 🚀 Quick Start

### Installation

```bash
# Install the OS (includes Polars & Arrow)
pip install eidos-framework

# For distributed computing (optional)
pip install eidos-framework[ray]
```

### Creating a Project

```bash
# Scaffold a new project
eidos create my-strategy --template quant
cd my-strategy
```

### Defining Logic (src/main.py)

```python
from eidos import Source, Sink
from eidos.quant import RSI, MACD

def main():
    # Define topology (Lazy Evaluation)
    flow = (
        Source("s3://market-data/aapl.parquet")
        >> RSI(window=14)
        >> MACD(fast=12, slow=26)
        >> Sink("db://signals")
    )
    return flow

if __name__ == "__main__":
    import eidos
    # Compiles to Polars/Ray and executes
    eidos.run(main())
```

### Running

```bash
# Local Execution (Vector Lane)
eidos run src/main.py

# Distributed Execution (Cluster Lane)
eidos run src/main.py --cluster ray://localhost:6379
```

## 🧠 AI Integration

Start the MCP Server to expose your pipelines to Claude Desktop or other MCP Clients:

```python
from eidos.interfaces.mcp import MCPPort
from my_strategy import main

port = MCPPort("MyQuantServer")
port.register_pipeline("run_strategy", main, "Executes the alpha strategy")
port.run()
```

## 🛠️ Status

*   **Kernel**: v1.0-Alpha (Stable DSL & Transpiler)
*   **Backends**: Polars (Ready), DolphinDB (Ready), Ray (Beta)
*   **Intelligence**: MCP Port (Ready), Sidecar (Beta)

## License

MIT
