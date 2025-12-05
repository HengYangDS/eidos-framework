from eidos.zero.symbolism.dsl import Source, Map
from eidos.zero.compiler import Compiler

def test_stream_algebra():
    print("\n--- Testing Stream Algebra (s1 | s2) ---")
    s1 = Source("A")
    s2 = Source("B")
    
    # Choice: s1 | s2 (Fallback)
    choice_stream = s1 | s2
    graph_c = choice_stream.compile()
    plan_c = Compiler.compile(graph_c, target="string")
    print(f"Choice Plan: {plan_c}")
    
    assert "Choice(Scan(A), Scan(B))" in plan_c or "Choice(Scan(B), Scan(A))" in plan_c
    
    # Ensemble: s1 & s2 (Parallel)
    ensemble_stream = s1 & s2
    graph_e = ensemble_stream.compile()
    plan_e = Compiler.compile(graph_e, target="string")
    print(f"Ensemble Plan: {plan_e}")
    
    assert "Ensemble(Scan(A), Scan(B))" in plan_e or "Ensemble(Scan(B), Scan(A))" in plan_e
    
    print("--- Stream Algebra OK ---")

if __name__ == "__main__":
    test_stream_algebra()
