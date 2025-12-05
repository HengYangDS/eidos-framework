from typing import Any, Protocol
import importlib.metadata
from ..symbolism.ast import Graph, Node, OpType, NodeID
from ...system.telemetry import trace_span
from ...system.governance import LineageRegistry

class BackendCompiler(Protocol):
    def compile_node(self, node: Node, inputs: list[Any]) -> Any:
        ...

class Transpiler:
    """
    Generic Graph Walker that delegates node compilation to a backend.
    """
    def __init__(self, backend: BackendCompiler):
        self.backend = backend

    @trace_span("transpiler.visit")
    def compile(self, graph: Graph) -> Any:
        # Simple memoized recursive visitor for DAG traversal
        compiled_nodes: dict[NodeID, Any] = {}
        
        def visit(node_id: NodeID) -> Any:
            if node_id in compiled_nodes:
                return compiled_nodes[node_id]
            
            node = graph.nodes[node_id]
            
            # Compile parents first
            parent_results = [visit(pid) for pid in node.parents]
            
            # Compile current node
            result = self.backend.compile_node(node, parent_results)
            compiled_nodes[node_id] = result
            return result
        
        sinks = graph.sinks
        if not sinks:
            parent_ids = {p for p, _ in graph.edges}
            leaf_ids = [n.id for n in graph.nodes.values() if n.id not in parent_ids]
            results = [visit(lid) for lid in leaf_ids]
        else:
            results = [visit(sink.id) for sink in sinks]
            
        # Python 3.10+ Pattern Matching
        match results:
            case [single]: return single
            case _: return results

class StringBackend:
    """
    A mock backend that generates a string representation (IR) of the plan.
    """
    @staticmethod
    def compile_node(node: Node, inputs: list[str]) -> str:
        inp = inputs[0] if inputs else "None"
        
        match node.op_type:
            case OpType.SOURCE:
                return f"Scan({node.config.get('uri', 'unknown')})"
            
            case OpType.MAP:
                fn = node.config.get('fn_name', 'fn')
                return f"Map({inp}, fn={fn})"
            
            case OpType.FILTER:
                fn = node.config.get('fn_name', 'pred')
                return f"Filter({inp}, pred={fn})"
            
            case OpType.SINK:
                uri = node.config.get('uri', 'stdout')
                return f"Sink({inp}, target={uri})"
            
            case OpType.CUSTOM:
                kind = node.config.get("kind", "Custom")
                return f"{kind}({inp})"
            
            case OpType.CHOICE:
                return f"Choice({', '.join(inputs)})"
            
            case OpType.ENSEMBLE:
                return f"Ensemble({', '.join(inputs)})"
            
            case OpType.MERGE:
                return f"Merge({', '.join(inputs)})"
                
            case _:
                return f"Unknown({node.op_type})"

class Compiler:
    """
    Main entry point for compilation.
    Supports Plugin Architecture via Entry Points.
    """
    @staticmethod
    @trace_span("compiler.compile")
    def compile(graph: Graph, target: str = "string") -> Any:
        # Register Lineage (Governance)
        try:
            LineageRegistry.register(graph)
        except Exception:
            # Governance failure should not block execution
            pass

        backend = None
        
        # 1. Try plugin discovery (Modern Plugin System)
        try:
            # Access the 'eidos.backends' entry point group
            entry_points = importlib.metadata.entry_points(group="eidos.backends")
            for ep in entry_points:
                if ep.name == target:
                    backend_cls = ep.load()
                    backend = backend_cls()
                    break
        except Exception:
            # Silently fail if no plugins found or error in loading
            pass
            
        # 2. Built-in Backends (Legacy/Core)
        if backend is None:
            match target:
                case "string":
                    backend = StringBackend()
                case "polars":
                    from .polars_backend import PolarsBackend
                    backend = PolarsBackend()
                case "ray":
                    from .ray_backend import RayBackend
                    backend = RayBackend()
                case "dolphindb":
                    from .dolphindb_backend import DolphinDBBackend
                    backend = DolphinDBBackend()
                case "python":
                    from .python_backend import PythonBackend
                    backend = PythonBackend()
                case "triton":
                    from .triton_backend import TritonBackend
                    backend = TritonBackend()
                case _:
                    raise ValueError(f"Unknown target: {target}")
            
        transpiler = Transpiler(backend)
        return transpiler.compile(graph)
