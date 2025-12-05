# Book XXV: HOLOGRAPHY - The Holographic Principle (UI)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "The information of a volume of space is encoded on its boundary." — Gerard 't
> Hooft

In **Eigen**, the **User Interface (UI)** is not a separate codebase. It is a
**Hologram** projected from the **Type Signatures** of the Operators (The Bulk).

## 24.1 The Bulk-Boundary Correspondence (AdS/CFT)

- **The Bulk (AdS)**: The Python Backend code. The complex, high-dimensional
  logic (`Operator[I, O]`).
- **The Boundary (CFT)**: The Frontend UI (React/Streamlit). A lower-dimensional
  projection of the Bulk.

**Theorem**: Any change in the Bulk *automatically* changes the Boundary.

## 24.2 The Algebra of Views

Just as we have an Algebra of Actions for logic, we have an **Algebra of Views**
for the UI.
UI Components are just Operators that emit VDOM (Virtual DOM) particles.

$$ V = \text{Render}(State) $$

### 24.2.1 Vertical Composition (Stack `+`)
The Addition operator stacks views vertically (Column).
$$ V_{total} = V_{header} + V_{body} + V_{footer} $$

```python

# A Page is a sum of its parts
Dashboard = Header() + Chart() + Footer()

```

### 24.2.2 Horizontal Composition (Grid `&`)
The Entanglement operator places views side-by-side (Row/Grid).
$$ V_{row} = V_{left} \otimes V_{right} $$

```python

# Side-by-side charts
Comparison = Chart(A) & Chart(B)

```

### 24.2.3 Conditional Rendering (Switch `|`)
The Choice operator renders the first view that accepts the state, or falls
back.
It implements **Tabs** or **Error Boundaries**.

```python

# If User is Admin, show AdminPanel, else show UserPanel
Panel = (Guard(IsAdmin) >> AdminPanel) | UserPanel

```

### 24.2.4 Context Injection (Theme `%`)
The Field operator injects styling or configuration context.
$$ V_{styled} = V_{raw} \% \text{Theme} $$

```python

# Apply Dark Mode
App = RawApp % {"theme": "dark", "accent": "blue"}

```

## 24.3 The Calculus of Experience (Minimizing Action)

Beyond algebra, we apply **The Calculus** (Book XVI) to User Interaction.
We treat the user's journey as a path through the state manifold.

### 24.3.1 The Principle of Least Action ($S$)
The goal of UI/UX design is to minimize the **Interaction Action** ($S$).

$$ S = \int_{t_{start}}^{t_{end}} (L_{cognitive} + L_{motor}) dt $$

*   $L_{cognitive}$: Mental load (reading, deciding).
*   $L_{motor}$: Physical load (moving mouse, typing).

An optimal UI is a **Geodesic** (shortest path) in this action space.

### 24.3.2 Interaction Gradients ($\nabla U$)
We can define a "User Potential" $U(x)$ (e.g., frustration or distance to goal).
The user naturally flows down the gradient:
$$ \vec{v}_{user} \propto -\nabla U $$

*   **Fitts's Law** is a gradient descent manifestation: users move faster to
    larger/closer targets.
*   **Eigen's Role**: By analyzing the `Hamiltonian` graph topology, we can
    optimize the UI projection to minimize $S$ automatically (e.g., placing
    frequently used buttons closer to the cursor context).

## 24.4 The `@hologram` Decorator

We use a decorator to attach "Visual Spin" to our particles.

```python
from eigen.techne.quanta import hologram, Widget

@hologram(
    temperature=Widget.Slider(0.0, 1.0),
    model=Widget.Dropdown(["gpt-4", "claude-3"])
)
class ChatAtom(Operator):
    def __init__(self, temperature: float, model: str):
        ...

```

## 24.5 The Holographic Projector (UIPort)

The `UIPort` scans the `Hamiltonian` graph and renders the UI.

```python

# define the physics
physics = Source() >> RAG() >> ChatAtom()

# project the hologram
UIPort(physics).render() 

```

### 24.5.1 Automatic Rendering Rules
- `int` / `float` -> Slider or Input Box.
- `bool` -> Toggle Switch.
- `Enum` -> Dropdown.
- `Stream[str]` -> Chat Terminal (Streaming).
- `DataFrame` -> Interactive Table (AgGrid).
- `Image` -> Canvas.

## 24.6 Event Horizon (Interaction)

When a user interacts with the UI (Boundary), they send a **Gravitational Wave**
into the Bulk.
- Slider moved -> Update `Field` context.
- Button clicked -> Trigger `Flow`.

This allows "Time Travel" debugging: we can record the UI events and replay them
in the backend to reproduce bugs.

## 24.7 Practice: UI Engineering

1.  **No HTML/CSS**: Never write layout code manually. Use algebra (`+`, `&`).
2.  **State is Truth**: The UI is a pure function of the Hamiltonian state. Do
    not store state in the DOM.
3.  **Zero Latency**: The UI connects to the Matrix via WebSockets. Updates are
    pushed as `Delta` particles.

## 24.8 Renormalized Views (Semantic Zoom)

As we "zoom out" from a single Operator to a whole System, the UI must
**Renormalize** (Coarse Grain).
Showing every log line at the cluster level is information overload (High
Entropy).

Eigen applies **Semantic Zoom**:
1.  **Micro Scale (Atom)**: Show full logs, inputs, outputs (Inspector).
2.  **Meso Scale (Molecule)**: Show dependency graph and data flow (Flowchart).
3.  **Macro Scale (Bulk)**: Show health metrics (Traffic Lights) and aggregated
    stats (Histograms).

The `UIPort` automatically applies the **Renormalization Group Transformation**
($\mathcal{R}$) to the view based on the user's zoom level.

$$ View_{macro} = \mathcal{R}(View_{micro}) $$

> "The screen is just a 2D slice of a high-dimensional computation."

---
**Eigen Cosmology** | [Previous: Book XXIV](24_THERMODYNAMICS_ECONOMY.md) | [Index](../00_INDEX.md) | [Next: Book XXVI](26_ENTANGLEMENT_DISTRIBUTED.md) | *© 2025 The Eigen High Council*
