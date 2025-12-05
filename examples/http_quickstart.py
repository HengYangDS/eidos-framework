import asyncio
import sys
from pathlib import Path

# Ensure local src is importable when run from repo root
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from eigen.runtime import activate  # type: ignore
from eigen.techne.ports.http_port import HTTPPort  # type: ignore


async def pipeline(payload: dict):
    """
    Minimal demo pipeline.
    - If payload has {"text": str} → return uppercased echo {"result": str}
    - Otherwise (including GET /stream which invokes with {}), stream numbers 0..4 as SSE
    """
    if isinstance(payload, dict) and "text" in payload:
        text = str(payload.get("text", ""))
        return {"result": text.upper()}

    async def gen():
        for i in range(5):
            await asyncio.sleep(0.1)
            yield {"value": i}

    return gen()


async def main() -> None:
    activate()
    port = HTTPPort(host="127.0.0.1", port=8000, timeout=5.0, max_concurrency=100, max_body_bytes=1_000_000)
    port.bind(pipeline)
    await port(None)  # start server


if __name__ == "__main__":
    asyncio.run(main())
