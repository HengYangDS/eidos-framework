# import pytest # Removed for standalone run
from eidos import Source, Map, Filter, Sink, SymbolicStream
from eidos.zero.symbolism import Graph, Node, OpType

def test_pipeline_construction():
    def increment(x):
        return x + 1
    
    def is_positive(x):
        return x > 0

    # Define the logic
    flow = (
        Source("s3://bucket/data.csv")
        >> Filter(is_positive)
        >> Map(increment)
        >> Sink("db://table")
    )
    
    # Compile (get graph)
    graph = flow.compile()
    
    # Assertions
    assert isinstance(graph, Graph)
    assert len(graph.nodes) == 4
    assert len(graph.edges) == 3
    
    # Verify Topological Order (Source -> Filter -> Map -> Sink)
    # Edges are (parent, child)
    
    # Find Source Node
    sources = graph.sources
    assert len(sources) == 1
    source_node = sources[0]
    assert source_node.op_type == OpType.SOURCE
    assert source_node.config["uri"] == "s3://bucket/data.csv"
    
    # Trace flow
    # Source -> Filter
    filter_node_id = [target for src, target in graph.edges if src == source_node.id][0]
    filter_node = graph.nodes[filter_node_id]
    assert filter_node.op_type == OpType.FILTER
    
    # Filter -> Map
    map_node_id = [target for src, target in graph.edges if src == filter_node.id][0]
    map_node = graph.nodes[map_node_id]
    assert map_node.op_type == OpType.MAP
    
    # Map -> Sink
    sink_node_id = [target for src, target in graph.edges if src == map_node.id][0]
    sink_node = graph.nodes[sink_node_id]
    assert sink_node.op_type == OpType.SINK

def test_branching_logic():
    # Test creating a fork in the graph
    source = Source("root")
    
    path_a = source >> Map(lambda x: x)
    path_b = source >> Filter(lambda x: True)
    
    # Compile one of the paths (they share the graph because they share the source's graph reference)
    # Actually, let's check if they share the graph.
    # Source("root") returns a stream with a new Graph() if not passed.
    # path_a shares that graph.
    # path_b connects to 'source' stream.
    
    # Does 'source' object (SymbolicStream) mutate its internal graph? Yes.
    
    graph = path_a.compile()
    
    assert len(graph.nodes) == 3 # Source, Map, Filter
    assert len(graph.edges) == 2 # Source->Map, Source->Filter
    
    assert path_a.graph is path_b.graph

if __name__ == "__main__":
    test_pipeline_construction()
    test_branching_logic()
    print("--- DSL Logic Tests Passed ---")
