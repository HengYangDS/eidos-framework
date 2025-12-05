from eidos import Source, Map, Filter, Sink
from eidos.zero.compiler import Compiler

def test_string_compilation():
    def inc(x): return x + 1
    def pos(x): return x > 0
    
    flow = (
        Source("csv://data.csv")
        >> Filter(pos)
        >> Map(inc)
        >> Sink("stdout")
    )
    
    graph = flow.compile()
    
    # Use the StringBackend (default)
    plan_str = Compiler.compile(graph, target="string")
    
    print(f"Compiled Plan: {plan_str}")
    
    # Note: The string representation depends on function names 'inc' and 'pos'
    expected = "Sink(Map(Filter(Scan(csv://data.csv), pred=pos), fn=inc), target=stdout)"
    assert plan_str == expected

if __name__ == "__main__":
    test_string_compilation()
