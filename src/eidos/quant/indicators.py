from typing import Any, Optional
from ..zero.symbolism.dsl import Operator
from ..zero.symbolism.ast import OpType

# --- Momentum Indicators ---

class RSI(Operator):
    """Relative Strength Index."""
    def __init__(self, window: int = 14, field: str = "close"):
        super().__init__(config={"kind": "RSI", "window": window, "field": field})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

class MACD(Operator):
    """Moving Average Convergence Divergence."""
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9, field: str = "close"):
        super().__init__(config={"kind": "MACD", "fast": fast, "slow": slow, "signal": signal, "field": field})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

class Stoch(Operator):
    """Stochastic Oscillator."""
    def __init__(self, window: int = 14, smooth: int = 3, field_high: str = "high", field_low: str = "low", field_close: str = "close"):
        super().__init__(config={"kind": "Stoch", "window": window, "smooth": smooth, "high": field_high, "low": field_low, "close": field_close})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

class CCI(Operator):
    """Commodity Channel Index."""
    def __init__(self, window: int = 14, field_high: str = "high", field_low: str = "low", field_close: str = "close"):
        super().__init__(config={"kind": "CCI", "window": window, "high": field_high, "low": field_low, "close": field_close})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

# --- Trend Indicators ---

class SMA(Operator):
    """Simple Moving Average."""
    def __init__(self, window: int, field: str = "close"):
        super().__init__(config={"kind": "SMA", "window": window, "field": field})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

class EMA(Operator):
    """Exponential Moving Average."""
    def __init__(self, window: int, field: str = "close"):
        super().__init__(config={"kind": "EMA", "window": window, "field": field})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

class WMA(Operator):
    """Weighted Moving Average."""
    def __init__(self, window: int, field: str = "close"):
        super().__init__(config={"kind": "WMA", "window": window, "field": field})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

class ADX(Operator):
    """Average Directional Index."""
    def __init__(self, window: int = 14):
        super().__init__(config={"kind": "ADX", "window": window})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

# --- Volatility Indicators ---

class BollingerBands(Operator):
    """Bollinger Bands."""
    def __init__(self, window: int = 20, std: int = 2, field: str = "close"):
        super().__init__(config={"kind": "BBands", "window": window, "std": std, "field": field})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

class ATR(Operator):
    """Average True Range."""
    def __init__(self, window: int = 14):
        super().__init__(config={"kind": "ATR", "window": window})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

# --- Volume Indicators ---

class OBV(Operator):
    """On-Balance Volume."""
    def __init__(self, field_close: str = "close", field_vol: str = "volume"):
        super().__init__(config={"kind": "OBV", "close": field_close, "vol": field_vol})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

class VWAP(Operator):
    """Volume Weighted Average Price."""
    def __init__(self, field_price: str = "price", field_vol: str = "volume"):
        super().__init__(config={"kind": "VWAP", "price": field_price, "vol": field_vol})
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM
