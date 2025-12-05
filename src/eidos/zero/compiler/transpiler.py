from typing import Any, Dict, List, Protocol
from ..symbolism.ast import Graph, Node, OpType

class BackendCompiler(Protocol):
    def compile_node(self, node: Node, inputs: List[Any]) -> Any:
        ...

class Transpiler:
    """
    Generic Graph Walker that delegates node compilation to a backend.
    """
    def __init__(self, backend: BackendCompiler):
        self.backend = backend

    def compile(self, graph: Graph) -> Any:
        # Simple memoized recursive visitor for DAG traversal
        compiled_nodes: Dict[str, Any] = {}
        
        def visit(node_id: str) -> Any:
            if node_id in compiled_nodes:
                return compiled_nodes[node_id]
            
            node = graph.nodes[node_id]
            
            # Compile parents first
            parent_results = []
            for pid in node.parents:
                parent_results.append(visit(pid))
            
            # Compile current node
            result = self.backend.compile_node(node, parent_results)
            compiled_nodes[node_id] = result
            return result
        
        sinks = graph.sinks
        if not sinks:
            parent_ids = set(p for p, c in graph.edges)
            leaf_ids = [n for n in graph.nodes if n not in parent_ids]
            results = [visit(lid) for lid in leaf_ids]
        else:
            results = [visit(sink.id) for sink in sinks]
            
        if len(results) == 1:
            return results[0]
        return results

class StringBackend:
    """
    A mock backend that generates a string representation (IR) of the plan.
    """
    def compile_node(self, node: Node, inputs: List[str]) -> str:
        if node.op_type == OpType.SOURCE:
            return f"Scan({node.config.get('uri', 'unknown')})"
        
        inp = inputs[0] if inputs else "None"
        
        if node.op_type == OpType.MAP:
            fn = node.config.get('fn_name', 'fn')
            return f"Map({inp}, fn={fn})"
            
        if node.op_type == OpType.FILTER:
            fn = node.config.get('fn_name', 'pred')
            return f"Filter({inp}, pred={fn})"
            
        if node.op_type == OpType.SINK:
            uri = node.config.get('uri', 'stdout')
            return f"Sink({inp}, target={uri})"
        
        if node.op_type == OpType.CUSTOM:
            kind = node.config.get("kind", "Custom")
            return f"{kind}({inp})"

        if node.op_type == OpType.CHOICE:
            return f"Choice({', '.join(inputs)})"

        if node.op_type == OpType.ENSEMBLE:
            return f"Ensemble({', '.join(inputs)})"

        if node.op_type == OpType.MERGE:
            return f"Merge({', '.join(inputs)})"
            
        return f"Unknown({node.op_type})"

class Compiler:
    """
    Main entry point for compilation.
    """
    @staticmethod
    def compile(graph: Graph, target: str = "string") -> Any:
        if target == "string":
            backend = StringBackend()
        elif target == "polars":
            from .polars_backend import PolarsBackend
            backend = PolarsBackend()
        elif target == "ray":
            from .ray_backend import RayBackend
            backend = RayBackend()
        elif target == "dolphindb":
            from .dolphindb_backend import DolphinDBBackend
            backend = DolphinDBBackend()
        else:
            raise ValueError(f"Unknown target: {target}")
            
        transpiler = Transpiler(backend)
        return transpiler.compile(graph)
