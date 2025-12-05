import unittest
from unittest.mock import patch, MagicMock
from eidos.zero.compiler import Compiler
from eidos import Source, Sink

class MockBackend:
    def compile_node(self, node, inputs):
        return f"Mock({node.op_type})"

class TestPluginSystem(unittest.TestCase):
    @patch("importlib.metadata.entry_points")
    def test_plugin_discovery(self, mock_entry_points):
        # Setup mock entry point
        mock_ep = MagicMock()
        mock_ep.name = "my-plugin"
        mock_ep.load.return_value = MockBackend
        
        # In Python 3.10+, entry_points(group=...) returns a list of EntryPoints
        mock_entry_points.return_value = [mock_ep]
        
        # Define a simple flow
        flow = Source("src") >> Sink("dst")
        graph = flow.compile()
        
        # Compile targeting the plugin
        result = Compiler.compile(graph, target="my-plugin")
        
        # Verify result came from MockBackend
        self.assertIn("Mock", str(result))
        self.assertTrue(mock_ep.load.called)
        
        # Verify group call
        mock_entry_points.assert_called_with(group="eidos.backends")

if __name__ == "__main__":
    unittest.main()
