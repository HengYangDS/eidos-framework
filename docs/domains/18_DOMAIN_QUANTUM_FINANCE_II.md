# Book XVIII: QUANTUM FINANCE - Strategy (The Wavefunction)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "A strategy is a Hamiltonian that minimizes risk and maximizes return."
> — *The Modern Portfolio Theory*

## 17.1 Alpha as an Operator

An **Alpha Factor** is an Operator that transforms Market Data into a Signal
(Prediction).
$$ \alpha(t) = H_{factor} |\psi_{market}\rangle $$

The signal is usually a vector $[-1, 1]$ representing conviction.
*   -1: Strong Sell
*   0: Neutral (Vacuum)
*   1: Strong Buy

### 17.1.1 Signal Composition (Entanglement)

Single factors are weak (Low SNR). We combine them into a **Strong Interaction**
using Entanglement (`&`).

```python

# Multi-Factor Model

# The Context Field injects specific parameters (Window Size)

Alpha = (
    (SMA(20) % {"name": "fast"}) &
    (RSI(14) % {"name": "mom"}) &
    (Sentiment() % {"source": "news"})
) >> WeightedAvg([0.4, 0.4, 0.2])

```

### 17.1.2 The Alpha Boson

```python
class AlphaBoson(Operator[Bar, float]):
    """Base class for all Alpha Factors."""
    def __init__(self, period: int):
        self.period = period
        self.buffer = deque(maxlen=period)

    async def __call__(self, bar: Bar) -> float:
        self.buffer.append(bar.close)
        if len(self.buffer) < self.period:
            return 0.0 # Warming up
        return self.compute(self.buffer)

```

## 17.2 Risk Management (The Shield)

Risk controls are **Filter Bosons** or **Potential Barriers** that prevent the
portfolio from entering dangerous states.
They act as the **Pauli Exclusion Principle** for money (Preventing infinite
loss).

```python

# Filters
StopLoss = Filter(lambda p: p.drawdown < 0.02)
MaxExposure = Filter(lambda p: p.gross_leverage < 1.5)
KillSwitch = CircuitBreaker(threshold=5)

# The Safe Hamiltonian
SafeStrategy = Alpha >> StopLoss >> MaxExposure >> KillSwitch >> Execution()

```

## 17.3 Backtesting: Closed Timelike Curves

Backtesting involves running the *exact same* Hamiltonian on historical data.
Eigen's **Time Symmetry** (Book XXVIII) allows us to inject a `VirtualClock`
field.

The strategy code **does not change**.
$$ H_{live} \equiv H_{backtest} $$

```python

# The Strategy is Time-Invariant (Gauge Symmetry)
Strategy = Source() >> Alpha >> Exec

# Live Mode

# RealTimeClock sleeps for real intervals.
Live = Strategy % RealTimeClock()

# Backtest Mode

# HistoricalClock warps time to replay history instantly.

# It injects the 'now' timestamp into the Field context.
Backtest = Strategy % HistoricalClock("2023-01-01", speed=1000)

```

### The Matching Engine Simulator

In Backtest mode, `Execution()` cannot hit the Exchange. It must hit a
Simulator.
This is achieved via **Isotope Injection** (Dependency Injection).

```python
if env == "LIVE":
    Execution = FixProtocolExec()
else:
    Execution = PaperTradingExec() # Simulates slippage and latency

```

## 17.4 Portfolio Optimization (The Calculus)

A Portfolio is a Tensor $W_{ij}$ (Weights of asset $i$ in regime $j$).
Optimization is the process of finding the Hamiltonian parameters that minimize
the **Loss Function** (Risk/Volatility) or maximize the **Objective Function**
(Sharpe Ratio).

In Eigen's **Calculus** (Book XVI), we use the **Gradient Operator** ($\nabla$)
to perform this optimization automatically.

$$ \theta_{t+1} = \theta_t - \eta \nabla_{\theta} \mathcal{L}(\text{Strategy})
$$

