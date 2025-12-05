# Book XXIV: MECHANICS - Economy (Cost)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "There is no free lunch. Every computation consumes energy (Joules) and
> capital (Dollars). The efficient system minimizes the Action of Cost."

## 23.1 The Cost Hamiltonian

In Eigen, we extend the Hamiltonian to include an economic term:
$$ H_{total} = H_{logic} + \lambda H_{cost} $$

*   $H_{logic}$: The business value produced.
*   $H_{cost}$: The resource consumption (CPU, RAM, Tokens).
*   $\lambda$: The Lagrange multiplier (Budget constraint).

## 23.2 The Budget Field (Constraints)

We apply cost constraints via the **Budget Field** (`% Budget`).

```python

# Constraint: Cannot spend more than $0.01 per execution
CheapOp = ExpensiveLLM % Budget(max_cost=0.01)

```

If the Hamiltonian predicts a cost violation, the wavefunction collapses to an
Error or a Fallback (Cheaper Model) *before* execution.

## 23.3 Tokenomics (The New Energy)

In the AI Era, **Tokens** are the fundamental unit of energy.
*   **Prompt Engineering** is thermodynamics: How to extract maximum work
    (Intelligence) from minimum heat (Tokens).
*   **Context Window**: The thermodynamic limit of the system's short-term
    memory.

### 23.3.1 Compression (Entropy Reduction)
To save cost, we must compress the input fermions.
`Summarizer >> LLM` is a standard pattern to lower the energy state of the
prompt.

## 23.4 Cost-Aware Routing (The Gradient)

Eigen supports **Gradient Descent on Cost**.
If we have multiple models (GPT-4, GPT-3.5, Llama 2), we can define a routing
surface.

$$ \vec{v} = -\nabla (\text{Accuracy} / \text{Cost}) $$

The **Router Boson** directs the flow along the path of highest ROI.
*   Simple queries $\to$ Llama (Low Potential).
*   Complex queries $\to$ GPT-4 (High Potential).

```python

# Smart Routing
Answer = (
    (IsSimple >> Llama) |
    (IsComplex >> GPT4)
)

```

## 23.5 Energy Auditing

The system must generate a **Bill of Materials (BOM)** for every execution
trace.
The `@metered` decorator attaches a meter to the operator.

```python
@metered
def generate_image(prompt):
    ...

```

**FinOps** becomes an intrinsic property of the code, not an external
spreadsheet.

## 23.6 The Jevons Paradox

**Warning**: Increasing efficiency (lowering cost) often increases total
consumption.
Making LLMs cheaper will simply make us use them in loop (Agents).
The total system energy tends to grow.

---
**Eigen Cosmology** | [Previous: Book XXIII](23_THERMODYNAMICS_ENTROPY.md) | [Index](../00_INDEX.md) | [Next: Book XXV](25_HOLOGRAPHY_PRINCIPLE.md) | *© 2025 The Eigen High Council*
