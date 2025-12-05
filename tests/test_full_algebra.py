from eidos.zero.symbolism.dsl import Source, Map, Filter, Sink, SymbolicStream
from eidos.zero.symbolism.ast import OpType

def test_full_algebra():
    print("\n--- Testing Full Algebra ---")
    
    s1 = Source("src1")
    s2 = Source("src2")
    
    # Test Choice (|)
    op_choice = Map(lambda x: x) | Filter(lambda x: True)
    flow_choice = s1 >> op_choice
    graph_choice = flow_choice.compile()
    print(f"[Choice] Nodes: {len(graph_choice.nodes)}")
    
    choice_node = [n for n in graph_choice.nodes.values() if n.op_type == OpType.CHOICE][0]
    assert choice_node.config["left"]["type"] == "Map"
    assert choice_node.config["right"]["type"] == "Filter"
    print("  Choice Operator: OK")

    # Test Ensemble (&)
    op_ensemble = Map(lambda x: x) & Map(lambda x: x*2)
    flow_ensemble = s1 >> op_ensemble
    graph_ensemble = flow_ensemble.compile()
    
    ensemble_node = [n for n in graph_ensemble.nodes.values() if n.op_type == OpType.ENSEMBLE][0]
    assert ensemble_node.config["left"]["type"] == "Map"
    assert ensemble_node.config["right"]["type"] == "Map"
    print("  Ensemble Operator: OK")

    # Test Chain (>>)
    op_chain = Map(lambda x: x) >> Filter(lambda x: True)
    # s1 >> (Map >> Filter) should result in s1 -> Map -> Filter
    flow_chain = s1 >> op_chain
    graph_chain = flow_chain.compile()
    
    # In the graph, we should see Source -> Map -> Filter
    # Not a "ChainNode". ChainOperator.bind unwraps itself.
    nodes = list(graph_chain.nodes.values())
    types = [n.op_type for n in nodes]
    print(f"[Chain] Types: {types}")
    assert OpType.MAP in types
    assert OpType.FILTER in types
    # Verify edges
    # Source -> Map
    # Map -> Filter
    print("  Chain Operator: OK")

    # Test Interference (+)
    # s1 + s2 -> Merge
    flow_merge = s1 + s2
    graph_merge = flow_merge.compile()
    merge_node = [n for n in graph_merge.nodes.values() if n.op_type == OpType.MERGE][0]
    assert len(merge_node.parents) == 2
    print("  Interference (Merge): OK")

    print("--- All Algebra Tests Passed ---")

if __name__ == "__main__":
    test_full_algebra()