```python
class PortfolioOptimizer(Operator[Signal, Weights]):
    def __init__(self, risk_model: RiskModel):
        self.risk_model = risk_model
        self.weights = Parameter(shape=(N,))

    async def __call__(self, signal: Signal) -> Weights:

        # 1. Define Loss (Negative Sharpe or Variance)
        def loss_fn(w):
            return w.T @ self.risk_model.cov @ w - lambda_ * (w.T @ signal.expected_return)

        # 2. Apply Gradient Descent (The Calculus)

        # Eigen automatically computes the gradient of the Operator
        grad = Gradient(loss_fn)(self.weights)
        
        # 3. Update State
        self.weights -= 0.01 * grad
        
        return Weights(self.weights)

```

This unifies **Machine Learning** (Backprop) and **Convex Optimization** (QP)
under the same algebraic operator.

## 17.6 The Multiverse: Risk Simulation (Epoch X)

While Backtesting replays *one* history, **Monte Carlo Simulation** explores
*many* possible histories.
This connects directly to **Epoch X: The Multiverse**.

We use the `Fork` and `QuantumSuicide` operators to simulate thousands of market
scenarios simultaneously.

```python
from eigen.cosmos.multi import Fork, QuantumSuicide

# Define the Stress Test

# In 95% of universes, the market is normal.

# In 5% of universes, we crash the market.
MarketCondition = Fork(1000) >> Choice([
    (0.95, NormalMarket()),
    (0.05, CrashMarket(drop=0.20))
])

# Run Strategy across the Multiverse
Simulation = MarketCondition >> Strategy >> MeasureRisk()

# Collapse the Wavefunction

# We want the strategy to survive in at least 99% of universes.
VaR = Simulation >> Merge(criteria="p99_loss")

```

This treats "Risk" not as a single number, but as the **Survivor Rate** across
the multiverse.

## 17.7 Prescient Trading: Negative Latency (Epoch VIII)

In HFT, speed is everything. But the speed of light is finite ($c$).
To beat the speed of light, we must use **Prescience** (Epoch VIII).

Instead of waiting for an event to happen ($t_0$) and then reacting ($t_1$), we
compute the reaction at $t_{-1}$ for all likely events.

```python
from eigen.cosmos.void import Prescience

# Pre-calculate reaction to Fed Announcement

# The 'Prescience' operator computes both branches (Rates Up, Rates Down)

# and caches the result in L1 CPU cache *before* the announcement.
HFT_Strategy = (
    Prescience(
        scenarios={"up": "Buy USD", "down": "Sell USD"},
        trigger=FedAnnouncement()
    )
    >> Execution()
)

```

When the event occurs, the `latency` is effectively the **L1 Cache Access Time**
(~1ns), which is orders of magnitude faster than computing the logic (~10µs).
This is **Negative Latency** relative to the computation time.

## 17.8 Practice: Strategy Design

1.  **Lookahead Bias**: The `VirtualClock` must strictly enforce causality.
    Future leakage violates the Causal Principle ($t_1 > t_0$).
    *   *Anti-Pattern*: Calculating `Close[t]` using `Close[t+1]`.
    *   *Eigen Solution*: The `Flow` operator enforces temporal ordering.
2.  **Overfitting**: This is "Data Dredging". Use `InvarianceStrategy` (Book IV)
    to test robust parameters.
    *   Run the same strategy on disjoint time periods (Regimes).
3.  **Latent States**: Use `Wavefunction` to carry hidden state (e.g., current
    position) through the pipeline. Do not use global variables.

> "The goal is not to predict the future, but to be positioned for it."

---
**Eigen Cosmology** | [Previous: Book XVII](17_DOMAIN_QUANTUM_FINANCE_I.md) | [Index](../00_INDEX.md) | [Next: Book XIX](19_DOMAIN_DATA_RELATIVITY_I.md) | *© 2025 The Eigen High Council*
