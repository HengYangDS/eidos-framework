from typing import Any, List, Optional, Callable, Dict
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
        self._custom_compilers: Dict[str, Callable] = {
            "SMA": self._compile_sma,
            "BBands": self._compile_bbands
        }

    def compile_node(self, node: Node, inputs: List[Any]) -> Any:
        if pl is None:
            raise ImportError("Polars is not installed. Please pip install polars.")

        if node.op_type == OpType.SOURCE:
            uri = node.config.get("uri", "")
            if uri.startswith("csv://") or uri.endswith(".csv"):
                clean_uri = uri.replace("csv://", "")
                return pl.scan_csv(clean_uri)
            elif uri.startswith("parquet://") or uri.endswith(".parquet"):
                clean_uri = uri.replace("parquet://", "")
                return pl.scan_parquet(clean_uri)
            else:
                # Fallback for testing
                return pl.DataFrame({"close": [1, 2, 3, 4, 5]}).lazy()

        if not inputs:
             raise ValueError(f"Node {node.op_type} requires input")
        
        lf = inputs[0]
        if not isinstance(lf, pl.LazyFrame):
            return lf # Pass through if it's a sink result

        if node.op_type == OpType.FILTER:
            predicate = node.config.get("predicate")
            if predicate:
                return lf.filter(
                    pl.struct(pl.all()).map_elements(predicate, return_dtype=pl.Boolean)
                )
            return lf

        if node.op_type == OpType.MAP:
            fn = node.config.get("fn")
            if fn:
                return lf.select(
                    pl.struct(pl.all()).map_elements(fn).alias("payload")
                )
            return lf

        if node.op_type == OpType.CUSTOM:
            kind = node.config.get("kind")
            if kind in self._custom_compilers:
                return self._custom_compilers[kind](node, lf)
            else:
                print(f"[Warn] No compiler for custom op {kind}, passing through.")
                return lf

        if node.op_type == OpType.SINK:
            uri = node.config.get("uri", "")
            def execute():
                if uri == "collect":
                    return lf.collect()
                elif uri.startswith("parquet://"):
                    path = uri.replace("parquet://", "")
                    return lf.sink_parquet(path)
                else:
                    return lf.collect()
            return execute

        return lf

    def _compile_sma(self, node: Node, lf: pl.LazyFrame) -> pl.LazyFrame:
        window = node.config["window"]
        field = node.config["field"]
        return lf.with_columns(
            pl.col(field).rolling_mean(window_size=window).alias(f"sma_{window}")
        )

    def _compile_bbands(self, node: Node, lf: pl.LazyFrame) -> pl.LazyFrame:
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
