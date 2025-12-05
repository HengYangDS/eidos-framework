import asyncio
import unittest

from pathlib import Path
import sys

# Ensure src on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from eigen.runtime import activate
from eigen.gauge.symmetry import OperatorMixin


class Const(OperatorMixin):
    def __init__(self, value):
        self.value = value

    async def __call__(self, _):
        return self.value


class Raise(OperatorMixin):
    async def __call__(self, _):
        raise RuntimeError("boom")


class Identity(OperatorMixin):
    async def __call__(self, x):
        return x


class ToList(OperatorMixin):
    async def __call__(self, it):
        out = []
        async for item in it:
            out.append(item)
        return out


async def agen(items):
    for x in items:
        await asyncio.sleep(0)
        yield x


class TestOperatorAlgebra(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        activate()

    async def test_choice_fallback_on_none(self):
        class NoneOp(OperatorMixin):
            async def __call__(self, _):
                return None

        left = NoneOp()
        right = Const(42)
        combined = left | right
        self.assertEqual(await combined(None), 42)

    async def test_choice_fallback_on_exception(self):
        combined = Raise() | Const(7)
        self.assertEqual(await combined(None), 7)

    async def test_interference_addition(self):
        a = Const(2)
        b = Const(5)
        # Interference via + should sum
        res = await (a + b)(None)
        self.assertEqual(res, 7)

    async def test_ensemble_parallel_and_async_stream_tee(self):
        # Build a stream and pass through two identities in parallel
        stream = agen([1, 2, 3])
        # Left branch collects to list, right branch collects to list
        left = ToList()
        right = ToList()

        # Compose Hamiltonian: (src) & (src) is not directly applicable; use operators on the same input
        # Build a small pipeline that feeds the same async iterator to both operators via &
        pipeline = (left) & (right)
        results = await pipeline(stream)
        left_list, right_list = results
        self.assertEqual(left_list, [1, 2, 3])
        self.assertEqual(right_list, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
