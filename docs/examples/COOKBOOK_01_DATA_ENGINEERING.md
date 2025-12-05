# Cookbook I: Data Engineering with Eigen

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

This cookbook demonstrates how to build production-grade **Data Engineering**
pipelines using the Eigen Framework.

## Scenario 1: The Lakehouse Ingestion (ETL)

**Goal**: Ingest 1TB of JSON logs from S3, validate schema, partition by date,
and write to Delta Lake (Parquet).

### 1.1 The Pipeline Definition

```python
from eigen.core import Flow, Operator
from eigen.techne import S3Source, ParquetSink
from eigen.bosons import Map, Filter, Batch
from eigen.logos import Knowledge
from datetime import datetime

# --- 1. Define Fermions (Data) ---
@dataclass
class RawLog(Knowledge):
    timestamp: str
    service: str
    level: str
    message: str

@dataclass
class CleanLog(Knowledge):
    ts: datetime
    service: str
    is_error: bool
    payload: dict

# --- 2. Define Bosons (Logic) ---

class ParseLog(Operator[RawLog, CleanLog]):
    async def __call__(self, raw: RawLog) -> CleanLog:
        ts = datetime.fromisoformat(raw.timestamp)
        return CleanLog(
            ts=ts,
            service=raw.service.lower(),
            is_error=(raw.level == "ERROR"),
            payload={"msg": raw.message}
        )

# Filter out DEBUG noise
IsSignificant = Filter(lambda log: log.level in ["INFO", "WARN", "ERROR"])

# --- 3. The Pipeline ---

# S3 -> Filter -> Parse -> Batch -> Parquet

Pipeline = (
    S3Source("s3://bucket/raw/*.json") 
    >> IsSignificant 
    >> ParseLog() 
    >> Batch(size=1000, timeout=1.0) 
    >> ParquetSink("s3://bucket/clean/")
)

```

### 1.2 Handling Bad Data (The Dead Letter Queue)

Real-world data is dirty. We use the **Choice Operator** (`|`) to handle
failures without stopping the stream.

```python
class ErrorHandler(Operator):
    async def __call__(self, error: Exception) -> None:

        # Send to DLQ (Dead Letter Queue)
        await SQS.send("dlq-queue", str(error))

# Robust Parser

# If ParseLog fails, the particle tunnels to ErrorHandler
SafeParse = ParseLog() | ErrorHandler()

Pipeline = (
    S3Source(...) 
    >> IsSignificant 
    >> SafeParse 
    >> Batch(...) 
    >> ParquetSink(...)
)

```

## Scenario 2: Change Data Capture (CDC)

**Goal**: Stream changes from Postgres, enrich with Redis, and push to
Elasticsearch.

```python

# --- The Hamiltonian ---

# 1. The Source (Gravitational Wave Detector)
CDCSource = PostgresWalSource(table="users")

# 2. Enrichment (Field Interaction)

# We bind the Redis cache as a Field
RedisField = Field("redis_conn")

@atom
async def EnrichUser(user: dict) -> dict:

    # Measure the field
    redis = RedisField.get()

    # Fetch metadata
    meta = await redis.get(f"meta:{user['id']}")
    return {**user, "meta": meta}

# 3. Indexing (Sink)
ElasticSink = ElasticsearchSink(index="users_v1")

# 4. The Topology

# We define a Parallel flow for reliability

# If ES fails, we don't want to crash the CDC stream.

# We use a Circuit Breaker.
SafeIndex = ElasticSink | CircuitBreaker() | LogError()

Pipeline = (
    CDCSource 
    >> EnrichUser 
    >> SafeIndex
)

# 5. Execution (With Field Injection)
with RedisField.context(redis_pool):
    Pipeline.run()

```

## Scenario 3: Recursive Partitioning

**Goal**: Process a directory tree recursively.

```python
from eigen.operators import Recursion

# Define a fractal operator
@atom
async def ProcessDir(path: str):
    if is_file(path):
        return ProcessFile(path)
    else:

        # Recursion: The operator calls itself

        # List dir, then Map ProcessDir over children
        return ListDir(path) >> Map(ProcessDir)

RootOp = ProcessDir("/data")

```

## Scenario 4: Data Quality Gates

**Goal**: Ensure that a dataset meets quality standards before promoting it.

```python
from eigen.mechanics import Thermodynamics

# Define Quality Metric
def purity_score(batch):
    return len([x for x in batch if x.is_valid]) / len(batch)

# The Gate
QualityGate = Filter(lambda batch: purity_score(batch) > 0.99)

# If quality drops, trigger alert and stop
ProductionLine = (
    BatchProcess 
    >> QualityGate 
    >> PromoteToProd
) | Alert("Data Quality Breach")

```

This utilizes the **Destructive Interference** principle to annihilate bad
batches.

## Scenario 5: Zero-Copy Transport (Arrow)

**Goal**: Move data between Python and Rust without serialization overhead.

```python

# Using Eigen's built-in Arrow support

# This uses Shared Memory (Plasma Store)

PySource = ArrowSource("data.arrow")
RustProcessor = ExternalOperator("rust_binary")

# The flow happens via memory pointers, not bytes
HighSpeedPipeline = PySource >> RustProcessor >> ArrowSink("out.arrow")

```

---
**Eigen Cosmology** | [Previous: Book XLI](../cosmos/41_THE_ARCHIVES.md) | [Index](../00_INDEX.md) | [Next: Cookbook II](COOKBOOK_02_QUANTUM_FINANCE.md) | *© 2025 The Eigen High Council*
