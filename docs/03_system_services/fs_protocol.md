# Eidos FS: The File System Protocol

## 1. The Data Packet (Monad)

In Eidos, "Everything is a File" is replaced by **"Everything is an Monad"**.

The `Monad[T]` is the fundamental unit of data transport. It is a Monad that wraps the raw data.

```python
@dataclass(frozen=True)
class Monad(Generic[T]):
    payload: T              # The actual data (e.g., Arrow Table)
    context: Context        # Metadata
    effects: list[Effect]   # Side effects
```

### 1.1 Context
Immutable metadata that travels with the data.
*   `trace_id`: For observability.
*   `span_id`: Current logical step.
*   `tenant_id`: Ownership.
*   `schema_version`: For schema evolution.

### 1.2 Effects
Eidos embraces **Algebraic Effects**. A function does not "print to console" or "write to disk" directly. Instead, it returns an `Effect` description.
*   `WriteEffect(path, data)`
*   `LogEffect(level, msg)`

The Runtime handles these effects, allowing for:
*   **Sandboxing**: Testing logic without touching real IO.
*   **Replay**: Re-running logic with recorded IO.

## 2. The Zero-Copy Bus

Eidos FS implements a virtual file system over shared memory.

### 2.1 Plasma Store
When running in `Cluster Lane` (Ray), Eidos uses the Plasma Object Store. Envelopes are serialized once to shared memory, and all local processes read them via memory mapping (`mmap`).

### 2.2 Arrow IPC
When moving between languages (Python -> Rust), Eidos uses the Arrow C Data Interface to pass pointers. No serialization occurs.

## 3. Streams

Eidos FS treats all data as **Streams**.
*   **Finite Stream**: A file or a batch query.
*   **Infinite Stream**: A Kafka topic or a WebSocket.

The API is unified:
```python
# Reads file (Finite)
eos.read("s3://data.parquet")

# Reads topic (Infinite)
eos.read("kafka://broker/topic")
```
