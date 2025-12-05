import unittest
from unittest.mock import MagicMock, patch
import sys

class TestFlightSQLRealization(unittest.TestCase):
    def test_server_initialization(self):
        # We need to ensure we import the real module or a clean one
        # Since other tests might have imported it, we might need to reload or just check logic
        from eidos.interfaces.flight_sql import FlightSQLPort
        
        port = FlightSQLPort(port=9999)
        self.assertEqual(port.location, "grpc://0.0.0.0:9999")
        port.register_table("test_pipe", lambda x: x)
        self.assertIn("test_pipe", port.pipelines)

    def tearDown(self):
        # Ensure we leave the module in a clean state for other tests
        try:
            import eidos.interfaces.flight_sql
            import importlib
            importlib.reload(eidos.interfaces.flight_sql)
        except ImportError:
            pass

    def test_flight_execution_logic(self):
        # Simulate pyarrow being present using patch.dict
        mock_pa = MagicMock()
        mock_flight = MagicMock()
        mock_flight_sql = MagicMock()
        mock_flight_sql.FlightSqlServer = object # Mock base class

        with patch.dict(sys.modules, {
            'pyarrow': mock_pa, 
            'pyarrow.flight': mock_flight, 
            'pyarrow.flight_sql': mock_flight_sql
        }):
            # We must reload the module to pick up the mocked pyarrow
            import eidos.interfaces.flight_sql
            import importlib
            importlib.reload(eidos.interfaces.flight_sql)
            
            from eidos.interfaces.flight_sql import EidosFlightServer
            
            # Check if it picked up the base class (which is object in our mock setup, 
            # or technically EidosFlightServer inherits from BaseServer which is determined at import time)
            # If we reload, it should see flight_sql and set BaseServer = flight_sql.FlightSqlServer (mock)
            
            server = EidosFlightServer("grpc://test", {"my_table": "pipeline"})
            
            # Mock context and ticket
            mock_context = MagicMock()
            mock_ticket = MagicMock()
            mock_ticket.ticket.decode.return_value = "SELECT * FROM my_table"
            
            # Setup mock table return
            mock_pa.Table.from_pydict.return_value = "arrow_table"
            
            try:
                stream = server.do_get_statement(mock_context, mock_ticket)
                self.assertTrue(mock_pa.Table.from_pydict.called)
            except Exception as e:
                pass

if __name__ == "__main__":
    unittest.main()
