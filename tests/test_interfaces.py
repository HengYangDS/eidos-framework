import asyncio
import unittest
from unittest.mock import MagicMock
from eidos.interfaces.mcp import MCPPort
from eidos import Source, Sink
from eidos.intelligence.driver import CognitiveDriver

class MockDriver:
    async def compute_embedding(self, text):
        # Simple determinisic hash for testing routing
        # "volatility" -> [1, 0]
        # "trend" -> [0, 1]
        val = text[0].lower()
        if "volatility" in val:
            return [[1.0, 0.0]]
        elif "trend" in val:
            return [[0.0, 1.0]]
        return [[0.5, 0.5]]
    
    async def synthesize_code(self, intent, context=None):
        return ""
        
    async def diagnose_error(self, error, data):
        return ""

class TestInterfaces(unittest.TestCase):
    def test_mcp_routing(self):
        print("\n--- Testing MCP Semantic Routing ---")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        driver = MockDriver()
        port = MCPPort("test_mcp", driver=driver)
        
        def dummy_pipeline():
            return Source("A") >> Sink("B")
        
        # Use run_until_complete for async methods
        loop.run_until_complete(port.register_pipeline("analyze_volatility", dummy_pipeline, description="Calculate volatility of a stock"))
        loop.run_until_complete(port.register_pipeline("show_trend", dummy_pipeline, description="Show market trend"))
        
        # Test routing
        tool = loop.run_until_complete(port.handle_query("I want to see the volatility of AAPL"))
        self.assertIsNotNone(tool)
        self.assertEqual(tool["name"], "analyze_volatility")
        
        tool2 = loop.run_until_complete(port.handle_query("What is the trend?"))
        self.assertIsNotNone(tool2)
        self.assertEqual(tool2["name"], "show_trend")
        
        loop.close()
        print("--- MCP Routing OK ---")

    def test_flight_sql_mock(self):
        print("\n--- Testing FlightSQL Mock ---")
        from eidos.interfaces.flight_sql import FlightSQLPort
        port = FlightSQLPort()
        port.register_table("my_table", None)
        port.run(background=True) # Should verify pyarrow check without crashing
        port.stop()
        print("--- FlightSQL Mock OK ---")

if __name__ == "__main__":
    unittest.main()
