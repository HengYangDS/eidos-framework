# Book V: MATRIX - The Hamiltonian Dynamics

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "The Hamiltonian represents the total energy of the system and governs its
> time evolution."

## 5.1 The Matrix Engine (Fa)

The **Matrix** (Fa) layer is the runtime environment of Eigen. While Logos
defines the laws, Matrix enforces them. It is the **JIT Compiler** and **Event
Loop**.

The core object in Matrix is the `Hamiltonian`. It is a compiled executable
graph of Operators.

## 5.2 The Hamiltonian Class

The `Hamiltonian` acts as the base class for all composite operators. It
implements the specific logic for the entire "Periodic Table of Operators"
defined in Book XVI.

```python
import asyncio
import random
from typing import Generic, TypeVar, Any, Callable
from eigen.logos import Operator, Symmetry, Particle
from eigen.techne import Fermion

I = TypeVar("I")
O = TypeVar("O")

class Hamiltonian[I, O]:
    """
    The Concrete Implementation of the Algebra of Actions.
    """
    
    # --- Fundamental Forces (Flow & Choice) ---

    def __rshift__(self, other: "Operator") -> "Flow":
        """Flow (>>): Causal Sequence."""
        return Flow(self, other)

    def __or__(self, other: "Operator") -> "Choice":
        """Superposition (|): Alternative Path / Fallback."""
        return Choice(self, other)
        
    def __and__(self, other: "Operator") -> "Ensemble":
        """Entanglement (&): Parallel Execution."""
        return Ensemble(self, other)

    # --- Arithmetic Ring (Interference) ---
    
    def __add__(self, other: "Operator") -> "Interference":
        """Interference (+): Constructive Sum / Merge."""
        return Interference(self, other)
        
    def __sub__(self, other: "Operator") -> "Constraint":
        """Constraint (-): Exclusion / Exception Suppression."""
        return Constraint(self, other)
        
    def __mul__(self, factor: int) -> "Amplifier":
        """Amplification (*): Repetition / Scaling."""
        return Amplifier(self, factor)

    def __truediv__(self, divisor: int) -> "Decimator":
        """Decimation (/): Sampling / Sharding."""
        return Decimator(self, divisor)

    def __floordiv__(self, batch_size: int) -> "Quantizer":
        """Quantization (//): Batching."""
        return Quantizer(self, batch_size)
        
    def __pow__(self, depth: int) -> "Fractal":
        """Recursion (**): Fractal Depth."""
        return Fractal(self, depth)

    def __matmul__(self, sink: "Operator") -> "Measurement":
        """Measurement (@): Projection / Logging."""
        return Measurement(self, sink)

    def __lshift__(self, feedback: "Operator") -> "Feedback":
        """Feedback (<<): Cybernetic Loop."""
        return Feedback(self, feedback)

    def __xor__(self, interrupt: "Operator") -> "Preemption":
        """Preemption (^): Interrupt / Exclusive Switch."""
        return Preemption(self, interrupt)
        
    def __invert__(self) -> "Antimatter":
        """Antimatter (~): Undo / Compensating Transaction."""
        return Antimatter(self)
        
    def __neg__(self) -> "TimeReversal":
        """Time Reversal (-x): Inverse Operation."""
        return TimeReversal(self)

    def __mod__(self, config: dict) -> "FieldBinding":
        """Gauge Fixing (%): Inject Context."""
        return FieldBinding(self, config)

```

## 5.3 The Dynamics Implementation

Here we define the runtime mechanics of each operator.

### 5.3.1 Flow (>>) & Choice (|)
See previous sections for `Flow` and `Choice` logic.

### 5.3.2 Interference (Merge `+`)

```python
class Interference[I, O]:
    def __init__(self, op1: Operator, op2: Operator):
        self.op1 = op1
        self.op2 = op2
        
    async def __call__(self, x: I) -> O:

        # Constructive Interference: Run both and sum the energies
        r1, r2 = await asyncio.gather(self.op1(x), self.op2(x))

        # Polymorphic addition (Str concat, Int sum, Dict merge)
        return r1 + r2

```

### 5.3.3 Constraint (Filter `-`)

```python
class Constraint[I, O]:
    def __init__(self, op: Operator, constraint: Any):
        self.op = op
        self.constraint = constraint # Can be an Operator or Exception type
        
    async def __call__(self, x: I) -> O:
        try:
            return await self.op(x)
        except Exception as e:

            # If the error matches the constraint, suppress it (Destructive Interference)
            if isinstance(self.constraint, type) and isinstance(e, self.constraint):
                return None # Annihilation
            raise e

```

### 5.3.4 Amplification (Loop `*`)

