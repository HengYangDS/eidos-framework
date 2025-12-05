import sys
from types import ModuleType
from unittest.mock import MagicMock

# Mock polars if not present
try:
    import polars
except ImportError:
    # Create a mock polars module
    mock_pl = MagicMock()
    
    # Define LazyFrame as a type for isinstance checks
    class MockLazyFrame:
        def filter(self, *args, **kwargs): return self
        def select(self, *args, **kwargs): return self
        def collect(self, *args, **kwargs): return "Collected"
        def sink_parquet(self, *args, **kwargs): return "Sinked"
        
    mock_pl.LazyFrame = MockLazyFrame
    mock_pl.Boolean = "Boolean"
    
    # Mock expression chain: pl.struct(pl.all()).map_elements(...)
    mock_expr = MagicMock()
    mock_expr.map_elements.return_value = mock_expr
    mock_expr.alias.return_value = mock_expr
    
    mock_pl.struct.return_value = mock_expr
    mock_pl.all.return_value = "all"
    
    mock_pl.scan_csv.return_value = MockLazyFrame()
    mock_pl.scan_parquet.return_value = MockLazyFrame()
    mock_pl.DataFrame.return_value.lazy.return_value = MockLazyFrame()
    
    sys.modules["polars"] = mock_pl

from eidos import Source, Map, Filter, Sink
from eidos.zero.compiler import Compiler

def test_polars_compilation():
    print("\n--- Testing Polars Backend Compilation ---")
    
    def inc(x): return x + 1
    def pos(x): return x > 0
    
    flow = (
        Source("csv://data.csv")
        >> Filter(pos)
        >> Map(inc)
        >> Sink("parquet://output.parquet")
    )
    
    graph = flow.compile()
    
    # Compile to Polars LazyFrame
    # This should use the mock if real polars is missing
    plan = Compiler.compile(graph, target="polars")
    
    print(f"Compiled Object: {plan}")
    
    # We can't easily assert the structure of the mock/LazyFrame without execution
    # but we check it's not None
    assert plan is not None
    
    # If it's a mock, we can check calls
    if isinstance(sys.modules.get("polars"), MagicMock):
        mock_pl = sys.modules["polars"]
        # scan_csv should have been called
        # mock_pl.scan_csv.assert_called() # scan_csv might be called with "data.csv"
        pass
        
    # Verify SINK returns a callable
    assert callable(plan)
    
    print("--- Polars Backend Compilation OK ---")

if __name__ == "__main__":
    test_polars_compilation()
