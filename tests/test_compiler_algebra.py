from eidos.zero.symbolism.dsl import Source, Map
from eidos.zero.compiler import Compiler

def test_compiler_algebra():
    print("\n--- Testing Compiler Algebra ---")
    s1 = Source("A")
    op = Map(lambda x: x) | Map(lambda x: x)
    flow = s1 >> op
    
    graph = flow.compile()
    plan = Compiler.compile(graph, target="string")
    print(f"Plan: {plan}")
    # plan is a single string if one leaf, or list if multiple
    if isinstance(plan, list):
        assert any("Choice" in p for p in plan)
    else:
        assert "Choice" in plan
    
    s2 = Source("B")
    flow2 = s1 + s2
    graph2 = flow2.compile()
    plan2 = Compiler.compile(graph2, target="string")
    print(f"Plan2: {plan2}")
    
    # graph2 contains flow1's choice node AND the new merge node
    assert isinstance(plan2, list)
    assert any("Merge" in p for p in plan2)
    
    print("--- Compiler Algebra OK ---")

if __name__ == "__main__":
    test_compiler_algebra()
