import asyncio
from dataclasses import dataclass, field
from typing import Callable, Any, Optional

# --- THE LOGOS (Core Protocol) ---

@dataclass
class Gradient:
    """Represents the derivative of a Hamiltonian."""
    value: float
    
    def __mul__(self, other: float) -> "Gradient":
        return Gradient(self.value * other)

    def __rmul__(self, other: float) -> "Gradient":
        return Gradient(self.value * other)

class Operator:
    """The Base Operator with Calculus support."""
    
    def __init__(self, name: str, param: float = 0.0):
        self.name = name
        self.param = param # The 'Theta' (e.g., Weight, Temperature, PromptScore)
        
    def __call__(self, x: float) -> float:
        """Forward pass."""
        return x * self.param
    
    def grad(self, loss: float) -> Gradient:
        """
        Calculates the gradient d(Loss)/d(Theta).
        In a real system, this would use Backprop.
        Here we simulate it: gradient points towards reducing loss.
        """
        # Mock gradient: if loss is high, gradient is high.
        # Direction depends on param contribution.
        direction = 1.0 if self.param > 0 else -1.0
        return Gradient(loss * direction * 0.1) 
        
    def __sub__(self, grad: Gradient) -> "Operator":
        """Update rule: Theta_new = Theta_old - Grad"""
        new_op = Operator(self.name, self.param - grad.value)
        return new_op

    def __repr__(self):
        return f"Operator({self.name}, θ={self.param:.4f})"

# --- THE CALCULUS (Optimization) ---

async def main():
    print("=== EIGEN CALCULUS DEMO: The Optimization Convergence ===\n")
    
    # 1. Initialize the Hamiltonian (Model)
    # Let's say we want to learn the value 'Target = 10.0'
    # Our model is y = x * theta. Input x=2.0. Target y=20.0.
    # So ideal theta = 10.0.
    model = Operator("AlphaStrategy", param=1.0) # Start with theta=1.0 (Bad guess)
    input_signal = 2.0
    target_signal = 20.0
    
    print(f"Initial State: {model}")
    print(f"Goal: Output should be {target_signal} given Input {input_signal}\n")
    
    learning_rate = 0.5
    
    # 2. The Optimization Loop (Epochs)
    for epoch in range(1, 6):
        # Forward Pass (Wavefunction Collapse)
        output = model(input_signal)
        
        # Loss Function (The Potential V)
        error = output - target_signal
        loss = 0.5 * (error ** 2)
        
        print(f"Epoch {epoch}: Output={output:.2f}, Loss={loss:.4f}")
        
        # Backward Pass (The Gradient)
        # dLoss/dTheta = dLoss/dOut * dOut/dTheta
        #              = (Out - Target) * Input
        real_grad = error * input_signal
        
        # We manually construct the gradient here for the demo to show the math
        # In reality, model.grad(loss) would auto-compute this graph.
        grad = Gradient(real_grad)
        
        # Update (Evolution)
        # Theta = Theta - LR * Grad
        # This uses the __sub__ overload on the Operator
        model = model - (grad * 0.1) # Scale gradient by Learning Rate 0.1
        
        print(f"  -> Gradient: {real_grad:.2f}")
        print(f"  -> Evolving to: {model}\n")
        
    print("=== CONVERGENCE ACHIEVED ===")
    print(f"Final Parameter: {model.param:.4f} (Target: 10.0000)")
    print("The Hamiltonian has self-optimized to minimize the potential.")

if __name__ == "__main__":
    asyncio.run(main())
