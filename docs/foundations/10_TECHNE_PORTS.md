# Book X: TECHNE - The Ports (Boundaries)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "The boundary of a system is a holographic screen. The complexity of the
> interior is encoded on the surface."

## 10.1 The Holographic Boundary

In Eigen, a **Port** is not just a function signature; it is a **Holographic
Boundary**.
According to the **Holographic Principle** in physics, the information contained
in a volume of space can be represented by a theory on the boundary of that
space.

Similarly, the complex business logic (Hamiltonian) inside a Service is
projected onto its Interface (Port).

### 10.1.1 The Event Horizon
The Port acts as an **Event Horizon**.
*   **Inbound (Ingress)**: Information falls in from the vacuum. Once inside, it
    obeys the system's Hamiltonian.
*   **Outbound (Egress)**: Information radiates out (Hawking Radiation).

$$ S_{boundary} \propto A $$
The complexity of the API ($S$) should be proportional to the surface area
($A$), not the internal volume. Keep interfaces minimal.

## 10.2 Port Algebra (Superposition)

A unique feature of Eigen is **Port Superposition**.
Just as an electron can be in a superposition of spin states, an Eigen Service
can expose multiple protocols simultaneously from a single definition.

$$ |Port\rangle = \alpha |HTTP\rangle + \beta |gRPC\rangle + \gamma |CLI\rangle
$$

```python
@atom
def ProcessPayment(amount: float, currency: str):
    ...

# The Superposition
App = ProcessPayment @ (FastAPI + Click + GrpcServer)

```

This is **Algebraic Correspondence** (Axiom IV) applied to infrastructure. You
sum the protocols.

## 10.3 Impedance Matching

When a Fermion (Data) crosses the Event Horizon, it encounters **Impedance**.
*   **Internal Impedance ($Z_{in}$)**: Python Objects (Pydantic).
*   **External Impedance ($Z_{out}$)**: JSON, Protobuf, Bytes.

If $Z_{in} \neq Z_{out}$, reflection occurs (Serialization Errors, Latency).
**Impedance Matching** is the art of designing Ports such that transmission is
lossless.

### 10.3.1 The Adapter Pattern (Transformers)
Eigen automatically generates **Transformers** (Impedance Matchers) based on
type hints.
*   `str` $\leftrightarrow$ `JSON String`
*   `datetime` $\leftrightarrow$ ISO8601
*   `Stream` $\leftrightarrow$ Server-Sent Events (SSE)

## 10.4 Standard Port Types

### 10.4.1 The HTTP Port (RestBoson)
Projects the logic onto the RESTful manifold.
*   `Get` $\to$ `GET`
*   `Create` $\to$ `POST`
*   `Update` $\to$ `PUT`
*   `Delete` $\to$ `DELETE`

### 10.4.2 The CLI Port (ShellBoson)
Projects the logic onto the Command Line.
*   Arguments $\to$ Flags (`--amount`)
*   Docstring $\to$ Help Text

### 10.4.3 The MCP Port (AgentBoson)
Projects the logic onto the **Model Context Protocol**.
This allows LLMs (Claude, GPT) to "call" your code natively.
*   **Function Calling**: The Port generates the JSON Schema for the LLM.
*   **Execution**: The Port handles the tool execution loop.

```python

# This single line makes your logic available to Claude Desktop
Serve(MyLogic, protocol=MCP)

```

## 10.5 Entangled Serving

In a distributed system, Ports can be **Entangled**.
A request hitting Port A on Node 1 might instantly collapse the wavefunction on
Node 2 via a hidden channel (RPC).

### 10.5.1 The Gateway Pattern
A Gateway is simply a Port that does not contain logic itself but forwards the
Fermion to another Port.

```python
Gateway = Port(
    route="/pay",
    target=PaymentService.port
)

```

## 10.6 Engineering Best Practices

1.  **Strict Schemas**: Define the boundary conditions precisely (Pydantic). A
    fuzzy boundary leads to vacuum decay (Runtime Errors).
2.  **Version as Dimension**: Treat API Versioning as a temporal dimension. `v1`
    and `v2` are parallel universes.
3.  **Idempotency**: Ensure that re-crossing the horizon doesn't duplicate the
    mass (Side Effects).

## 10.7 Holographic Projection (UI)

The concept of **Holography** extends to the User Interface (Book XXV).
The UI is simply a 2D projection of the N-dimensional Logic.

*   **Command** $\to$ Button.
*   **Stream** $\to$ List View.
*   **State** $\to$ Label.

```python

# Auto-generating a React UI from the Python Logic
@hologram
class Dashboard(Hamiltonian):
    ...

```

## 10.8 Black Hole Information Paradox (Security)

In Physics, the paradox asks if information is lost when it enters a black hole.
In Software, the paradox is **Security**.
*   If we allow external data in (Information), can we prevent internal secrets
    from leaking out (Hawking Radiation)?
*   **Solution**: The **Firewall** (Horizon). We place a `Filter` boson at the
    event horizon that incinerates unauthorized particles.

---
**Eigen Cosmology** | [Previous: Book IX](09_TECHNE_BOSONS.md) | [Index](../00_INDEX.md) | [Next: Book XI](11_MATHEMATICAL_DERIVATIONS.md) | *© 2025 The Eigen High Council*
