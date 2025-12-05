# Cookbook XI: Machine Learning - The Differential Engine

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

## 1. The Operator as a Neuron

In Eigen, a Neuron is simply a parameterized Operator.

$$ y = \sigma(Wx + b) $$

```python
import numpy as np
from eigen.core import Operator, Tensor
from eigen.calculus import Differentiable, Parameter, d

class Neuron(Differentiable):
    def __init__(self, input_dim):

        # Weights and Bias are Parameters (Tracked for Gradients)
        self.W = Parameter(np.random.randn(input_dim))
        self.b = Parameter(np.random.randn(1))
        
    def forward(self, x: Tensor) -> Tensor:
        z = x.dot(self.W) + self.b
        return self.sigmoid(z)
        
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

```

---

## 2. The Layer as a Manifold

A Layer is a `Map` operator that transforms the geometry of the data manifold.

```python
class DenseLayer(Differentiable):
    def __init__(self, in_dim, out_dim):
        self.neurons = [Neuron(in_dim) for _ in range(out_dim)]
        
    async def run(self, x: Tensor) -> Tensor:

        # Parallel execution of neurons (Entanglement)
        outputs = await asyncio.gather(*[n.forward(x) for n in self.neurons])
        return Tensor(outputs)

```

---

## 3. The Network as a Pipeline

A Neural Network is just a `Flow` of layers.

```python

# Define the architecture
Model = (
    DenseLayer(784, 128)  # Input -> Hidden
    >> Relu()             # Activation
    >> DenseLayer(128, 10) # Hidden -> Output
    >> Softmax()          # Probability
)

```

---

## 4. Training (The Optimization Loop)

Training is the process of minimizing the Hamiltonian (Loss) via Gradient
Descent.

$$ \theta_{t+1} = \theta_t - \eta \nabla_\theta H $$

```python
from eigen.calculus import SGD

async def train(dataset, epochs=10):
    optimizer = SGD(learning_rate=0.01)
    
    for epoch in range(epochs):
        total_loss = 0
        
        async for x, y_true in dataset:

            # 1. Forward Pass (Evolution)
            y_pred = await Model.run(x)
            
            # 2. Compute Hamiltonian (Energy/Cost)
            loss = CrossEntropy(y_pred, y_true)
            
            # 3. Backward Pass (Sensitivity Analysis)

            # The 'd()' operator automatically computes gradients

            # for all Parameters involved in the 'loss' calculation.
            grads = d(loss)
            
            # 4. Update Parameters (Force application)
            optimizer.step(Model.parameters(), grads)
            
            total_loss += loss
            
        print(f"Epoch {epoch}: Loss = {total_loss}")

```

---

## 5. Advanced: The Transformer

A Transformer block is composed of `Attention` (Entanglement) and `FeedForward`
(Map).

```python
class SelfAttention(Operator):
    def __init__(self, dim):
        self.W_q = Parameter(np.random.randn(dim, dim))
        self.W_k = Parameter(np.random.randn(dim, dim))
        self.W_v = Parameter(np.random.randn(dim, dim))
        
    async def run(self, x):
        Q = x @ self.W_q
        K = x @ self.W_k
        V = x @ self.W_v
        
        # Scaled Dot-Product Attention
        scores = (Q @ K.T) / np.sqrt(dim)
        attn = softmax(scores)
        return attn @ V

# The Transformer Block
TransformerBlock = (
    (Identity() & SelfAttention(512)) # Residual Connection
    >> Add()
    >> LayerNorm()
    >> (Identity() & FeedForward(512)) # Residual
    >> Add()
    >> LayerNorm()
)

```

---
**Eigen Cosmology** | [Previous: Cookbook X](COOKBOOK_10_CHAOS_ENGINEERING.md) | [Index](../00_INDEX.md) | [Next: Cookbook XII](COOKBOOK_12_CYBERSECURITY.md) | *© 2025 The Eigen High Council*
