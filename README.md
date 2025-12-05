# Eigen Framework

The Physics of Software.

## Requirements
- Python >= 3.14
- OS: Linux/macOS/Windows

Optional integrations (install when needed):
- HTTP Port: `pip install -e .[http]`
- SQL Server Source: `pip install -e .[sql]`

## Documentation
See [docs/00_INDEX.md](docs/00_INDEX.md).

## Public API
- Top-level imports are provided for the most common types and operators:

```python
from eigen import activate, Map, Filter, Batch, Operator, Flow, Tensor, Interference
```

## Quickstart

```python
import asyncio
from eigen.runtime import activate
from eigen.techne.sources.file_source import FileSource
from eigen.techne.operators.standard import Map, Filter
from eigen.techne.emitters.csv_sink import CSVSink

async def main():
    activate()  # set QuantumField as the active field
    src = FileSource("./data.txt")
    fil = Filter(lambda line: "a" in line)
    mapper = Map(lambda line: {"value": line})
    sink = CSVSink("./out.csv")
    H = src >> fil >> mapper >> sink
    await H(None)

if __name__ == "__main__":
    asyncio.run(main())
```

## Examples
See `examples/` directory.

- Minimal end-to-end demo:
  - `python examples/eigen_standard_demo.py`

- Map concurrency demo:
  - `python examples/concurrent_map_demo.py`

- HTTP quickstart server (requires extras):
  - `pip install -e .[http]`
  - Optionally enable simple request logs: set `EIGEN_HTTP_LOGGING=1`
  - Optional API key enforcement: set `EIGEN_HTTP_API_KEY=your-secret` (client must send `X-API-Key`)
  - Trace ID: send `X-Trace-Id` to correlate; server echoes it back as `x-trace-id`. If not provided, server generates one and injects into POST payload `_context.trace_id`.
  - Request size guard: if `HTTPPort(max_body_bytes=...)` is set and `Content-Length` exceeds it, POST /run returns 413 as RFC7807 `application/problem+json`.
  - Invalid JSON: if POST /run body cannot be decoded as JSON, returns 400 as RFC7807 `application/problem+json` with an `x-trace-id` header.
  - Start: `python examples/http_quickstart.py`
  - Test JSON:
    - `curl -X POST http://127.0.0.1:8000/run -H "content-type: application/json" -d '{"text":"hello"}'`
  - Stream SSE:
    - `curl http://127.0.0.1:8000/stream`
  - When API key is enabled, add header: `-H "X-API-Key: your-secret"`

- SQL Server demo (requires extras and a reachable SQL Server):
  - `pip install -e .[sql]`
  - Set environment variables:
    - `EIGEN_SQL_HOST`, `EIGEN_SQL_USER`, `EIGEN_SQL_PASSWORD`, optional `EIGEN_SQL_DATABASE`
  - Run: `python examples/sql_server_demo.py`
  - Output CSV: `dz_daily_sample.csv` at repo root

## Testing
- Preferred: use the local runner to avoid site-packages collisions and ensure `src/` is on the path.

```
python scripts/run_tests.py
```

- You can also run individual demos/tests directly:
  - `python examples/eigen_standard_demo.py`
  - `python tests/test_http_port.py` (skips automatically if FastAPI/Uvicorn are not installed)

## Repository
Remote (GitHub): https://github.com/HengYangDS/eigen-framework

### Clone locally
```
git clone https://github.com/HengYangDS/eigen-framework.git
cd eigen-framework
```

### Install
```
pip install -e .
```
