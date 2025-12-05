import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import json
import asyncio

# Ensure src is in path
sys.path.append("src")

from eidos import Source, Map, Sink, expose
from eidos.interfaces.rest import RestPort

# Mock module content
@expose(route="/predict", method="POST")
def predict(payload):
    return Source.from_payload(payload) >> Map(lambda x: {"res": x["val"] * 2})

class TestRestRealization(unittest.TestCase):
    @patch("uvicorn.run")
    def test_server_startup(self, mock_run):
        try:
            port = RestPort()
            port.run()
            mock_run.assert_called_once()
        except ImportError:
            print("Skipping test_server_startup because dependencies are missing")

    def test_route_registration(self):
        try:
            port = RestPort()
        except ImportError:
            print("Skipping test_route_registration")
            return

        # Manually register the function
        port._register_route(predict)
        
        # Check if route exists in FastAPI app
        routes = [r for r in port.app.routes if getattr(r, "path", "") == "/predict"]
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].methods, {"POST"})

    @patch("eidos.zero.compiler.Compiler.compile")
    def test_endpoint_execution(self, mock_compile):
        try:
            import polars as pl
        except ImportError:
            print("Skipping test_endpoint_execution because Polars is missing")
            return
            
        # Mock compiler to return a Polars DataFrame result
        mock_compile.return_value = pl.DataFrame({"res": [4]})
        
        try:
            port = RestPort()
        except ImportError:
            return

        port._register_route(predict)
        
        # Find the endpoint function
        route = [r for r in port.app.routes if getattr(r, "path", "") == "/predict"][0]
        endpoint = route.endpoint
        
        # Simulate Request
        mock_request = MagicMock()
        mock_request.json = AsyncMock(return_value={"val": 2})
        
        # Run async endpoint
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(endpoint(mock_request))
        
        # Verify response
        body = json.loads(response.body)
        self.assertEqual(body, [{"res": 4}])
        
        loop.close()

if __name__ == "__main__":
    unittest.main()