```python
class Amplifier[I, O]:
    def __init__(self, op: Operator, factor: int):
        self.op = op
        self.factor = factor
        
    async def __call__(self, x: I) -> list[O]:

        # Run N times (Parallel or Sequential depends on JIT optimization)
        tasks = [self.op(x) for _ in range(self.factor)]
        return await asyncio.gather(*tasks)

```

### 5.3.5 Decimation (Sample `/`)

```python
class Decimator[I, O]:
    def __init__(self, op: Operator, rate: int):
        self.op = op
        self.rate = rate # 1/N
        
    async def __call__(self, x: I) -> O:

        # Probabilistic execution
        if random.randint(1, self.rate) == 1:
            return await self.op(x)
        raise ParticleDecimated()

```

### 5.3.6 Quantization (Batch `//`)

```python
class Quantizer[I, O]:
    def __init__(self, op: Operator, batch_size: int):
        self.op = op
        self.batch_size = batch_size
        self.buffer = []
        
    async def __call__(self, x: I) -> list[O]:
        self.buffer.append(x)
        if len(self.buffer) >= self.batch_size:
            batch = self.buffer[:]
            self.buffer.clear()
            return await self.op(batch) # Process batch
        raise AwaitingCriticalMass()

```

### 5.3.7 Measurement (Observe `@`)

```python
class Measurement[I, O]:
    def __init__(self, op: Operator, sink: Operator):
        self.op = op
        self.sink = sink
        
    async def __call__(self, x: I) -> O:
        result = await self.op(x)

        # Side-channel observation (Fire and forget or await)
        asyncio.create_task(self.sink(result))
        return result # Pass-through

```

### 5.3.8 Antimatter (Undo `~`)

```python
class Antimatter[I, O]:
    def __init__(self, op: Operator):
        self.op = op
        
    async def __call__(self, x: I) -> O:

        # The Logic of Reversal

        # In a transaction context, this registers a rollback
        tx_context = current_transaction.get()
        if tx_context:
            tx_context.register_undo(self.op, x)
        return None

```

## 5.4 The Event Loop

Matrix relies on the `asyncio` loop to schedule these interacting particles. The
JIT compiler optimizes the graph before execution (e.g., fusing `Amplifier` and
`Ensemble`).

### Sequence Diagram: The Life of a Packet

```mermaid
sequenceDiagram
    participant User
    participant Loop as EventLoop
    participant H as Hamiltonian
    participant Op1
    participant Op2
    
    User->>Loop: run(H, input)
    Loop->>H: __call__(input)
    
    rect rgb(20, 20, 40)
        note right of H: H = Op1 >> (Op2 | Op3)
        H->>Op1: await call(input)
        Op1-->>H: result1
        
        H->>Op2: await call(result1)
        alt Op2 Fails
            Op2-->>H: Raise Error
            H->>Op3: Tunneling (Choice)
            Op3-->>H: result2
        else Op2 Succeeds
            Op2-->>H: result2
        end
    end
    
    H-->>Loop: result2
    Loop-->>User: result2

```

## 5.5 The Heisenberg Picture vs Schrödinger Picture

In Eigen, we can view the system execution from two perspectives:

### 5.5.1 The Schrödinger Picture (State Evolution)
Here, the Operators ($\hat{H}$) are static, and the Data States ($|\psi\rangle$)
evolve over time.
$$ i\hbar \frac{\partial}{\partial t} |\psi(t)\rangle = \hat{H} |\psi(t)\rangle
$$
*   **Implementation**: The standard `Flow` where `data` is passed from function
    to function. The functions don't change; the data does.
*   **Use Case**: Most stateless microservices.

### 5.5.2 The Heisenberg Picture (Operator Evolution)
Here, the States ($|\psi\rangle$) are static (the Initial Conditions), and the
Operators ($\hat{A}(t)$) evolve over time.
$$ \frac{d}{dt}\hat{A}(t) = \frac{i}{\hbar} [\hat{H}, \hat{A}(t)] +
\frac{\partial \hat{A}}{\partial t} $$
*   **Implementation**: **Self-Modifying Code** or **Meta-Programming**. The
    `Optimization` loop where the weights of the Neural Network (Operator)
    change over time (`t` = Epochs).
*   **Use Case**: Machine Learning, Biogenesis (Evolutionary Algorithms).

The **Matrix Layer** supports both. By default, it runs in the Schrödinger
picture. When `eigen.calculus` or `eigen.bio` is engaged, it switches to the
Heisenberg picture to evolve the operators themselves.

---
**Eigen Cosmology** | [Previous: Book IV](04_LOGOS_INVARIANCE.md) | [Index](../00_INDEX.md) | [Next: Book VI](06_MATRIX_PATH_INTEGRAL.md) | *© 2025 The Eigen High Council*