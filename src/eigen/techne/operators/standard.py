from collections.abc import Callable, AsyncIterator, Awaitable
from typing import Any, Optional, Literal
from ...gauge.symmetry import OperatorMixin
import inspect
import asyncio

class Map(OperatorMixin):
    """
    A Boson that transforms the state of a particle.
    Applies a function f(x) to each item in the stream.
    """
    def __init__(self,
                 fn: Callable[[Any], Any | Awaitable[Any]],
                 *,
                 concurrency: Optional[int] = None,
                 order: Literal["preserved", "free"] = "preserved"):
        self.fn = fn
        self.name = f"Map({getattr(fn, '__name__', 'fn')})"
        self._concurrency = concurrency if (isinstance(concurrency, int) and concurrency > 1) else None
        self._order: Literal["preserved", "free"] = order

    async def __call__(self, input: Any) -> Any:
        # Modern awaiting semantics: await any awaitable results
        # Handle Stream (AsyncIterator)
        if isinstance(input, AsyncIterator):
            if self._concurrency and self._order == "free":
                return self._process_stream_concurrent_free(input)
            return self._process_stream(input)
        
        # Handle Batch (List)
        elif isinstance(input, list):
            # concurrent list mapping with optional order preservation (always preserved here)
            if self._concurrency:
                sem = asyncio.Semaphore(self._concurrency)
                
                async def run_one(idx_item: tuple[int, Any]):
                    idx, item = idx_item
                    async with sem:
                        res = self.fn(item)
                        if inspect.isawaitable(res):
                            res = await res
                        return idx, res
                tasks = [asyncio.create_task(run_one((i, it))) for i, it in enumerate(input)]
                results = [None] * len(tasks)
                for t in asyncio.as_completed(tasks):
                    idx, val = await t
                    results[idx] = val
                return results
            else:
                result = []
                for item in input:
                    res = self.fn(item)
                    if inspect.isawaitable(res):
                        res = await res
                    result.append(res)
                return result
            
        # Handle Scalar
        else:
            res = self.fn(input)
            if inspect.isawaitable(res):
                res = await res
            return res

    async def _process_stream(self, input: AsyncIterator):
        async for item in input:
            res = self.fn(item)
            if inspect.isawaitable(res):
                res = await res
            yield res

    async def _process_stream_concurrent_free(self, input: AsyncIterator):
        # Producer-consumer with worker pool; emits outputs as soon as ready (order-free)
        assert self._concurrency is not None
        in_q: asyncio.Queue[Any] = asyncio.Queue(maxsize=self._concurrency * 2)
        out_q: asyncio.Queue[Any] = asyncio.Queue(maxsize=self._concurrency * 4)
        SENTINEL = object()

        async def producer():
            async for item in input:
                await in_q.put(item)
            # signal workers to stop
            for _ in range(self._concurrency):
                await in_q.put(SENTINEL)

        async def worker():
            while True:
                item = await in_q.get()
                if item is SENTINEL:
                    # propagate sentinel for other workers if taken prematurely not needed due to count
                    break
                res = self.fn(item)
                if inspect.isawaitable(res):
                    res = await res
                await out_q.put(res)

        prod_task = asyncio.create_task(producer())
        workers = [asyncio.create_task(worker()) for _ in range(self._concurrency)]

        active_workers = self._concurrency
        while True:
            if active_workers == 0 and out_q.empty():
                break
            try:
                item = await asyncio.wait_for(out_q.get(), timeout=0.1)
                yield item
            except asyncio.TimeoutError:
                # check worker status
                done, pending = await asyncio.wait(workers, timeout=0, return_when=asyncio.FIRST_COMPLETED)
                if done:
                    active_workers -= len(done)
                    # remove finished from list
                    workers = list(pending)
                # continue loop until all drained
                continue
        await prod_task

class Filter(OperatorMixin):
    """
    A Boson that selectively allows particles to pass (Tunneling).
    """
    def __init__(self, predicate: Callable[[Any], bool | Awaitable[bool]]):
        self.predicate = predicate
        self.name = f"Filter({predicate.__name__})"

    async def __call__(self, input: Any) -> Any:
        if isinstance(input, AsyncIterator):
            return self._process_stream(input)
            
        elif isinstance(input, list):
            result = []
            for item in input:
                keep = self.predicate(item)
                if inspect.isawaitable(keep):
                    keep = await keep
                if keep:
                    result.append(item)
            return result
            
        else:
            keep = self.predicate(input)
            if inspect.isawaitable(keep):
                keep = await keep
            return input if keep else None

    async def _process_stream(self, input: AsyncIterator):
        async for item in input:
            keep = self.predicate(item)
            if inspect.isawaitable(keep):
                keep = await keep
            if keep:
                yield item

class Batch(OperatorMixin):
    """
    A Boson that condenses a stream of particles into a single heavy particle (Batch).
    """
    def __init__(self, size: int):
        self.size = size
        self.name = f"Batch({size})"

    async def __call__(self, input: Any) -> AsyncIterator[list[Any]]:
        if isinstance(input, AsyncIterator):
            async for batch in self._process_stream(input):
                yield batch
        else:
            yield [input]

    async def _process_stream(self, input: AsyncIterator):
        buffer = []
        async for item in input:
            buffer.append(item)
            if len(buffer) >= self.size:
                yield buffer
                buffer = []
        if buffer:
            yield buffer
