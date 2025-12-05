import unittest
import json
from unittest.mock import patch, MagicMock
from eidos.intelligence.driver import OpenAIDriver
from eidos.system.sidecar import Sidecar
import asyncio

class TestIntelligenceRealization(unittest.TestCase):
    def setUp(self):
        self.driver = OpenAIDriver(api_key="test-key")

    @patch("urllib.request.urlopen")
    def test_synthesize_code_request(self, mock_urlopen):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "choices": [{"message": {"content": "from eidos import Source\nflow = Source('test')"}}]
        }).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Run async method
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.driver.synthesize_code("create a test flow"))
        
        # Verify
        self.assertEqual(result, "from eidos import Source\nflow = Source('test')")
        
        # Check request
        args, kwargs = mock_urlopen.call_args
        req = args[0]
        self.assertEqual(req.full_url, "https://api.openai.com/v1/chat/completions")
        self.assertEqual(req.headers["Authorization"], "Bearer test-key")
        
        # Check payload
        payload = json.loads(req.data.decode("utf-8"))
        self.assertEqual(payload["model"], "gpt-4o")
        self.assertEqual(payload["messages"][0]["role"], "system")
        self.assertTrue("Eidos DSL" in payload["messages"][0]["content"])

    @patch("urllib.request.urlopen")
    def test_diagnose_error_request(self, mock_urlopen):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "choices": [{"message": {"content": "Fix: use .cast(float)"}}]
        }).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.driver.diagnose_error("traceback...", {"a": 1}))
        
        self.assertEqual(result, "Fix: use .cast(float)")

    def test_sidecar_integration(self):
        # Test that sidecar can use the driver
        sidecar = Sidecar(driver=self.driver)
        
        # Mock the driver's diagnose_error method to avoid network
        async def mock_diagnose(trace, context):
            return f"Diagnosed: {trace[:10]}"
        
        self.driver.diagnose_error = mock_diagnose
        
        try:
            raise ValueError("Test Error")
        except ValueError as e:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            diagnosis = loop.run_until_complete(sidecar.heal(e, None))
            
            self.assertTrue("Diagnosed" in diagnosis)
            # Check if traceback was captured (traceback string starts with "Traceback")
            # but our mock_diagnose returns "Diagnosed: " + first 10 chars.
            # traceback usually starts with "Traceback"
            self.assertTrue("Traceback" in diagnosis or "ValueError" in diagnosis)

if __name__ == "__main__":
    unittest.main()
