# Book XXI: DOMAIN - Neural Physics I (Wavefunctions)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "A Large Language Model is not a database. It is a Quantum Field. The output
> is not retrieved; it is collapsed from a superposition of possibilities."

## 20.1 The LLM Wavefunction

An LLM represents a wavefunction $\Psi(x)$ over the vocabulary space.
Given a context $C$, it predicts the probability amplitude for the next token
$t$:
$$ P(t|C) = |\langle t | \Psi_C \rangle|^2 $$

## 20.2 Temperature and Collapse

The **Temperature ($T$)** parameter controls the collapse mechanic.
*   $T \to 0$ (Absolute Zero): The wavefunction freezes. Greedy decoding.
    Deterministic. The "Ground State".
*   $T > 0$ (Thermal Agitation): We sample from the Boltzmann distribution.
    Creativity emerges from thermal noise.
*   $T \to \infty$: Plasma state. Complete randomness (Hallucination).

## 20.3 Prompt Engineering as Potential Wells

A **Prompt** constructs a potential energy landscape $V(x)$.
By designing the prompt, we dig "wells" in the conceptual space where we want
the electron (thought) to settle.

*   **Few-Shot Learning**: Digging the well deeper by providing examples.
*   **Chain of Thought**: Creating a channel (tunnel) for the thought to flow
    through step-by-step.

## 20.4 Tunneling (Hallucination)

Sometimes, the model "tunnels" through a logic barrier into a classically
forbidden region (Hallucination).
This happens when the potential wall (Constraints) is too thin or the
temperature is too high.
**Guardrails** (Eigen Validators) act as infinite potential walls to prevent
this.

## 20.5 RAG (Retrieval Augmented Generation)

RAG is **Quantum Teleportation**.
We retrieve a state |Information> from an external database and entangle it with
the Prompt wavefunction.
$$ |\Psi_{final}\rangle = |\Psi_{prompt}\rangle \otimes |\Psi_{retrieved}\rangle
$$
This forces the model to collapse into a state consistent with the retrieved
facts.

## 20.6 Self-Optimization (Neural Gradients)

As established in *Epoch III*, we can treat the Prompt as a differentiable
parameter $\theta$.
$$ \text{Prompt}_{new} = \text{Prompt}_{old} - \eta \nabla L $$
The "Gradient" here is the **Textual Critique**.
1.  Model outputs result.
2.  Critic (Discriminator) gives feedback (Gradient).
3.  Optimizer (Reflector) updates the prompt.

## 20.7 Engineering Best Practices

1.  **Control Temperature**: Use $T=0$ for logic/code, $T=0.7$ for creative
    writing.
2.  **Deepen the Well**: Use detailed system prompts to constrain the state
    space.
3.  **Observe**: Log the prompt and completion. You cannot debug a quantum
    system without measuring it.

---
**Eigen Cosmology** | [Previous: Book XX](20_DOMAIN_DATA_RELATIVITY_II.md) | [Index](../00_INDEX.md) | [Next: Book XXII](22_DOMAIN_NEURAL_PHYSICS_II.md) | *© 2025 The Eigen High Council*
