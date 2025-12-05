from eidos.interfaces.mcp import MCPPort
from eidos import Source, Sink

def test_mcp_routing():
    print("\n--- Testing MCP Semantic Routing ---")
    port = MCPPort("test_mcp")
    
    def dummy_pipeline():
        return Source("A") >> Sink("B")
    
    port.register_pipeline("analyze_volatility", dummy_pipeline, description="Calculate volatility of a stock")
    port.register_pipeline("show_trend", dummy_pipeline, description="Show market trend")
    
    # Test routing
    tool = port.handle_query("I want to see the volatility of AAPL")
    assert tool is not None
    assert tool["name"] == "analyze_volatility"
    
    tool2 = port.handle_query("What is the trend?")
    assert tool2 is not None
    assert tool2["name"] == "show_trend"
    
    print("--- MCP Routing OK ---")

def test_flight_sql_mock():
    print("\n--- Testing FlightSQL Mock ---")
    from eidos.interfaces.flight_sql import FlightSQLPort
    port = FlightSQLPort()
    port.register_table("my_table", None)
    port.run() # Should verify pyarrow check without crashing
    print("--- FlightSQL Mock OK ---")

if __name__ == "__main__":
    test_mcp_routing()
    test_flight_sql_mock()
