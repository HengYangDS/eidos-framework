from ..gauge.symmetry import OperatorMixin
from ..gauge.field import Field, activate_field
from typing import Any
from collections.abc import AsyncIterator
import asyncio

class Hamiltonian(OperatorMixin):
    """
    Hamiltonian Dynamics: The Engine that drives the system evolution.
    """
    def __init__(self, steps: list[OperatorMixin]):
        self.steps = []
        for step in steps:
            if isinstance(step, Hamiltonian):
                self.steps.extend(step.steps)
            else:
                self.steps.append(step)
    
    async def __call__(self, input: Any) -> Any:
        result = input
        for step in self.steps:
            result = await step(result)
        return result
    
    def __repr__(self):
        return " >> ".join([str(s) for s in self.steps])

class Choice(OperatorMixin):
    """
    Fallback/Choice: try left; on exception or None, try right.
    """
    def __init__(self, left: OperatorMixin, right: OperatorMixin):
        self.left = left
        self.right = right

    async def __call__(self, input: Any) -> Any:
        try:
            result = await self.left(input)
            # If result is an async iterator or truthy value, use it
            if result is None:
                return await self.right(input)
            return result
        except Exception:
            return await self.right(input)

class Ensemble(OperatorMixin):
    """
    Parallel/Ensemble: run left and right concurrently and return [left_result, right_result].
    If input is an AsyncIterator, it is teed to feed both operators safely.
    """
    def __init__(self, left: OperatorMixin, right: OperatorMixin):
        self.left = left
        self.right = right

    async def __call__(self, input: Any) -> list[Any]:
        if isinstance(input, AsyncIterator):
            a, b = _async_tee(input, 2)
            async with asyncio.TaskGroup() as tg:  # structured concurrency (3.11+)
                t1 = tg.create_task(self.left(a))
                t2 = tg.create_task(self.right(b))
            return [t1.result(), t2.result()]
        else:
            async with asyncio.TaskGroup() as tg:  # structured concurrency (3.11+)
                t1 = tg.create_task(self.left(input))
                t2 = tg.create_task(self.right(input))
            return [t1.result(), t2.result()]

def _async_tee(source: AsyncIterator, n: int = 2) -> tuple[AsyncIterator, ...]:
    """
    Tee an async iterator into n independent async iterators.
    Implementation: one producer fan-out into n queues; each consumer yields from its queue.
    """
    queues = [asyncio.Queue() for _ in range(n)]
    SENTINEL = object()

    async def producer():
        try:
            async for item in source:
                for q in queues:
                    await q.put(item)
        finally:
            for q in queues:
                await q.put(SENTINEL)

    # Start background producer
    asyncio.create_task(producer())

    async def make_reader(q: asyncio.Queue):
        while True:
            item = await q.get()
            if item is SENTINEL:
                break
            yield item

    return tuple(make_reader(q) for q in queues)

class Interference(OperatorMixin):
    """
    Constructive/Destructive Interference (Summation).
    """
    def __init__(self, operators: list[OperatorMixin]):
        self.operators = operators
        
    async def __call__(self, input: Any) -> Any:
        # Naive constructive interference (summation)
        results = [await op(input) for op in self.operators]
        # Assume results are summable (numbers, tensors)
        total = results[0]
        for r in results[1:]:
            total = total + r
        return total

class QuantumField(Field):
    def flow(self, left: Any, right: Any) -> Any:
        return Hamiltonian([left, right])

    def choice(self, left: Any, right: Any) -> Any:
        return Choice(left, right)

    def ensemble(self, left: Any, right: Any) -> Any:
        return Ensemble(left, right)
        
    def interference(self, left: Any, right: Any) -> Any:
        # If left is already Interference, append right
        ops = []
        if isinstance(left, Interference):
            ops.extend(left.operators)
        else:
            ops.append(left)
            
        if isinstance(right, Interference):
            ops.extend(right.operators)
        else:
            ops.append(right)
            
        return Interference(ops)
