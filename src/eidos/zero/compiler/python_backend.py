from typing import Any, List, Iterator, Iterable, Dict
import csv
import io
from ..symbolism.ast import Node, OpType
try:
    from ...quant import python_impl
except ImportError:
    python_impl = None

class PythonBackend:
    """
    The "Free Lane": Pure Python execution using generators.
    No heavy dependencies (Polars/Ray) required.
    """
    def __init__(self):
        self._custom_handlers = {}
        if python_impl:
            self._custom_handlers = {
                "SMA": python_impl.calculate_sma,
                "EMA": python_impl.calculate_ema,
                "WMA": python_impl.calculate_wma,
                "RSI": python_impl.calculate_rsi,
                "MACD": python_impl.calculate_macd,
                "BBands": python_impl.calculate_bbands,
                "Stoch": python_impl.calculate_stoch,
                "CCI": python_impl.calculate_cci,
                "ADX": python_impl.calculate_adx,
                "ATR": python_impl.calculate_atr,
                "OBV": python_impl.calculate_obv,
                "VWAP": python_impl.calculate_vwap
            }

    def compile_node(self, node: Node, inputs: List[Iterable[Any]]) -> Iterable[Any]:
        
        if node.op_type == OpType.SOURCE:
            uri = node.config.get("uri", "")
            
            # --- Universal I/O Sources ---
            if uri.startswith("kafka://"):
                from ...io.kafka import KafkaConnector
                return KafkaConnector.read(uri)
            
            if uri.startswith("redis://"):
                from ...io.redis import RedisConnector
                return RedisConnector.read(uri)
            
            # Basic implementation for CSV and in-memory lists
            if uri.startswith("csv://") or uri.endswith(".csv"):
                path = uri.replace("csv://", "")
                return self._read_csv(path)
            elif isinstance(node.config.get("data"), list):
                return iter(node.config["data"])
            elif node.config.get("uri") == "payload://":
                return iter([node.config.get("payload", {})])
            else:
                # Fallback: simple generator
                return iter([{"data": "dummy"}])

        if not inputs:
             raise ValueError(f"Node {node.op_type} requires input")

        upstream = inputs[0]
        
        if node.op_type == OpType.MAP:
            fn = node.config.get("fn")
            if fn:
                return map(fn, upstream)
            return upstream
        
        if node.op_type == OpType.FILTER:
            pred = node.config.get("predicate")
            if pred:
                return filter(pred, upstream)
            return upstream
            
        if node.op_type == OpType.SINK:
            uri = node.config.get("uri", "")
            
            # --- Universal I/O Sinks ---
            if uri.startswith("kafka://"):
                from ...io.kafka import KafkaConnector
                def execute_kafka():
                    # Consume the write stream to trigger side effects
                    return list(KafkaConnector.write(uri, upstream))
                return execute_kafka

            if uri.startswith("redis://"):
                from ...io.redis import RedisConnector
                def execute_redis():
                    return list(RedisConnector.write(uri, upstream))
                return execute_redis

            # Sink consumes the generator
            def execute():
                results = []
                if uri == "stdout" or uri == "console":
                    print(f"--- Sink: {node.config.get('name', 'Result')} ---")
                    for item in upstream:
                        print(item)
                        results.append(item)
                    print("----------------")
                elif uri == "memory" or uri == "collect":
                    results = list(upstream)
                else:
                    # Write to file
                    try:
                         with open(uri, "w") as f:
                            for item in upstream:
                                f.write(str(item) + "\n")
                                results.append(item)
                    except Exception:
                         # If URI is not a file path, just collect
                         results = list(upstream)
                return results
            return execute

        if node.op_type == OpType.WINDOW:
            size = int(node.config.get("size", 1))
            return self._window_gen(upstream, size)

        # Handling Custom Ops (Quant)
        if node.op_type == OpType.CUSTOM:
            kind = node.config.get("kind")
            if kind in self._custom_handlers:
                # These handlers expect a list of dicts, so we must materialize the upstream
                # This is inefficient for streaming, but required for indicators that need history
                # Future optimization: Use deque buffer
                data = list(upstream)
                
                # Map config to args
                kwargs = {k: v for k, v in node.config.items() if k != "kind"}
                # Fix argument names if needed (e.g., 'std' vs 'std_dev')
                if kind == "BBands" and "std" in kwargs:
                    kwargs["std_dev"] = kwargs.pop("std")
                
                return iter(self._custom_handlers[kind](data, **kwargs))
            
            print(f"[PythonBackend] Warning: Passthrough for Custom Op {kind}")
            return upstream

        return upstream

    def _read_csv(self, path: str) -> Iterator[dict]:
        try:
            with open(path, "r", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Try to convert numbers
                    yield {k: self._try_convert(v) for k, v in row.items()}
        except FileNotFoundError:
            print(f"[PythonBackend] File not found: {path}")
            yield {}

    def _try_convert(self, value):
        try:
            return float(value)
        except ValueError:
            return value

    def _window_gen(self, iterable, size):
        buffer = []
        for item in iterable:
            buffer.append(item)
            if len(buffer) >= size:
                yield buffer.copy()
                buffer.pop(0) # Slide by 1
