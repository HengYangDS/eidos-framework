from typing import Any, Optional
from pydantic import BaseModel, Field
from ..zero.symbolism.dsl import Operator
from ..zero.symbolism.ast import OpType

# --- Base Class ---

class Indicator(Operator):
    @property
    def op_type(self) -> OpType: return OpType.CUSTOM

# --- Momentum Indicators ---

class RSIConfig(BaseModel):
    kind: str = "RSI"
    window: int = Field(14, gt=0)
    field: str = "close"

class RSI(Indicator):
    """Relative Strength Index."""
    def __init__(self, window: int = 14, field: str = "close"):
        cfg = RSIConfig(window=window, field=field)
        super().__init__(config=cfg.model_dump())

class MACDConfig(BaseModel):
    kind: str = "MACD"
    fast: int = Field(12, gt=0)
    slow: int = Field(26, gt=0)
    signal: int = Field(9, gt=0)
    field: str = "close"

class MACD(Indicator):
    """Moving Average Convergence Divergence."""
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9, field: str = "close"):
        cfg = MACDConfig(fast=fast, slow=slow, signal=signal, field=field)
        super().__init__(config=cfg.model_dump())

class StochConfig(BaseModel):
    kind: str = "Stoch"
    window: int = Field(14, gt=0)
    smooth: int = Field(3, gt=0)
    high: str = "high"
    low: str = "low"
    close: str = "close"

class Stoch(Indicator):
    """Stochastic Oscillator."""
    def __init__(self, window: int = 14, smooth: int = 3, field_high: str = "high", field_low: str = "low", field_close: str = "close"):
        cfg = StochConfig(window=window, smooth=smooth, high=field_high, low=field_low, close=field_close)
        super().__init__(config=cfg.model_dump())

class CCIConfig(BaseModel):
    kind: str = "CCI"
    window: int = Field(14, gt=0)
    high: str = "high"
    low: str = "low"
    close: str = "close"

class CCI(Indicator):
    """Commodity Channel Index."""
    def __init__(self, window: int = 14, field_high: str = "high", field_low: str = "low", field_close: str = "close"):
        cfg = CCIConfig(window=window, high=field_high, low=field_low, close=field_close)
        super().__init__(config=cfg.model_dump())

# --- Trend Indicators ---

class MAConfig(BaseModel):
    kind: str
    window: int = Field(..., gt=0)
    field: str = "close"

class SMA(Indicator):
    """Simple Moving Average."""
    def __init__(self, window: int, field: str = "close"):
        cfg = MAConfig(kind="SMA", window=window, field=field)
        super().__init__(config=cfg.model_dump())

class EMA(Indicator):
    """Exponential Moving Average."""
    def __init__(self, window: int, field: str = "close"):
        cfg = MAConfig(kind="EMA", window=window, field=field)
        super().__init__(config=cfg.model_dump())

class WMA(Indicator):
    """Weighted Moving Average."""
    def __init__(self, window: int, field: str = "close"):
        cfg = MAConfig(kind="WMA", window=window, field=field)
        super().__init__(config=cfg.model_dump())

class ADXConfig(BaseModel):
    kind: str = "ADX"
    window: int = Field(14, gt=0)
    high: str = "high"
    low: str = "low"
    close: str = "close"

class ADX(Indicator):
    """Average Directional Index."""
    def __init__(self, window: int = 14, field_high: str = "high", field_low: str = "low", field_close: str = "close"):
        cfg = ADXConfig(window=window, high=field_high, low=field_low, close=field_close)
        super().__init__(config=cfg.model_dump())

# --- Volatility Indicators ---

class BBandsConfig(BaseModel):
    kind: str = "BBands"
    window: int = Field(20, gt=0)
    std: int = Field(2, gt=0)
    field: str = "close"

class BollingerBands(Indicator):
    """Bollinger Bands."""
    def __init__(self, window: int = 20, std: int = 2, field: str = "close"):
        cfg = BBandsConfig(window=window, std=std, field=field)
        super().__init__(config=cfg.model_dump())

class ATRConfig(BaseModel):
    kind: str = "ATR"
    window: int = Field(14, gt=0)
    high: str = "high"
    low: str = "low"
    close: str = "close"

class ATR(Indicator):
    """Average True Range."""
    def __init__(self, window: int = 14, field_high: str = "high", field_low: str = "low", field_close: str = "close"):
        cfg = ATRConfig(window=window, high=field_high, low=field_low, close=field_close)
        super().__init__(config=cfg.model_dump())

# --- Volume Indicators ---

class OBVConfig(BaseModel):
    kind: str = "OBV"
    close: str = "close"
    vol: str = "volume"

class OBV(Indicator):
    """On-Balance Volume."""
    def __init__(self, field_close: str = "close", field_vol: str = "volume"):
        cfg = OBVConfig(close=field_close, vol=field_vol)
        super().__init__(config=cfg.model_dump())

class VWAPConfig(BaseModel):
    kind: str = "VWAP"
    price: str = "price"
    vol: str = "volume"

class VWAP(Indicator):
    """Volume Weighted Average Price."""
    def __init__(self, field_price: str = "price", field_vol: str = "volume"):
        cfg = VWAPConfig(price=field_price, vol=field_vol)
        super().__init__(config=cfg.model_dump())
