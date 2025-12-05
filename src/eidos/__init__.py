"""
Eidos: The Neuro-Symbolic Logic Operating System.
"""

from .zero.symbolism import (
    Source, Map, Filter, Sink,
    Operator, SymbolicStream,
    Graph, Node, OpType
)
from .quant import indicators as quant
from .zero.compiler import Compiler

def run(flow, engine="polars"):
    """
    Compiles and runs the given flow.
    """
    if hasattr(flow, "compile"):
        graph = flow.compile()
        # In a real scenario, detect available backends
        try:
            import polars
        except ImportError:
            if engine == "polars":
                engine = "string"
        
        return Compiler.compile(graph, target=engine)
    return None

def mcp_tool(name=None, description=None):
    def decorator(fn):
        fn._is_mcp_tool = True
        fn._mcp_name = name or fn.__name__
        fn._mcp_desc = description
        return fn
    return decorator

def expose(route=None, method="POST"):
    def decorator(fn):
        fn._is_exposed = True
        fn._route = route
        fn._method = method
        return fn
    return decorator

# Expose the DSL as the main entry point
__all__ = [
    "Source", "Map", "Filter", "Sink",
    "Operator", "SymbolicStream",
    "quant", "run", "mcp_tool", "expose"
]

__version__ = "1.0.0-alpha"
