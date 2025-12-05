import pytest
from syrupy import SnapshotAssertion
from eidos import Source, Map, Filter, Sink
from eidos.zero.compiler import Compiler

def test_pipeline_snapshot(snapshot: SnapshotAssertion):
    """
    Verifies that the compiled IR remains stable using Syrupy snapshots.
    """
    flow = (
        Source("csv://data.csv")
        >> Filter(lambda x: x['value'] > 0)
        >> Map(lambda x: x * 2)
        >> Sink("s3://output")
    )
    
    graph = flow.compile()
    ir = Compiler.compile(graph, target="string")
    
    # The lambdas might have different addresses or names like <lambda>
    # but usually just <lambda>.
    # If lambda names are unstable, we might need to name functions.
    
    assert ir == snapshot
    
def test_complex_topology_snapshot(snapshot: SnapshotAssertion):
    s1 = Source("A")
    s2 = Source("B")
    
    # Choice
    flow = (s1 | s2) >> Sink("out")
    
    graph = flow.compile()
    ir = Compiler.compile(graph, target="string")
    
    assert ir == snapshot
