from eidos import Source, Map, Sink
from eidos.zero.compiler import Compiler
from eidos.system.governance import LineageRegistry
from eidos.system.fs import FS
from eidos.interfaces.mcp import MCPPort

def test_eidos_os_full_stack():
    print("\n--- [Eidos] Integration Test ---")
    
    # 1. Define Logic (User Space)
    print("1. Defining User Logic...")
    def normalize(x): return x.lower()
    
    flow = (
        Source("s3://raw/logs.txt")
        >> Map(normalize)
        >> Sink("db://clean_logs")
    )
    
    # 2. Compile to Graph (Kernel Space - Frontend)
    graph = flow.compile()
    print(f"   Graph built with {len(graph.nodes)} nodes.")
    
    # 3. Governance Check (System Space)
    print("2. Extracting Lineage (System)...")
    lineage = LineageRegistry.extract_lineage(graph)
    sources = [s['config'] for s in lineage['sources']]
    sinks = [s['config'] for s in lineage['sinks']]
    print(f"   Sources: {sources}")
    print(f"   Sinks: {sinks}")
    
    assert "s3://raw/logs.txt" in str(sources)
    
    # 4. Register with Neuro-Interface (Interface Space)
    print("3. Registering with MCP (Interface)...")
    mcp = MCPPort("Eidos-Agent")
    
    # Simulate wrapping the flow in a callable tool
    def pipeline_tool():
        return flow
        
    mcp.register_pipeline("clean_logs_tool", pipeline_tool)
    mcp.run()
    
    # 5. Transpile to Execution Plan (Kernel Space - Backend)
    print("4. Transpiling to Physical Plan (Kernel)...")
    plan = Compiler.compile(graph, target="string")
    print(f"   Physical Plan: {plan}")
    
    assert "Scan(s3://raw/logs.txt)" in plan
    
    print("--- [Eidos] Test Passed ---")

if __name__ == "__main__":
    test_eidos_os_full_stack()
