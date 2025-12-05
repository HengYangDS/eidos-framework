# Eidos Quant: The Financial Mathematics Library

**Eidos Quant** is the "DirectX" of Eidos. It provides a comprehensive suite of high-performance, vectorized financial operators that serve as the benchmark for the kernel's capabilities.

It is designed to bridge the gap between **Python Research** (backtesting) and **C++ Production** (execution).

## 1. Core Indicators (Native Implementation)

All indicators are backend-agnostic. They compile to:
*   **Polars**: Native Rust-backed vectorized expressions (Zero-Copy).
*   **DolphinDB**: Transpiled to `.dos` scripts using built-in functions (`mavg`, `rsi`, `cci`).
*   **Python**: Pure Python generators (No-GIL) for debugging and simple backtesting.

### Momentum
*   `RSI(window=14)`: Relative Strength Index.
*   `MACD(fast=12, slow=26, signal=9)`: Moving Average Convergence Divergence.
*   `Stoch(window=14, smooth=3)`: Stochastic Oscillator (%K, %D).
*   `CCI(window=14)`: Commodity Channel Index.

### Trend
*   `SMA(window)`: Simple Moving Average.
*   `EMA(window)`: Exponential Moving Average.
*   `WMA(window)`: Weighted Moving Average.
*   `ADX(window=14)`: Average Directional Index (Wilder's Smoothing).

### Volatility
*   `BollingerBands(window=20, std=2)`: Upper, Middle, Lower bands.
*   `ATR(window=14)`: Average True Range (Wilder's Smoothing).

### Volume
*   `OBV()`: On-Balance Volume.
*   `VWAP()`: Volume Weighted Average Price.

### Type Safety & Validation (New in v1.0)
All indicators are strongly typed and validated at runtime using **Pydantic**.
*   **Validation**: `RSI(window=-1)` raises a `ValidationError` immediately during definition, preventing invalid topologies.
*   **Schema**: Each operator exposes its configuration schema (e.g., `RSIConfig`), enabling auto-generated UI forms in the future Web Studio.

## 2. Time Series Primitives

Eidos Quant introduces a **Temporal Calculus** that is missing from standard SQL.

### `Lag(k: int, by: str = None)`
Shifts the series backwards in time.
*   **Logic**: $x_t \to x_{t-k}$
*   **Usage**: `Close - Lag(1)` gives the price change.

### `Diff(k: int)`
Calculates discrete difference. Equivalent to `x - Lag(k)`.

### `Returns(method="log" | "simple")`
Calculates financial returns.
*   **Log**: $\ln(P_t / P_{t-1})$ (Additive, preferred for modeling).
*   **Simple**: $(P_t - P_{t-1}) / P_{t-1}$.

### `Resample(rule: str, method: str = "last")`
Changes the time frequency.
*   **Downsampling**: `1m -> 1h`. Aggregation required (OHLCV construction).
*   **Upsampling**: `1d -> 1h`. Interpolation required (`ffill`, `linear`).

### `AsOfJoin` (The "Quant Join")
Matches records based on the closest timestamp without looking into the future.
*   **Critical for**: Joining high-frequency quotes with lower-frequency trades.
*   **Zero-Lookahead**: Guaranteed by the compiler.

## 3. Backtesting Engine

The `Backtest` operator is a "Meta-Operator" that compiles the upstream logic into an event-driven or vectorized simulation.

```python
from eidos.quant import Backtest, Signal, Portfolio

strategy = (
    Source("market_data")
    # 1. Alpha Generation
    >> WithColumns(
        rsi = RSI(14),
        ma_50 = SMA(50)
    )
    >> Filter(col("rsi") < 30) # Buy Signal
    
    # 2. Portfolio Construction
    >> Signal(
        weight = 1.0 / col("volatility"), # Inverse Volatility Sizing
        side = "long"
    )
    
    # 3. Simulation
    >> Backtest(
        initial_capital = 1_000_000,
        fees = 0.0005,
        slippage = 0.0001,
        benchmark = "SPY"
    )
)
```

### 3.1 Compilation Strategy
*   **Vectorized Mode (Default)**: Compiles to a giant Polars expression tree. Extremely fast (seconds for 10 years of data). Supports logic that doesn't have path dependence (e.g., rebalancing every day).
*   **Event Mode**: Compiles to a Python Loop or C++ Runner. Required for logic where today's trade depends on yesterday's exact filled quantity (complex path dependence).

## 4. DolphinDB Integration

When the source is a DolphinDB URI, Eidos Quant performs **Operator Transpilation**.

**Python DSL**:
```python
Source("dfs://stock") >> Filter(col("symbol") == "AAPL") >> MACD(12, 26, 9)
```

**Compiled DolphinDB Script (`.dos`)**:
```sql
t = loadTable("dfs://stock")
selected = select * from t where symbol = "AAPL"
result = select *, mavg(close, 12) - mavg(close, 26) as macd_line from selected
```

This ensures that the heavy lifting happens on the DB server, not the client.
