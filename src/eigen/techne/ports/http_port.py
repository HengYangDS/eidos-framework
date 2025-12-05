from typing import Any, Optional
from collections.abc import Callable, Awaitable, AsyncIterator
from ...gauge.symmetry import OperatorMixin
import asyncio
import os
import uuid
import json

# Optional HTTP stack
try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse, StreamingResponse
    import uvicorn
except ImportError:
    FastAPI = None
    uvicorn = None

class HTTPPort(OperatorMixin):
    """
    A Boundary Port that exposes a Hamiltonian (Pipeline) as an HTTP API.
    """
    def __init__(self,
                 host: str = "127.0.0.1",
                 port: int = 8000,
                 *,
                 timeout: Optional[float] = None,
                 max_concurrency: Optional[int] = None,
                 max_body_bytes: Optional[int] = None):
        self.host = host
        self.port = port
        self.app = FastAPI() if FastAPI else None
        self.name = f"HTTPPort({host}:{port})"
        self.pipeline_handler: Optional[Callable[[Any], Awaitable[Any]]] = None
        self._on_startup: Optional[Callable[[], Awaitable[None] | None]] = None
        self._on_shutdown: Optional[Callable[[], Awaitable[None] | None]] = None
        self._ready: bool = False
        self._timeout = timeout
        self._max_body_bytes = max_body_bytes
        self._sema: Optional[asyncio.Semaphore] = (
            asyncio.Semaphore(max_concurrency) if (isinstance(max_concurrency, int) and max_concurrency > 0) else None
        )
        self._logging_enabled = str(os.getenv("EIGEN_HTTP_LOGGING", "")).lower() in ("1", "true", "yes", "on")
        # Optional simple API key auth
        self._api_key: Optional[str] = os.getenv("EIGEN_HTTP_API_KEY") or None

    def bind(self,
             handler: Callable[[Any], Awaitable[Any]],
             *,
             on_startup: Optional[Callable[[], Awaitable[None] | None]] = None,
             on_shutdown: Optional[Callable[[], Awaitable[None] | None]] = None):
        """
        Binds a Hamiltonian to this Port.
        """
        self.pipeline_handler = handler
        self._on_startup = on_startup
        self._on_shutdown = on_shutdown
        if self.app:
            app = self.app

            @app.on_event("startup")
            async def _startup():
                if self._on_startup:
                    res = self._on_startup()
                    if asyncio.iscoroutine(res):
                        await res
                self._ready = True

            @app.on_event("shutdown")
            async def _shutdown():
                self._ready = False
                if self._on_shutdown:
                    res = self._on_shutdown()
                    if asyncio.iscoroutine(res):
                        await res

            @app.exception_handler(Exception)
            async def _unified_error_handler(_, exc: Exception):
                problem = {
                    "type": "about:blank",
                    "title": exc.__class__.__name__,
                    "detail": str(exc),
                    "status": 500,
                }
                return JSONResponse(problem, status_code=500, media_type="application/problem+json")

            @self.app.post("/run")
            async def run_pipeline(request: Request):
                # Ensure a trace id exists for this request (passthrough or generate)
                trace_id = request.headers.get("x-trace-id") or uuid.uuid4().hex

                # API key enforcement (optional)
                if self._api_key is not None:
                    supplied = request.headers.get("x-api-key")
                    if supplied != self._api_key:
                        problem = {
                            "type": "about:blank",
                            "title": "Unauthorized",
                            "detail": "Missing or invalid API key",
                            "status": 401,
                        }
                        return JSONResponse(problem, status_code=401, media_type="application/problem+json", headers={"x-trace-id": trace_id})

                # optional size guard using Content-Length
                if self._max_body_bytes is not None:
                    cl = request.headers.get("content-length")
                    if cl is not None:
                        try:
                            if int(cl) > int(self._max_body_bytes):
                                problem = {
                                    "type": "about:blank",
                                    "title": "Request Entity Too Large",
                                    "detail": f"Content-Length exceeds max_body_bytes={self._max_body_bytes}",
                                    "status": 413,
                                }
                                return JSONResponse(problem, status_code=413, media_type="application/problem+json", headers={"x-trace-id": trace_id})
                        except ValueError:
                            # bad header, ignore guard
                            pass

                # Enforce content-type application/json
                ctype = request.headers.get("content-type", "").lower()
                if "application/json" not in ctype:
                    problem = {
                        "type": "about:blank",
                        "title": "Unsupported Media Type",
                        "detail": "Content-Type must be application/json",
                        "status": 415,
                    }
                    return JSONResponse(problem, status_code=415, media_type="application/problem+json", headers={"x-trace-id": trace_id})

                # Parse JSON body with graceful 400 on decode errors
                try:
                    data = await request.json()
                except Exception as e:
                    problem = {
                        "type": "about:blank",
                        "title": "Bad Request",
                        "detail": f"Invalid JSON payload: {str(e)}",
                        "status": 400,
                    }
                    return JSONResponse(problem, status_code=400, media_type="application/problem+json", headers={"x-trace-id": trace_id})

                # inject minimal context with trace_id
                try:
                    if isinstance(data, dict):
                        ctx = data.get("_context")
                        if not isinstance(ctx, dict):
                            ctx = {}
                            data["_context"] = ctx
                        ctx["trace_id"] = trace_id
                except Exception:
                    pass

                async def _invoke():
                    assert self.pipeline_handler is not None
                    return await self.pipeline_handler(data)

                # concurrency gating
                if self._sema:
                    async with self._sema:
                        if self._logging_enabled:
                            print(f"[{self.name}] /run start")
                        result = await (_invoke() if self._timeout is None else asyncio.wait_for(_invoke(), self._timeout))
                else:
                    if self._logging_enabled:
                        print(f"[{self.name}] /run start")
                    result = await (_invoke() if self._timeout is None else asyncio.wait_for(_invoke(), self._timeout))

                # If result is an async iterator → stream JSON lines
                if isinstance(result, AsyncIterator):
                    async def streamer():
                        if self._logging_enabled:
                            print(f"[{self.name}] /run streaming start")
                        async for item in result:
                            # Proper JSONL: one valid JSON object per line
                            try:
                                line = json.dumps(item, ensure_ascii=False)
                            except Exception:
                                # Fallback to string if not JSON-serializable
                                line = str(item)
                            yield (line + "\n").encode("utf-8")
                        if self._logging_enabled:
                            print(f"[{self.name}] /run streaming end")

                    return StreamingResponse(streamer(), media_type="application/jsonl", headers={"x-trace-id": trace_id})
                if self._logging_enabled:
                    print(f"[{self.name}] /run done")
                # Wrap scalar/list results to attach trace header
                return JSONResponse(result, headers={"x-trace-id": trace_id})
            
            @self.app.get("/health")
            async def health():
                return {"status": "ok", "system": "Eigen v1.0"}

            @self.app.get("/ready")
            async def ready():
                return {"ready": self._ready}

            @self.app.get("/stream")
            async def stream(request: Request):
                trace_id = request.headers.get("x-trace-id") or uuid.uuid4().hex
                if self._api_key is not None:
                    supplied = request.headers.get("x-api-key")
                    if supplied != self._api_key:
                        problem = {
                            "type": "about:blank",
                            "title": "Unauthorized",
                            "detail": "Missing or invalid API key",
                            "status": 401,
                        }
                        return JSONResponse(problem, status_code=401, media_type="application/problem+json", headers={"x-trace-id": trace_id})

                async def _invoke():
                    assert self.pipeline_handler is not None
                    # default empty input for streaming producer pipelines
                    return await self.pipeline_handler({})

                if self._sema:
                    async with self._sema:
                        result = await (_invoke() if self._timeout is None else asyncio.wait_for(_invoke(), self._timeout))
                else:
                    result = await (_invoke() if self._timeout is None else asyncio.wait_for(_invoke(), self._timeout))

                if not isinstance(result, AsyncIterator):
                    # Coerce single value into a one-item stream
                    async def one():
                        yield result
                    result_iter = one()
                else:
                    result_iter = result

                async def sse():
                    if self._logging_enabled:
                        print(f"[{self.name}] /stream start")
                    async for item in result_iter:
                        try:
                            payload = json.dumps(item, ensure_ascii=False)
                        except Exception:
                            payload = str(item)
                        yield (f"data: {payload}\n\n").encode("utf-8")
                    if self._logging_enabled:
                        print(f"[{self.name}] /stream end")

                return StreamingResponse(sse(), media_type="text/event-stream", headers={"x-trace-id": trace_id})

    async def __call__(self, input: Any) -> Any:
        """
        Starting the Port acts as a blocking call (server loop).
        Input is ignored or treated as config.
        """
        if not self.app or not uvicorn:
            raise RuntimeError("HTTPPort requires optional dependencies 'fastapi' and 'uvicorn'.")
        
        print(f"[{self.name}] Starting server...")
        config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
