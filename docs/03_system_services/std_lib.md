# Standard Library: The Core Operators

The Standard Library (`eidos.std`) provides the fundamental building blocks for constructing pipelines. These operators are **Polymorphic** (they work on Streams, Batches, and Scalars) and **Backend-Agnostic** (they compile to Polars, Ray, or SQL).

> **Note**: All operators here are **Lazy**. They return an updated Graph, not data.

## 1. Transformation

### `Map(fn: Callable | Expr)`
Applies a function to every element in the stream.
*   **Python UDF**: `Map(lambda x: x + 1)` (Runs in Free Lane / No-GIL).
*   **Expression**: `Map(col("price") * 2)` (Runs in Vector Lane / Polars).

### `Filter(predicate: Callable | Expr)`
Retains elements where the predicate is True.
*   **Pushdown**: Automatically pushed down to the database if possible.
*   **Example**: `Filter(col("status") == "ACTIVE")`

### `Project(*cols)` / `Select(*cols)`
Selects a subset of columns or renames them.
*   **Example**: `Project("id", "name", alias="new_name")`

### `WithColumns(**kwargs)`
Adds new columns or updates existing ones (similar to Polars).
*   **Example**: `WithColumns(total = col("price") * col("qty"))`

## 2. Aggregation & Windowing

### `Window(size: str, slide: str, by: str = None)`
Defines a sliding or tumbling window over time.
*   **Syntax**: `Window("5m", "1m")` (5-minute window, sliding every 1 minute).
*   **Usage**: Must be followed by an aggregation operator.
```python
stream >> Window("1h") >> Mean()
```

### `Group(by: str | List[str])`
Partitions the stream by a key.
*   **Example**: `Group("symbol") >> Agg(max("price"))`

### `Reduce(fn: Callable)` / `Fold`
Accumulates values into a single result.
*   **Warning**: This forces a "Shuffle" in distributed execution.

### `Agg(*exprs)`
Performs multiple aggregations in parallel.
*   **Example**: `Agg(min("price"), max("price"), count())`

## 3. Set & Relational Operations

### `Join(other, on, how="inner")`
Joins two streams.
*   **Types**: `inner`, `left`, `outer`, `cross`, `semi`, `anti`.
*   **Example**: `trades >> Join(quotes, on="symbol", how="left")`

### `Union(other)`
Merges two streams with the same schema.
*   **Analogy**: SQL `UNION ALL`.

### `Sort(by, descending=False)`
Sorts the stream.
*   **Distributed**: Triggers a global shuffle.

### `Distinct(on=None)` / `Unique`
Removes duplicate records.

### `Limit(n)` / `Head(n)`
Returns the first `n` elements.
*   **Optimization**: Pushed down to Source.

## 4. Time Series (Temporal)

### `AsOfJoin(other, on, by, tolerance)`
Performs a point-in-time join (critical for Quant). Matches the closest previous timestamp.
*   **Example**: Joining Trades with Quotes.

### `Lag(k)` / `Shift(k)`
Shifts the series by `k` steps.
*   **Example**: `price - Lag(1)` (Calculate price change).

### `Resample(rule)`
Downsamples or Upsamples time series data.
*   **Example**: `Resample("1d") >> Last()` (Daily Close).

## 5. IO (Input / Output)

### `Source(uri: str, schema=None)`
Reads data from a URI.
*   **Supported Protocols**: `s3://`, `file://`, `http://`, `db://`, `kafka://`.
*   **Format**: Auto-detected (Parquet, CSV, JSON, Delta).

### `Sink(uri: str, mode="append")`
Writes data to a URI.
*   **Modes**: `append`, `overwrite`, `error`.

## 6. Control Flow

### `Tee(n)`
Splits the stream into `n` identical copies. Used for branching.

### `Barrier()`
Synchronization point. Waits for all upstream tasks to complete before proceeding.

### `Cache()`
Persists the intermediate result in memory (or Plasma store) to avoid re-computation.
