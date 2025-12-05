# Cookbook II: Quantum Finance with Eigen

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

This cookbook demonstrates how to apply Eigen's **Quantum Operators** to high-
frequency trading, portfolio optimization, and risk management.

## Scenario 1: The Momentum Strategy (Stream Processing)

**Goal**: Detect momentum signals in tick data and execute orders.

### 1.1 The Microstructure Hamiltonian

```python
from eigen.core import Flow, Operator, Atom
from eigen.domains.finance import Tick, Order, Signal
from eigen.operators import Window, Filter

# --- 1. Fermions (Market Data) ---
@dataclass
class Tick(Fermion):
    symbol: str
    price: float
    volume: float
    time: float

# --- 2. Bosons (Alpha Factors) ---

class CalculateVWAP(Operator[list[Tick], float]):
    """Volume Weighted Average Price"""
    async def __call__(self, ticks: list[Tick]) -> float:
        pv = sum(t.price * t.volume for t in ticks)
        v = sum(t.volume for t in ticks)
        return pv / v if v > 0 else 0.0

class MomentumSignal(Operator[float, Signal]):
    """Detects if price is diverging from VWAP"""
    def __init__(self, threshold: float):
        self.threshold = threshold
        
    async def __call__(self, vwap: float, current: float) -> Signal:
        drift = (current - vwap) / vwap
        if drift > self.threshold:
            return Signal(side="BUY", strength=drift)
        elif drift < -self.threshold:
            return Signal(side="SELL", strength=-drift)
        return Signal(side="HOLD", strength=0)

# --- 3. The Pipeline ---

# Source: Websocket Feed

# Logic: Window(1s) -> VWAP -> Signal -> Execution

Strategy = (
    MarketSource("BTC-USD")
    >> Window(seconds=1)  # Batch Boson
    >> (CalculateVWAP() & LastPrice()) # Entangle to get both
    >> MomentumSignal(threshold=0.005)
    >> Filter(lambda s: s.side != "HOLD")
    >> ExecuteOrder()
)

```

## Scenario 2: Pairs Trading (Entanglement)

**Goal**: Monitor two correlated assets (e.g., KO and PEP). If the spread
diverges, short the winner and buy the loser.

```python

# --- 1. Entangled Source ---

# We need synchronized observations of both assets.

# We use the Zip operator (a form of Entanglement).

PairSource = Zip(
    MarketSource("KO"), 
    MarketSource("PEP")
)

# --- 2. Spread Calculation ---

@atom
def CalculateSpread(pair: tuple[Tick, Tick]) -> float:
    ko, pep = pair
    return ko.price - pep.price

# --- 3. Mean Reversion Logic ---

class MeanReversion(Operator):
    def __init__(self, mean: float, std: float):
        self.mean = mean
        self.std = std
        
    async def __call__(self, spread: float) -> Order:
        z_score = (spread - self.mean) / self.std
        if z_score > 2.0:
            return Order(side="SELL_SPREAD") # Short KO, Buy PEP
        elif z_score < -2.0:
            return Order(side="BUY_SPREAD")  # Buy KO, Short PEP
            
# --- 4. Execution ---

# The Order must be split back into two atomic orders
SplitExecution = ExecuteLeg1 & ExecuteLeg2

PairsStrategy = (
    PairSource 
    >> CalculateSpread 
    >> MeanReversion(5.0, 1.2)
    >> SplitExecution
)

```

## Scenario 3: Portfolio Optimization (Calculus)

**Goal**: Find the optimal weights $w$ for a portfolio to maximize Sharpe Ratio.
We use Eigen's **Gradient Operator** (`d`) for this.

```python
from eigen.calculus import d, Parameter
from eigen.cosmos import Renormalization

# --- 1. Define the Loss Function (Hamiltonian) ---

# Negative Sharpe Ratio
def loss_function(weights, returns, cov_matrix):
    port_return = weights @ returns
    port_vol = sqrt(weights.T @ cov_matrix @ weights)
    return -(port_return / port_vol)

# --- 2. The Optimizer ---

weights = Parameter([0.5, 0.5], requires_grad=True)

@atom
def Step(data):

    # Compute Gradient
    grad = d(loss_function)(weights, data.returns, data.cov)

    # Update Weights (Gradient Descent)
    weights.data -= 0.01 * grad

    # Project to constraint (sum=1)
    weights.data /= sum(weights.data)
    return weights

# --- 3. Continuous Learning ---

# As new market data arrives, we continuously refine the portfolio
Optimizer = MarketData >> Step >> Rebalance

```

## Scenario 4: Multiverse Risk Simulation

**Goal**: Stress test the strategy against 1000 parallel market scenarios (Monte
Carlo).

```python
from eigen.cosmos import Fork, Merge

# --- 1. Scenario Generator ---

# Generates 1000 permutations of market conditions
Simulations = Fork(1000, generator=MarketSimulator)

# --- 2. The Strategy (Immutable) ---

# We run the SAME strategy logic in all universes
TestRun = Strategy

# --- 3. Collapse (Risk Metrics) ---

# We gather the P&L from all universes
CalculateVaR = Merge(method="percentile_5")

RiskEngine = (
    Simulations 
    >> TestRun 
    >> CalculateVaR
)

```

## Scenario 5: Smart Order Routing (Renormalization)

**Goal**: Route orders based on size.
*   Small Order -> Market Order (Micro scale)
*   Large Order -> TWAP Algo (Macro scale)

```python

# --- 1. The RG Flow ---

# The Renormalization Group decides the implementation based on scale

SmartRoute = RenormalizationGroup(
    threshold=10000, # $10k
    micro=ExecuteMarket,
    macro=ExecuteTWAP
)

OrderFlow = SignalSource >> SmartRoute

```

---
**Eigen Cosmology** | [Previous: Cookbook I](COOKBOOK_01_DATA_ENGINEERING.md) | [Index](../00_INDEX.md) | [Next: Cookbook III](COOKBOOK_03_NEURAL_PHYSICS.md) | *© 2025 The Eigen High Council*
