from typing import Any
from ..symbolism.ast import Node, OpType

try:
    import ray
    from ray.data import Dataset
except ImportError:
    ray = None
    Dataset = Any

try:
    from ...quant import python_impl
except ImportError:
    python_impl = None

class RayBackend:
    """
    Compiles Eidos AST into Ray Data execution plan.
    """
    def compile_node(self, node: Node, inputs: list[Any]) -> Any:
        if ray is None:
            raise ImportError("Ray is not installed. Please pip install 'ray[data]'.")
        
        if node.op_type == OpType.SOURCE:
            uri = node.config.get("uri", "")
            match uri:
                case _ if uri.startswith("parquet://") or uri.endswith(".parquet"):
                    return ray.data.read_parquet(uri.replace("parquet://", ""))
                case _ if uri.startswith("csv://") or uri.endswith(".csv"):
                    return ray.data.read_csv(uri.replace("csv://", ""))
                case _:
                    # Fallback
                    return ray.data.from_items([{"status": "dummy_ray_source"}])

        if not inputs:
             raise ValueError(f"Node {node.op_type} requires input")

        ds = inputs[0]
        
        match node.op_type:
            case OpType.MAP:
                if fn := node.config.get("fn"):
                    return ds.map(fn)
                return ds
            
            case OpType.FILTER:
                if pred := node.config.get("predicate"):
                    return ds.filter(pred)
                return ds
            
            case OpType.CUSTOM:
                kind = node.config.get("kind")
                # Ray Data is parallel, but stateful window ops (SMA, RSI) require order.
                # We must be careful. Ray Data doesn't strictly guarantee global order unless sorted.
                # For v1.0 Alpha, we assume the dataset fits in memory or we accept partition-local windows.
                # We use map_batches to process chunks.
                
                def batch_wrapper(batch: dict[str, Any]) -> dict[str, Any]:
                    # Convert Ray batch (Dict of arrays) to List of Dicts for python_impl
                    # This is slow but correct for re-use
                    keys = list(batch.keys())
                    length = len(batch[keys[0]])
                    rows = [{k: batch[k][i] for k in keys} for i in range(length)]
                    
                    # Apply logic
                    kwargs = {k: v for k, v in node.config.items() if k != "kind"}
                    # Adjust argument names for compatibility
                    match kind:
                        case "BBands" if "std" in kwargs:
                            kwargs["std_dev"] = kwargs.pop("std")
                    
                    if python_impl and hasattr(python_impl, f"calculate_{kind.lower()}"):
                        func = getattr(python_impl, f"calculate_{kind.lower()}")
                        result_rows = func(rows, **kwargs)
                    else:
                        result_rows = rows # Pass through
                    
                    # Convert back to Dict of arrays
                    # Note: This assumes all rows have same keys
                    if not result_rows:
                        return {k: [] for k in keys}
                    
                    res_keys = list(result_rows[0].keys())
                    res_batch = {k: [r[k] for r in result_rows] for k in res_keys}
                    return res_batch

                return ds.map_batches(batch_wrapper, batch_format="numpy")

            case OpType.SINK:
                uri = node.config.get("uri", "")
                # Returns an action
                def execute():
                    match uri:
                        case "collect":
                            return ds.take_all()
                        case _ if uri.startswith("parquet://"):
                            path = uri.replace("parquet://", "")
                            ds.write_parquet(path)
                            return path
                        case _:
                            ds.show(limit=5)
                            return "shown"
                return execute
                
            case _:
                return ds
