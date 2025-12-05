from typing import Any, Callable
import pickle

try:
    import cloudpickle
except ImportError:
    cloudpickle = None

class FunctionSerializer:
    """
    Serializes functions (UDFs) for distributed or cross-process execution.
    """
    @staticmethod
    def serialize(fn: Callable) -> bytes:
        if cloudpickle:
            return cloudpickle.dumps(fn)
        return pickle.dumps(fn)

    @staticmethod
    def deserialize(data: bytes) -> Callable:
        if cloudpickle:
            return cloudpickle.loads(data)
        return pickle.loads(data)
