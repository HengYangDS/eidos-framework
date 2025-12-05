import os
import sys
from pathlib import Path

# Ensure src on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

# Optional deps
try:
    from fastapi.testclient import TestClient  # type: ignore
    fastapi_available = True
except Exception:
    fastapi_available = False


def _skip(reason: str) -> None:
    print(f"SKIP: {reason}")


def _set_env(key: str, value: str | None):
    old = os.environ.get(key)
    if value is None:
        os.environ.pop(key, None)
    else:
        os.environ[key] = value
    return old


def test_api_key_enforcement() -> None:
    if not fastapi_available:
        return _skip("FastAPI not installed; HTTPPort tests skipped")

    from eigen.techne.ports.http_port import HTTPPort  # type: ignore

    async def handler(payload: dict):
        return {"ok": True, "echo": payload}

    # Enable API key
    old = _set_env("EIGEN_HTTP_API_KEY", "secret")
    try:
        port = HTTPPort()
        port.bind(handler)
        assert port.app is not None
        with TestClient(port.app) as client:
            # Missing key -> 401 problem+json
            r = client.post("/run", json={"msg": "hi"})
            assert r.status_code == 401, r.text
            assert r.headers.get("content-type", "").startswith("application/problem+json")
            body = r.json()
            assert body.get("status") == 401

            # Wrong key -> 401
            r = client.post("/run", headers={"X-API-Key": "wrong", "content-type": "application/json"}, json={})
            assert r.status_code == 401

            # Correct key -> 200
            r = client.post("/run", headers={"X-API-Key": "secret", "content-type": "application/json"}, json={"a": 1})
            assert r.status_code == 200, r.text
            assert r.json().get("ok") is True
    finally:
        _set_env("EIGEN_HTTP_API_KEY", old)


def test_trace_id_passthrough_and_context_injection() -> None:
    if not fastapi_available:
        return _skip("FastAPI not installed; HTTPPort tests skipped")

    from eigen.techne.ports.http_port import HTTPPort  # type: ignore

    async def handler(payload: dict):
        # Echo back payload to observe injected context
        return payload

    old = _set_env("EIGEN_HTTP_API_KEY", None)
    try:
        port = HTTPPort()
        port.bind(handler)
        assert port.app is not None
        with TestClient(port.app) as client:
            # With provided trace id
            trace = "abc123"
            r = client.post("/run", headers={"content-type": "application/json", "X-Trace-Id": trace}, json={"a": 1})
            assert r.status_code == 200, r.text
            assert r.headers.get("x-trace-id") == trace
            body = r.json()
            assert body.get("_context", {}).get("trace_id") == trace

            # Without provided trace id → server generates one and injects
            r2 = client.post("/run", json={"b": 2})
            assert r2.status_code == 200, r2.text
            gen_trace = r2.headers.get("x-trace-id")
            assert gen_trace and isinstance(gen_trace, str)
            b2 = r2.json()
            assert b2.get("_context", {}).get("trace_id") == gen_trace
    finally:
        _set_env("EIGEN_HTTP_API_KEY", old)


def test_request_too_large_returns_413() -> None:
    if not fastapi_available:
        return _skip("FastAPI not installed; HTTPPort tests skipped")

    from eigen.techne.ports.http_port import HTTPPort  # type: ignore

    async def handler(payload: dict):
        return payload

    old = _set_env("EIGEN_HTTP_API_KEY", None)
    try:
        # Set very small max_body_bytes to trigger 413 via Content-Length
        port = HTTPPort(max_body_bytes=5)
        port.bind(handler)
        assert port.app is not None
        with TestClient(port.app) as client:
            r = client.post("/run", json={"long": "0123456789"})
            assert r.status_code == 413, r.text
            assert r.headers.get("content-type", "").startswith("application/problem+json")
            body = r.json()
            assert body.get("status") == 413
    finally:
        _set_env("EIGEN_HTTP_API_KEY", old)


