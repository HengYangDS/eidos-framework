# Engineering Track: Observability & Debuggability

Status: initial stub. Baseline: Python >= 3.14.

- Logging: standard library logging with structured context (future helper)
- Metrics: OpenTelemetry metrics exporter (optional extra `otlp`)
- Tracing: propagation of trace IDs through operator calls (future)
- Health & readiness: HTTPPort exposes /health and /ready endpoints when enabled
