from typing import Any, List
from ..symbolism.ast import Node, OpType

try:
    import ray
    from ray.data import Dataset
except ImportError:
    ray = None
    Dataset = Any

class RayBackend:
    """
    Compiles Eidos AST into Ray Data execution plan.
    """
    def compile_node(self, node: Node, inputs: List[Any]) -> Any:
        if ray is None:
            raise ImportError("Ray is not installed. Please pip install 'ray[data]'.")
        
        if node.op_type == OpType.SOURCE:
            uri = node.config.get("uri", "")
            if uri.startswith("parquet://") or uri.endswith(".parquet"):
                return ray.data.read_parquet(uri.replace("parquet://", ""))
            elif uri.startswith("csv://") or uri.endswith(".csv"):
                return ray.data.read_csv(uri.replace("csv://", ""))
            else:
                # Fallback
                return ray.data.from_items([{"status": "dummy_ray_source"}])

        if not inputs:
             raise ValueError(f"Node {node.op_type} requires input")

        ds = inputs[0]
        
        if node.op_type == OpType.MAP:
            fn = node.config.get("fn")
            if fn:
                return ds.map(fn)
            return ds
        
        if node.op_type == OpType.FILTER:
            pred = node.config.get("predicate")
            if pred:
                return ds.filter(pred)
            return ds
                
        if node.op_type == OpType.SINK:
            uri = node.config.get("uri", "")
            # Returns an action
            def execute():
                if uri == "collect":
                    return ds.take_all()
                elif uri.startswith("parquet://"):
                    path = uri.replace("parquet://", "")
                    ds.write_parquet(path)
                    return path
                else:
                    ds.show(limit=5)
                    return "shown"
            return execute
            
        return ds
