# IDE Integration & Language Server

Eidos provides a comprehensive **Language Server Protocol (LSP)** implementation to support PyCharm (via plugin) and VSCode (via extension).

This integration transforms the IDE from a text editor into a **Logic Topology Visualizer**.

## 1. The Logic Graph View

When you open a Python file importing `eidos`, the plugin activates the **Topology Sidecar**.

### 1.1 Live Rendering
As you type `>>` or `|`, the plugin:
1.  Sends the current file content to the `eidos-ls` server.
2.  `eidos-ls` parses the AST (using `eidos.zero.symbolism` itself, not regex).
3.  It returns a `Graph` JSON payload.
4.  The IDE renders the DAG using Webview (React Flow).

### 1.2 Bi-directional Navigation
*   **Code -> Graph**: Click on a line of code (e.g., `Filter(...)`). The corresponding node in the graph highlights.
*   **Graph -> Code**: Double-click a node in the graph. The cursor jumps to the definition in the source code.

## 2. Intelligent Features

### 2.1 Type Inference (Schema Propagation)
Because the AST is known, the LSP can predict downstream schemas.

```python
# Source has schema {price: float}
flow = Source("data") >> Map(lambda x: x.price) 

# When typing the next operator...
# >> Filter(lambda y: y.|) 
# The autocomplete suggests 'price' because it knows 'y' is a record with 'price'.
```

### 2.2 Data Preview (Lazy Peek)
Hover over any `SymbolicStream` variable. The IDE shows a **"Peek"** tooltip.
*   **Mechanism**: The LSP triggers a background job: `stream.limit(5).collect()`.
*   **Result**: A small table (First 5 rows) appears in the tooltip.
*   **Benefit**: Debug logic without running the whole pipeline.

### 2.3 Performance Hints
The Static Analyzer marks inefficient patterns.
*   **Warning**: "You are using a Python `Map` loop here. Consider using `eidos.quant.VectorizedMap` for 100x speedup."
*   **Error**: "Type mismatch: Upstream produces `str`, Downstream expects `int`."

## 3. Eidos Nous Integration (The Copilot)

The IDE plugin connects directly to the **Eidos Nous Sidecar**.

### 3.1 Context Awareness
Eidos Nous doesn't just read the text buffer; she reads the **Compiled AST** and the **Database Schema**.
*   **Prompt**: "Filter by high volume."
*   **Eidos Nous's Thought**: "I see the source table has a column 'vol_24h'. I will use that."
*   **Action**: Inserts `>> Filter(col("vol_24h") > 1000000)`.

### 3.2 Natural Language Refactoring
Select a block of code -> Right Click -> "Refactor with Eidos".
*   **Convert Loop to Vector**: Transforms `for` loops into `Map` operators.
*   **Pushdown**: Suggests moving filters up the chain.

## 4. Installation

### PyCharm
Search for "Eidos Support" in the Marketplace.

### VSCode
Install `eidos-vscode` extension.
