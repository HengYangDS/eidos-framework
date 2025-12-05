from typing import Any, Callable
from ..symbolism.ast import Node, OpType

try:
    import polars as pl
except ImportError:
    pl = None

class PolarsBackend:
    """
    Compiles Eidos AST into Polars LazyFrame.
    """
    def __init__(self):
        self._custom_compilers: dict[str, Callable] = {
            "SMA": self._compile_sma,
            "EMA": self._compile_ema,
            "WMA": self._compile_wma,
            "RSI": self._compile_rsi,
            "MACD": self._compile_macd,
            "BBands": self._compile_bbands,
            "Stoch": self._compile_stoch,
            "CCI": self._compile_cci,
            "ADX": self._compile_adx,
            "ATR": self._compile_atr,
            "OBV": self._compile_obv,
            "VWAP": self._compile_vwap
        }

    def compile_node(self, node: Node, inputs: list[Any]) -> Any:
        if pl is None:
            raise ImportError("Polars is not installed. Please pip install polars.")

        if node.op_type == OpType.SOURCE:
            uri = node.config.get("uri", "")
            match uri:
                case _ if uri.startswith("csv://") or uri.endswith(".csv"):
                    clean_uri = uri.replace("csv://", "")
                    return pl.scan_csv(clean_uri)
                case _ if uri.startswith("parquet://") or uri.endswith(".parquet"):
                    clean_uri = uri.replace("parquet://", "")
                    return pl.scan_parquet(clean_uri)
                case _:
                    # Fallback for testing
                    return pl.DataFrame({"close": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                                         "high": [1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1, 11.1, 12.1, 13.1, 14.1, 15.1],
                                         "low": [0.9, 1.9, 2.9, 3.9, 4.9, 5.9, 6.9, 7.9, 8.9, 9.9, 10.9, 11.9, 12.9, 13.9, 14.9],
                                         "volume": [100] * 15}).lazy()

        if not inputs:
             raise ValueError(f"Node {node.op_type} requires input")
        
        lf = inputs[0]
        if not isinstance(lf, pl.LazyFrame):
            return lf # Pass through if it's a sink result

        match node.op_type:
            case OpType.FILTER:
                if predicate := node.config.get("predicate"):
                    return lf.filter(
                        pl.struct(pl.all()).map_elements(predicate, return_dtype=pl.Boolean)
                    )
                return lf

            case OpType.MAP:
                if fn := node.config.get("fn"):
                    return lf.select(
                        pl.struct(pl.all()).map_elements(fn).alias("payload")
                    )
                return lf

            case OpType.CUSTOM:
                kind = node.config.get("kind")
                if compiler := self._custom_compilers.get(kind):
                    return compiler(node, lf)
                else:
                    print(f"[Warn] No compiler for custom op {kind}, passing through.")
                    return lf

            case OpType.SINK:
                uri = node.config.get("uri", "")
                def execute():
                    match uri:
                        case "collect" | "memory":
                            return lf.collect()
                        case _ if uri.startswith("parquet://"):
                            path = uri.replace("parquet://", "")
                            return lf.sink_parquet(path)
                        case _:
                            return lf.collect()
                return execute

            case _:
                return lf

    def _compile_sma(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        window = node.config["window"]
        field = node.config["field"]
        return lf.with_columns(
            pl.col(field).rolling_mean(window_size=window).alias(f"sma_{window}")
        )

    def _compile_ema(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        window = node.config["window"]
        field = node.config["field"]
        return lf.with_columns(
            pl.col(field).ewm_mean(span=window, adjust=False).alias(f"ema_{window}")
        )

    def _compile_wma(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        window = node.config["window"]
        field = node.config["field"]
        
        # WMA = Sum(Price * Weight) / Sum(Weights)
        # This requires rolling dot product which isn't native expression in Polars yet
        # Falling back to rolling_map (slow but correct)
        weights = list(range(1, window + 1))
        denom = sum(weights)
        
        def wma_calc(values):
             if len(values) != window: return None
             w_sum = sum(w * v for w, v in zip(weights, values))
             return w_sum / denom

        return lf.with_columns(
            pl.col(field).rolling_map(wma_calc, window_size=window).alias(f"wma_{window}")
        )

    def _compile_rsi(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        window = node.config["window"]
        field = node.config["field"]
        
        delta = pl.col(field).diff()
        gain = pl.when(delta > 0).then(delta).otherwise(0)
        loss = pl.when(delta < 0).then(-delta).otherwise(0)
        
        avg_gain = gain.ewm_mean(alpha=1.0/window, adjust=False, min_periods=window)
        avg_loss = loss.ewm_mean(alpha=1.0/window, adjust=False, min_periods=window)
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return lf.with_columns(rsi.alias(f"rsi_{window}"))

    def _compile_macd(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        fast = node.config["fast"]
        slow = node.config["slow"]
        signal = node.config["signal"]
        field = node.config["field"]
        
        fast_ema = pl.col(field).ewm_mean(span=fast, adjust=False)
        slow_ema = pl.col(field).ewm_mean(span=slow, adjust=False)
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm_mean(span=signal, adjust=False)
        
        return lf.with_columns(
            macd_line.alias("macd"),
            signal_line.alias("macd_signal"),
            (macd_line - signal_line).alias("macd_hist")
        )

    def _compile_bbands(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        window = node.config["window"]
        std = node.config["std"]
        field = node.config["field"]
        
        mean = pl.col(field).rolling_mean(window_size=window)
        std_dev = pl.col(field).rolling_std(window_size=window)
        
        return lf.with_columns(
            mean.alias(f"bb_mid"),
            (mean + std * std_dev).alias(f"bb_upper"),
            (mean - std * std_dev).alias(f"bb_lower")
        )

    def _compile_stoch(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        window = node.config["window"]
        smooth = node.config["smooth"]
        high = node.config["high"]
        low = node.config["low"]
        close = node.config["close"]
        
        min_l = pl.col(low).rolling_min(window_size=window)
        max_h = pl.col(high).rolling_max(window_size=window)
        
        k_raw = 100 * (pl.col(close) - min_l) / (max_h - min_l)
        
        return lf.with_columns(
            k_raw.alias("stoch_k"),
            k_raw.rolling_mean(window_size=smooth).alias("stoch_d")
        )

    def _compile_cci(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        window = node.config["window"]
        high = node.config["high"]
        low = node.config["low"]
        close = node.config["close"]
        
        tp = (pl.col(high) + pl.col(low) + pl.col(close)) / 3
        sma_tp = tp.rolling_mean(window_size=window)
        
        # MAD = Mean(|TP - SMA_TP|)
        # We cannot easily compute rolling MAD relative to rolling Mean in one pass without custom map
        # Approximation: Use rolling_std * constant? No, too inaccurate.
        # Use rolling_map
        
        def mad_calc(values):
            if len(values) < window: return None
            # Last value of TP series? No, Polars passes the window of the column it's applied to.
            # But we need TP and SMA_TP.
            # Wait, rolling_map acts on a single series. 
            # We can calculate MAD of TP itself? 
            # CCI = (TP - SMA) / (0.015 * MeanDev)
            # MeanDev is Mean(|TP_i - SMA_TP|) where SMA_TP is constant for the window?
            # Yes, standard definition: MD = Sum(|P_i - SMA|) / N.
            # Since SMA changes every bar, this is computationally heavy.
            
            mean = sum(values) / len(values)
            mad = sum(abs(x - mean) for x in values) / len(values)
            return mad
        
        mad = tp.rolling_map(mad_calc, window_size=window)
        
        cci = (tp - sma_tp) / (0.015 * mad)
        
        return lf.with_columns(cci.alias("cci"))

    def _compile_atr(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        window = node.config["window"]
        high = pl.col(node.config["high"] or "high")
        low = pl.col(node.config["low"] or "low")
        close = pl.col("close") # Assuming 'close' for prev close
        
        # TR = Max(H-L, |H-Cp|, |L-Cp|)
        prev_close = close.shift(1)
        
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        
        tr = pl.max_horizontal(tr1, tr2, tr3)
        
        # Wilder's Smoothing (alpha = 1/n)
        atr = tr.ewm_mean(alpha=1.0/window, adjust=False, min_periods=window)
        
        return lf.with_columns(atr.alias(f"atr_{window}"))

    def _compile_adx(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        window = node.config["window"]
        high = pl.col(node.config.get("high", "high"))
        low = pl.col(node.config.get("low", "low"))
        close = pl.col(node.config.get("close", "close"))
        
        # 1. TR
        prev_close = close.shift(1)
        tr = pl.max_horizontal(
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs()
        )
        
        # 2. DM
        prev_high = high.shift(1)
        prev_low = low.shift(1)
        
        up_move = high - prev_high
        down_move = prev_low - low
        
        plus_dm = pl.when((up_move > down_move) & (up_move > 0)).then(up_move).otherwise(0)
        minus_dm = pl.when((down_move > up_move) & (down_move > 0)).then(down_move).otherwise(0)
        
        # 3. Smooth
        # Wilder's smoothing = ewm(alpha=1/n)
        smooth_tr = tr.ewm_mean(alpha=1.0/window, adjust=False, min_periods=window)
        smooth_pdm = plus_dm.ewm_mean(alpha=1.0/window, adjust=False, min_periods=window)
        smooth_mdm = minus_dm.ewm_mean(alpha=1.0/window, adjust=False, min_periods=window)
        
        # 4. DI
        pdi = 100 * smooth_pdm / smooth_tr
        mdi = 100 * smooth_mdm / smooth_tr
        
        # 5. DX
        dx = 100 * (pdi - mdi).abs() / (pdi + mdi)
        
        # 6. ADX (Smooth DX)
        adx = dx.ewm_mean(alpha=1.0/window, adjust=False, min_periods=window)
        
        return lf.with_columns(adx.alias(f"adx_{window}"))

    def _compile_obv(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        close = pl.col(node.config.get("close", "close"))
        vol = pl.col(node.config.get("vol", "volume"))
        
        diff = close.diff()
        sign = pl.when(diff > 0).then(1).when(diff < 0).then(-1).otherwise(0)
        
        obv = (sign * vol).cum_sum()
        return lf.with_columns(obv.alias("obv"))

    def _compile_vwap(self, node: Node, lf: "pl.LazyFrame") -> "pl.LazyFrame":
        price = pl.col(node.config.get("price", "close"))
        vol = pl.col(node.config.get("vol", "volume"))
        
        cum_pv = (price * vol).cum_sum()
        cum_v = vol.cum_sum()
        
        vwap = cum_pv / cum_v
        return lf.with_columns(vwap.alias("vwap"))
