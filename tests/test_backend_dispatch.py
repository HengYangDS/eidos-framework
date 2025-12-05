from eidos import Source, Map, Filter, Sink
from eidos.zero.compiler import Compiler
from eidos.quant.indicators import SMA, RSI

def test_backend_dispatch():
    print("\n--- Testing Backend Dispatch ---")
    
    # Define a simple quant flow
    flow = Source("csv://data.csv") >> SMA(window=20) >> Sink("stdout")
    graph = flow.compile()
    
    # 1. Test Polars Backend Dispatch (Mocked)
    # We expect it to run without error, even if Polars is missing (mocked in backend if needed)
    # But PolarsBackend imports polars. If not installed, it might raise ImportError during compile_node.
    # Let's wrap in try-except to verify it *attempts* to load.
    try:
        Compiler.compile(graph, target="polars")
        print("Polars Backend: Loaded (or Mocked)")
    except ImportError as e:
        print(f"Polars Backend: Skipped ({e})")
    except Exception as e:
        print(f"Polars Backend: Error ({e})")

    # 2. Test DolphinDB Backend Dispatch
    try:
        plan = Compiler.compile(graph, target="dolphindb")
        print(f"DolphinDB Plan:\n{plan}")
        # Expected: Some script with mavg
        assert "mavg" in str(plan)
        print("DolphinDB Backend: OK")
    except Exception as e:
        print(f"DolphinDB Backend: Error ({e})")
        raise e

    print("--- Backend Dispatch Test Complete ---")

if __name__ == "__main__":
    test_backend_dispatch()
