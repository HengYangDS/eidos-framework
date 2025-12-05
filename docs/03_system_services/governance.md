# Eidos-Governance: The Registry

## 1. Governance as Code

In traditional platforms, governance (Lineage, Metadata) is an afterthought, often scraped from logs. In Eidos, **Governance is Code**.

Since the AST is a static definition of the entire logic topology, the OS knows exactly:
*   Where data comes from.
*   How it is transformed.
*   Where it goes.
*   What schema it has at every step.

## 2. Lineage Registry

The **Lineage Registry** is a database populated at **Compile Time**.

### 2.1 Column-Level Lineage
Eidos tracks dependency not just at the table level, but at the column level.
```python
# Code
df = source.with_columns(
    c = col("a") + col("b")
)

# Registry Entry
Column(c) -> DependsOn(Column(a), Column(b))
```

### 2.2 Impact Analysis
Because lineage is a graph, we can answer: "If I change the format of column `a`, which downstream dashboards will break?"

## 3. Schema Registry

Eidos enforces schema contracts.

### 3.1 Contract Definition
Every `Source` and `Sink` must define a Schema (using Pydantic or PyArrow).

```python
class TradeSchema(Schema):
    symbol: str
    price: float
    qty: int
```

### 3.2 Runtime Validation
In `Development Mode`, the Runtime validates every batch against the schema. In `Production Mode`, it uses statistical sampling to minimize overhead.

## 4. Catalog

The Catalog is the "File Explorer" of Eidos. It unifies:
*   **Tables**: Database tables, Parquet files.
*   **Streams**: Kafka topics.
*   **Models**: AI models registered via MCP.
*   **Views**: Named Eidos pipelines.

```python
# Accessing the catalog
table = eos.catalog.load("warehouse.public.trades")
```
