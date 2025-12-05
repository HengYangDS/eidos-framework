# Universal I/O: Streaming Adapters

Eidos v1.1 introduces **Universal I/O**, a set of connectors that allow the framework to interface with external streaming systems like Kafka and Redis.

These connectors are integrated into the `PythonBackend` (Free Lane), enabling rapid prototyping and stream processing without heavy dependencies.

## 1. Kafka Adapter

Supports consuming from and producing to Apache Kafka topics.

### Installation
```bash
pip install eidos-framework[io]
```

### Usage

```python
from eidos import Source, Sink

# Read from Kafka
pipeline = (
    Source("kafka://broker:9092/input-topic")
    >> Map(lambda msg: {"processed": True, **msg})
    >> Sink("kafka://broker:9092/output-topic")
)
```

### Configuration
The URI format is: `kafka://broker:port/topic`
*   **Consumer Group**: Defaults to `eidos-consumer-group`.
*   **Offset**: Defaults to `earliest`.
*   **Format**: Assumes JSON payloads.

## 2. Redis Adapter

Supports Redis Lists (Queue), Streams, and PubSub.

### Usage

```python
# List Mode (Queue)
Source("redis://localhost/my-queue?mode=list")

# Stream Mode (Event Log)
Source("redis://localhost/my-stream?mode=stream")

# PubSub Mode
Sink("redis://localhost/notifications?mode=channel")
```

### Configuration
The URI format is: `redis://host:port/key?mode=...`
*   **mode**: `list`, `stream`, or `channel` (default: `list`).

## 3. Future Roadmap

*   **Polars Integration**: Native streaming support in Vector Lane.
*   **Ray Integration**: Kafka sources for distributed Ray actors.
