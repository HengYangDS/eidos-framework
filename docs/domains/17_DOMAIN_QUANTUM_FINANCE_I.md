# Book XVII: QUANTUM FINANCE - Microstructure (The Field)

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

> "The market is a quantum field of orders. Price is just the collapse of the
> wavefunction."
> — *The Efficient Market Hypothesis (Refuted)*

## 16.1 The Particle: Tick

In High-Frequency Trading (HFT), the fundamental particle is the **Tick**.
It represents a discrete event in the market spacetime $(x, t)$.
Unlike classical particles, ticks are Fermions (they occupy a unique state in
the matching engine sequence).

### Implementation (Fermion)

```python
from dataclasses import dataclass
from typing import Literal
from eigen.logos import Fermion

@dataclass(frozen=True, slots=True)
class Tick(Fermion):
    """
    The fundamental quantum of market information.
    """
    symbol: str
    timestamp: int  # Nanoseconds (Event Time)
    price: float
    volume: float
    side: Literal["buy", "sell", "none"]
    
    @property
    def notional(self) -> float:
        return self.price * self.volume

    def __lt__(self, other: "Tick") -> bool:

        # Causal ordering
        return self.timestamp < other.timestamp

```

## 16.2 The Potential: Order Book

The **Limit Order Book (LOB)** creates a Potential Well $V(x)$.
*   **Bids**: Attractive force (Potential well). Traders want to sell here.
*   **Asks**: Repulsive force (Potential barrier). Traders must pay energy to
    buy here.

Incoming Market Orders act like particles scattering off this potential. If the
particle has enough energy (Price), it tunnels through the spread.

### Order Matching Engine (The Hamiltoniam)

```python
class OrderBook(Operator[Tick, "MarketSnapshot"]):
    """
    Accumulates Ticks into a State (L2 Snapshot).
    This is a Stateful Operator (Non-unitary evolution).
    """
    def __init__(self, depth: int = 10):
        self.bids = {} # Price -> Vol
        self.asks = {} # Price -> Vol
        self.depth = depth
        self.last_update = 0

    async def __call__(self, tick: Tick) -> "MarketSnapshot":

        # 1. Update State (Wavefunction Evolution)
        if tick.side == "buy":
            self.bids[tick.price] = tick.volume
        elif tick.side == "sell":
            self.asks[tick.price] = tick.volume
            
        # 2. Maintain Invariants (Conservation of Order)
        self._prune_crossed_book()
            
        # 3. Emit Snapshot (Measurement Collapse)

        # Only emit if state changed significantly (Quantized update)
        if tick.timestamp - self.last_update > 1_000_000: # 1ms
            self.last_update = tick.timestamp
            return self._snapshot(tick.timestamp)
        
        # Virtual Particle (Internal state change, no observable emission)
        raise ParticleAbsorbed()

    def _prune_crossed_book(self):
        """Removes impossible states where Bid >= Ask."""
        while self.bids and self.asks and max(self.bids) >= min(self.asks):

            # Annihilation event
            best_bid = max(self.bids)
            best_ask = min(self.asks)
            del self.bids[best_bid]
            del self.asks[best_ask]

```

## 16.3 Heisenberg Uncertainty in HFT

In HFT, observing the market (placing an order) changes the market (Market
Impact).
This is the **Heisenberg Uncertainty Principle of Finance**.

$$ \Delta P \cdot \Delta V \geq \frac{\hbar_{liquidity}}{2} $$

You cannot know the exact Price ($P$) and exact Liquidity ($V$) simultaneously
for large orders.
*   If you probe with a small order ($\Delta V \to 0$), you measure $P$
    accurately but know nothing about depth.
*   If you probe with a large order, you measure depth but shift $P$ (Slippage).

**Eigen Strategy**: Use **Iceberg Orders** (Virtual Particles) to minimize
wavefunction collapse.

## 16.4 Time Resampling (Renormalization)

Tick data is non-uniform (Quantum Noise). Events happen in bursts.
To apply standard signal processing (FFT, SMA), we must **Renormalize** time
(Resample) to uniform bars (OHLCV).
Algebraically, this is the **Quantization Operator** (`//`).

$$ \text{Bars} = \text{Ticks} // \text{"1s"} $$

### The Renormalization Group Flow

```python
class Resample(Operator[Tick, "Bar"]):
    """
    Renormalizes the time dimension.
    t -> t' = floor(t / interval)
    """
    def __init__(self, interval: str = "1s"):
        self.interval_ns = self._parse(interval)
        self.current_bar = None

    async def __call__(self, tick: Tick) -> "Bar":

        # Quantize time
        bucket = tick.timestamp // self.interval_ns
        
        if self.current_bar and bucket > self.current_bar.bucket:

            # Emit completed bar (Phase Transition)
            closed_bar = self.current_bar

            # Start new epoch
            self.current_bar = Bar(
                bucket=bucket, 
                open=tick.price, 
                high=tick.price, 
                low=tick.price, 
                close=tick.price, 
                volume=tick.volume
            )
            return closed_bar
            
        # Accumulate energy in current bucket
        if not self.current_bar:
             self.current_bar = Bar(bucket=bucket, open=tick.price, ...)
        
        self.current_bar.high = max(self.current_bar.high, tick.price)
        self.current_bar.low = min(self.current_bar.low, tick.price)
        self.current_bar.close = tick.price
        self.current_bar.volume += tick.volume
        
        raise ParticleAbsorbed() # Don't emit yet

```

## 16.5 Practice: Microstructure Engineering

### 1. Zero Copy Transport
Ticks arrive at millions per second. Python objects are too heavy (28 bytes +
overhead).
We use **PolarsReactor** to process them as a Stream Tensor.
The memory remains in the Arrow buffer (Rust/C++). Python only touches the
metadata.

### 2. Event Time vs Processing Time
Always use the Exchange Timestamp ($t_{exchange}$), not the Receipt Timestamp
($t_{local}$).
Relativity matters.
$$ t_{local} = t_{exchange} + \frac{d}{c} + \epsilon_{jitter} $$
Strategies based on $t_{local}$ are hallucinating causality.

### 3. Backpressure (Thermodynamic Choke)
If the Hamiltonian is slower than the Market, the buffer fills up ($P \to
\infty$).
Use **Shedding** strategies:
*   **DropShedder**: Randomly drop particles (Lossy).
*   **ToDisk**: Spill to NVMe (Lossless but slow).
*   **Collapse**: Summarize 10 ticks into 1 bar immediately.

> "Alpha is just energy extraction from market inefficiencies. The market tries
> to close the gap; we try to keep it open."

---
**Eigen Cosmology** | [Previous: Book XVI](../operators/16_OPERATORS_ALGEBRA.md) | [Index](../00_INDEX.md) | [Next: Book XVIII](18_DOMAIN_QUANTUM_FINANCE_II.md) | *© 2025 The Eigen High Council*
