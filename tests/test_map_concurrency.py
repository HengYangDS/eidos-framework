import sys
from pathlib import Path
import asyncio
import time

# Ensure src on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from eigen.bosons import Map, Batch  # type: ignore


async def test_list_mapping_order_preserved() -> None:
    data = [1, 2, 3, 4]

    async def fn(x: int) -> int:
        # trivial awaitable
        await asyncio.sleep(0)
        return x * x

    m = Map(fn)
    out = await m(data)
    assert out == [1, 4, 9, 16]


async def test_stream_mapping_order_preserved() -> None:
    async def gen():
        for i in range(5):
            yield i

    async def fn(x: int) -> int:
        # Reverse sleep to create natural out-of-order completion if concurrent
        await asyncio.sleep(0.01 * (5 - x))
        return x * x

    m = Map(fn)
    out = []
    async for v in await m(gen()):
        out.append(v)
    # Since default is preserved (serial for streams), order should be 0..4 squared
    assert out == [0, 1, 4, 9, 16]


async def test_stream_mapping_concurrent_free_shape() -> None:
    async def gen():
        for i in range(6):
            yield i

    async def fn(x: int) -> int:
        await asyncio.sleep(0.02 * (x % 3))
        return x * x

    m = Map(fn, concurrency=3, order="free")
    results = []
    async for v in await m(gen()):
        results.append(v)
    # Same multiset as input squared
    expected = [i * i for i in range(6)]
    assert sorted(results) == sorted(expected)


async def test_batch_over_stream_yields_sizes() -> None:
    # simple Batch over a stream
    async def gen():
        for i in range(7):
            yield i

    b = Batch(3)
    sizes = []
    # Batch.__call__ is an async generator; iterate directly
    async for batch in b(gen()):
        sizes.append(len(batch))
    assert sizes == [3, 3, 1]


async def main() -> None:
    tests = [
        test_list_mapping_order_preserved,
        test_stream_mapping_order_preserved,
        test_stream_mapping_concurrent_free_shape,
        test_batch_over_stream_yields_sizes,
    ]
    failures = 0
    for t in tests:
        try:
            await t()
            print(f"PASS: {t.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"FAIL: {t.__name__}: {e}")
        except Exception as e:
            failures += 1
            print(f"ERROR: {t.__name__}: {e}")
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
