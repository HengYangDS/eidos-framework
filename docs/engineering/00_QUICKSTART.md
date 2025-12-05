# Engineering Track: Quickstart

Baseline requirements: Python >= 3.14

Activate the runtime and run a minimal pipeline:

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
    map_ = Map(lambda line: {"value": line})
    sink = CSVSink("./out.csv")
    H = src >> fil >> map_ >> sink
    await H(None)

if __name__ == "__main__":
    asyncio.run(main())
```

## Installation

- Core: `pip install -e .`
- HTTP extras: `pip install -e .[http]`
- SQL Server extras: `pip install -e .[sql]`

### HTTP tips
- Enable simple request logging: set `EIGEN_HTTP_LOGGING=1`.
- Optional API key enforcement: set `EIGEN_HTTP_API_KEY=your-secret` and include header `X-API-Key: your-secret` in requests.
- POST /run enforces `Content-Type: application/json` and will return problem+json (RFC7807) for unsupported media types.
- Trace correlation: send `X-Trace-Id` and the server will echo it back as `x-trace-id`. If omitted, the server generates a trace id and injects it into POST payload as `_context.trace_id` and also returns it in the response header.
- Request size guard: if `HTTPPort(max_body_bytes=...)` is configured and the `Content-Length` exceeds it, POST /run returns `413 Request Entity Too Large` as `application/problem+json`.
- Invalid JSON handling: if POST /run body cannot be parsed as JSON, server returns `400 Bad Request` as `application/problem+json` and includes `x-trace-id`.

Examples:

- Unsupported media type (returns 415 with problem+json):

  `curl -i -X POST http://127.0.0.1:8000/run -H "content-type: text/plain" -d "hello"`

- Unauthorized vs authorized (when API key is enabled):

  - Unauthorized (401):

    `curl -i -X POST http://127.0.0.1:8000/run -H "content-type: application/json" -d '{"text":"hi"}'`

  - Authorized (200):

    `curl -i -X POST http://127.0.0.1:8000/run -H "content-type: application/json" -H "X-API-Key: your-secret" -d '{"text":"hi"}'`

- Streaming:
  - POST /run streams JSON Lines when your pipeline returns an async iterator (response `content-type: application/jsonl`).
  - GET /stream uses Server-Sent Events (response `content-type: text/event-stream`) with lines prefixed by `data:`.

- Invalid JSON (returns 400 with problem+json):

  `curl -i -X POST http://127.0.0.1:8000/run -H "content-type: application/json" -d "{not-json}"`

### SQL Server demo
- Ensure you have network access to a SQL Server and install extras: `pip install -e .[sql]`.
- Set environment variables: `EIGEN_SQL_HOST`, `EIGEN_SQL_USER`, `EIGEN_SQL_PASSWORD`, optional `EIGEN_SQL_DATABASE`.
- Run: `python examples/sql_server_demo.py` (writes `dz_daily_sample.csv`).