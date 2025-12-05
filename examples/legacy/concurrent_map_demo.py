import asyncio
import time
from pathlib import Path
import sys

# Ensure local src on path when running from repository root
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from eidos.bosons import Map  # type: ignore


async def stream(n: int):
    for i in range(n):
        yield i


async def slow_square(x: int) -> int:
    # Simulate IO/CPU delay
    await asyncio.sleep(0.05)
    return x * x


async def main():
    N = 20

    # Serial (order preserved)
    m_serial = Map(slow_square)
    t0 = time.perf_counter()
    serial_out = []
    async for v in await m_serial(stream(N)):
        serial_out.append(v)
    t1 = time.perf_counter()

    # Concurrent, order-free
    m_conc = Map(slow_square, concurrency=5, order="free")
    t2 = time.perf_counter()
    conc_out = []
    async for v in await m_conc(stream(N)):
        conc_out.append(v)
    t3 = time.perf_counter()

    print(f"Serial time: {t1 - t0:.3f}s, items: {len(serial_out)}")
    print(f"Concurrent time: {t3 - t2:.3f}s, items: {len(conc_out)}")
    # Validate results are the same set (order may differ)
    assert sorted(serial_out) == sorted(conc_out)


if __name__ == "__main__":
    asyncio.run(main())
