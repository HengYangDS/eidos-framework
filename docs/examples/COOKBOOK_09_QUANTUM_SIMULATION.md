# Cookbook IX: Quantum Simulation - The Qubit Operator

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

## 1. Qubits as Fermions

In Eigen, a Qubit is a normalized complex vector (Tensor).

$$ |\psi\rangle = \alpha |0\rangle + \beta |1\rangle $$

We can model this using the `Tensor` fermion.

```python
import numpy as np
from eigen.core import Tensor, Operator

class Qubit(Tensor):
    def __init__(self, alpha=1.0, beta=0.0):
        self.state = np.array([complex(alpha), complex(beta)])
        self.normalize()
        
    def normalize(self):
        norm = np.linalg.norm(self.state)
        self.state /= norm

```

---

## 2. Quantum Gates as Bosons

Quantum Gates are unitary operators acting on the Qubit state.

### 2.1 The Hadamard Gate (Superposition)
Creates a superposition from a basis state.

```python
class Hadamard(Operator):
    """The H Gate: Maps |0> to (|0> + |1>)/sqrt(2)"""
    def __init__(self):
        self.matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        
    async def apply(self, qubit: Qubit) -> Qubit:
        qubit.state = self.matrix @ qubit.state
        return qubit

```

### 2.2 The Pauli-X Gate (NOT)
Flips the bit.

```python
class PauliX(Operator):
    """The X Gate: NOT operation"""
    def __init__(self):
        self.matrix = np.array([[0, 1], [1, 0]])
        
    async def apply(self, qubit: Qubit) -> Qubit:
        qubit.state = self.matrix @ qubit.state
        return qubit

```

---

## 3. Entanglement (CNOT)

Entanglement requires a Multi-Qubit system (Tensor Product).

$$ |\psi_{AB}\rangle = |\psi_A\rangle \otimes |\psi_B\rangle $$

```python
class CNOT(Operator):
    """Controlled-NOT Gate"""
    def __init__(self):

        # 4x4 Matrix for 2 Qubits
        self.matrix = np.array([
            [1,0,0,0],
            [0,1,0,0],
            [0,0,0,1],
            [0,0,1,0]
        ])
        
    async def apply(self, system: MultiQubitSystem) -> MultiQubitSystem:
        system.state = self.matrix @ system.state
        return system

```

---

## 4. Quantum Circuit Pipeline

A Quantum Circuit is just an Eigen Pipeline.

```python

# Bell State Generator: |00> -> (|00> + |11>)/sqrt(2)

# 1. Start with |00>

# 2. Apply H to Qubit 0

# 3. Apply CNOT (Control=0, Target=1)

BellCircuit = (
    Source("|00>") 
    >> Hadamard(target=0) 
    >> CNOT(control=0, target=1)
    >> Measure()
)

```

---

## 5. Grover's Algorithm (Search)

Grover's algorithm provides quadratic speedup for search. In Eigen, it is an
iterative amplitude amplification.

```python
class Oracle(Operator):
    """Marks the target state by flipping phase"""
    def __init__(self, target_state):
        self.target = target_state

class Diffuser(Operator):
    """Inversion about the mean"""
    
GroversAlgorithm = (
    InitSuperposition()
    >> (Oracle(target="|101>") >> Diffuser()) * OptimalIterations
    >> Measure()
)

```

---
**Eigen Cosmology** | [Previous: Cookbook VIII](COOKBOOK_08_BIOINFORMATICS.md) | [Index](../00_INDEX.md) | [Next: Cookbook X](COOKBOOK_10_CHAOS_ENGINEERING.md) | *© 2025 The Eigen High Council*
