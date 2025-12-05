# Eidos: The Neuro-Symbolic Logic Operating System

> **"Code is Topology. Execution is Physis. Intelligence is Control."**

Welcome to the documentation for **Eidos** (codenamed *Singularity*).
Eidos is a logic operating system that decouples business logic from physical execution, enabling "Write Once, Run Optimally" across local vectors, distributed clusters, and databases.

## 📚 The Eidos Canon

### [Book I: Principia (The Philosophy)](01_principia/manifesto.md)
The foundational axioms and architectural vision.
*   [Manifesto](01_principia/manifesto.md) - "Physics is the only reality."
*   [Architecture](01_principia/architecture.md) - The Microkernel & 4-Layer Stack.
*   [Concepts & Terminology](01_principia/concepts.md) - The vocabulary of Eidos (AST, Monad, Kernel).

### [Book II: Eidos Zero (The Kernel)](02_kernel_zero/symbolism.md)
The core logic compiler and runtime engine.
*   [Symbolism](02_kernel_zero/symbolism.md) - The DSL, AST, and Static Analysis.
*   [Compilation](02_kernel_zero/compilation.md) - IR generation, Fusion, and Pushdown optimization.
*   [Runtime HAL](02_kernel_zero/runtime_hal.md) - Polars, Ray, and No-GIL Python adapters.

### [Book III: System Services (The Userland)](03_system_services/fs_protocol.md)
Standard services provided by the OS.
*   [File System (Eidos FS)](03_system_services/fs_protocol.md) - The Monad Protocol and Zero-Copy Bus.
*   [Governance](03_system_services/governance.md) - Automated Lineage and Schema Registry.
*   [Standard Library](03_system_services/std_lib.md) - Core operators reference.

### [Book IV: Interfaces (The I/O)](04_interfaces/mcp_neuro_port.md)
Connectivity with the external world.
*   [Neuro-Interface (MCP)](04_interfaces/mcp_neuro_port.md) - Connecting to LLMs (Claude/GPT).
*   [Data-Interface (FlightSQL)](04_interfaces/flight_sql_port.md) - Connecting to BI (Tableau/Excel).
*   [App-Interface (Rest)](04_interfaces/rest_port.md) - Connecting to Web Apps.

### [Book V: Developer Experience (The Tools)](05_developer_experience/cli_guide.md)
Tools for building and debugging.
*   [CLI Guide](05_developer_experience/cli_guide.md) - `eidos create`, `run`, `deploy`.
*   [IDE Integration](05_developer_experience/ide_plugin.md) - PyCharm/VSCode plugins and LSP.

### [Book VI: Extensions (The Ecosystem)](06_extensions/eidos_quant.md)
Domain-specific capability packs.
*   [Eidos Quant](06_extensions/eidos_quant.md) - High-performance financial mathematics.
*   [Integration Guides](06_extensions/integration_guides.md) - DolphinDB, Prefect, etc.

---

## 🚀 Quick Start

```bash
# Install the kernel
pip install eidos-zero

# Install the OS with standard extensions
pip install eidos-os[quant,ray]

# Create a new project
eidos create my-strategy
```

## 🛠️ Status
*   **Kernel**: v0.1 (Alpha) - Symbolic Compiler & Polars Backend.
*   **Python**: 3.14+ (Recommended) / 3.10+ (Supported).
*   **License**: MIT.
