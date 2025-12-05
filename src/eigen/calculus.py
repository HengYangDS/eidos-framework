from .core import Operator, Tensor
from typing import Any, Callable

class Parameter(Tensor):
    """
    A Tensor that accumulates gradients.
    """
    def __init__(self, data: Any):
        super().__init__(data)
        self.grad = None

class Differentiable(Operator):
    """
    An Operator that can be differentiated.
    """
    def parameters(self):
        # Should return list of Parameters
        return []

def d(func_or_tensor: Any) -> Any:
    """
    The Differential Operator (Gradient).
    """
    # Mock gradient
    return []

class SGD:
    """
    Stochastic Gradient Descent.
    """
    def __init__(self, learning_rate: float = 0.01):
        self.lr = learning_rate
        
    def step(self, params: Any, grads: Any):
        pass
