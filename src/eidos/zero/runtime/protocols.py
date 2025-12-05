from typing import Protocol, Set, Any, Dict, List, runtime_checkable
from ..symbolism.ast import Graph
from ..symbolism.types import Monad

@runtime_checkable
class Backend(Protocol):
    """
    Protocol that all execution engines must implement.
    """
    def capabilities(self) -> Set[str]:
        """Returns a set of capabilities, e.g., {'vectorized', 'distributed', 'sql'}."""
        ...

    def execute(self, plan: Any) -> Any:
        """Executes the compiled plan."""
        ...

@runtime_checkable
class Compiler(Protocol):
    """
    Protocol for translating the Logical AST to a Physical Plan.
    """
    def compile(self, graph: Graph) -> Any:
        """Compiles AST to a backend-specific plan (e.g., Polars LazyFrame)."""
        ...

@runtime_checkable
class CognitiveDriver(Protocol):
    """
    Protocol for AI/LLM integration.
    """
    async def synthesize_code(self, intent: str, context: Graph) -> str:
        """Generates code based on intent."""
        ...

    async def diagnose_error(self, trace: Dict[str, Any], data_sample: Any) -> str:
        """Diagnoses runtime errors."""
        ...
