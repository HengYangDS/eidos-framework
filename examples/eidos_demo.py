import asyncio
from eidos import Source, Map, Filter, Sink, SymbolicStream
from eidos.zero.compiler import Compiler
from eidos.system.governance import LineageRegistry
from eidos.interfaces.mcp import MCPPort

def main():
    print("=== Eidos v1.0 Demo ===")
    print("Code is Topology. Execution is Physis.\n")

    # --- 1. User Space: Defining Logic (Symbolism) ---
    print("[User] Defining logical topology...")
    
    def to_upper(x):
        return x.upper()
    
    def is_error(x):
        return "ERROR" in x

    # The DSL builds an AST in memory (Lazy Evaluation)
    flow: SymbolicStream = (
        Source("s3://app-logs/server.log")
        >> Filter(is_error)
        >> Map(to_upper)
        >> Sink("db://alerts")
    )
    
    # Compile to get the Graph object
    graph = flow.compile()
    print(f"[Kernel] AST captured. Nodes: {len(graph.nodes)}")

    # --- 2. System Space: Governance (Registry) ---
    print("\n[System] Auto-registering lineage...")
    lineage = LineageRegistry.extract_lineage(graph)
    print(f"   Lineage Source: {lineage['sources'][0]['config']}")
    print(f"   Lineage Sink:   {lineage['sinks'][0]['config']}")

    # --- 3. Interface Space: Neuro-Interface (MCP) ---
    print("\n[Interface] Exposing to MCP (Neuro-Interface)...")
    mcp = MCPPort("Eidos-Neuro-Port")
    mcp.register_pipeline("analyze_logs", lambda: flow)
    mcp.run()

    # --- 4. Physical Space: Execution (Dynamics) ---
    print("\n[Kernel] Transpiling to Physical Plan...")
    # In a real scenario, target="polars" or "ray"
    plan = Compiler.compile(graph, target="string")
    print(f"   Physical Plan: {plan}")
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    main()
