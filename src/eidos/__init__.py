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
from .system.logging import configure_logging, get_logger
from .system.config import settings

# Initialize default logging (can be re-configured by CLI)
configure_logging(level=settings.log_level, json_format=settings.json_logs)
logger = get_logger("eidos")

def run(flow, engine=None):
    """
    Compiles and runs the given flow.
    """
    engine = engine or settings.default_backend
    logger.debug("Running flow", engine=engine)
    if hasattr(flow, "compile"):
        graph = flow.compile()
        # Detect available backends
        target = engine
        if target == "polars":
            try:
                import polars
            except ImportError:
                # Fallback to Python Native Backend (Free Lane)
                logger.warning("Polars not found, falling back to Python backend")
                target = "python"
        
        return Compiler.compile(graph, target=target)
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

__version__ = "1.0.0"