def test_content_type_enforced_for_run() -> None:
    if not fastapi_available:
        return _skip("FastAPI not installed; HTTPPort tests skipped")

    from eigen.techne.ports.http_port import HTTPPort  # type: ignore

    async def handler(payload: dict):
        return payload

    # Ensure no API key for this test
    old = _set_env("EIGEN_HTTP_API_KEY", None)
    try:
        port = HTTPPort()
        port.bind(handler)
        assert port.app is not None
        with TestClient(port.app) as client:
            # Wrong content type -> 415
            r = client.post("/run", data="plain text", headers={"content-type": "text/plain"})
            assert r.status_code == 415, r.text
            assert r.headers.get("content-type", "").startswith("application/problem+json")

            # Correct content type -> 200
            r = client.post("/run", json={"x": 1})
            assert r.status_code == 200
            assert r.json() == {"x": 1}
    finally:
        _set_env("EIGEN_HTTP_API_KEY", old)


def test_invalid_json_returns_400() -> None:
    if not fastapi_available:
        return _skip("FastAPI not installed; HTTPPort tests skipped")

    from eigen.techne.ports.http_port import HTTPPort  # type: ignore

    async def handler(payload: dict):
        return payload

    old = _set_env("EIGEN_HTTP_API_KEY", None)
    try:
        port = HTTPPort()
        port.bind(handler)
        assert port.app is not None
        from fastapi.testclient import TestClient  # type: ignore
        with TestClient(port.app) as client:
            # Send invalid JSON with application/json content type
            r = client.post("/run", data="{not-json}", headers={"content-type": "application/json"})
            assert r.status_code == 400, r.text
            assert r.headers.get("content-type", "").startswith("application/problem+json"), r.headers.get("content-type")
            assert r.headers.get("x-trace-id") is not None
            body = r.json()
            assert body.get("status") == 400
            assert body.get("title") == "Bad Request"
    finally:
        _set_env("EIGEN_HTTP_API_KEY", old)


def test_run_streams_jsonl_when_iterator_returned() -> None:
    if not fastapi_available:
        return _skip("FastAPI not installed; HTTPPort tests skipped")

    from eigen.techne.ports.http_port import HTTPPort  # type: ignore

    async def handler(_payload: dict):
        async def gen():
            for i in range(3):
                # small async yield
                yield {"value": i}
        return gen()

    old = _set_env("EIGEN_HTTP_API_KEY", None)
    try:
        port = HTTPPort()
        port.bind(handler)
        assert port.app is not None
        with TestClient(port.app) as client:
            r = client.post("/run", json={})
            assert r.status_code == 200
            assert r.headers.get("content-type", "").startswith("application/jsonl")
            # Body should contain three lines
            lines = [ln for ln in r.text.splitlines() if ln.strip()]
            assert len(lines) == 3
            assert all("value" in ln for ln in lines)
    finally:
        _set_env("EIGEN_HTTP_API_KEY", old)


def test_sse_stream_endpoint() -> None:
    if not fastapi_available:
        return _skip("FastAPI not installed; HTTPPort tests skipped")

    from eigen.techne.ports.http_port import HTTPPort  # type: ignore

    async def handler(_payload: dict):
        async def gen():
            for i in range(2):
                yield {"tick": i}
        return gen()

    old = _set_env("EIGEN_HTTP_API_KEY", None)
    try:
        port = HTTPPort()
        port.bind(handler)
        assert port.app is not None
        with TestClient(port.app) as client:
            r = client.get("/stream")
            assert r.status_code == 200
            ctype = r.headers.get("content-type", "")
            assert ctype.startswith("text/event-stream")
            text = r.text
            assert text.count("data: ") >= 2
    finally:
        _set_env("EIGEN_HTTP_API_KEY", old)


def main() -> None:
    # Run synchronously like other tests
    failures = 0
    tests = [
        test_api_key_enforcement,
        test_content_type_enforced_for_run,
        test_invalid_json_returns_400,
        test_run_streams_jsonl_when_iterator_returned,
        test_sse_stream_endpoint,
        test_trace_id_passthrough_and_context_injection,
        test_request_too_large_returns_413,
    ]
    for t in tests:
        try:
            t()
            name = getattr(t, "__name__", str(t))
            print(f"PASS: {name}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL: {t.__name__}: {e}")
        except Exception as e:
            failures += 1
            print(f"ERROR: {t.__name__}: {e}")
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
