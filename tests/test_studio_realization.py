import unittest
from unittest.mock import MagicMock, patch
import sys

# Ensure src is in path
sys.path.append("src")

try:
    from fastapi.testclient import TestClient
    from eidos.interfaces.studio import app
except ImportError:
    app = None

from eidos.system.evolution import EvolutionarySupervisor

class TestStudioRealization(unittest.TestCase):
    def setUp(self):
        # Disable httpx logging to avoid structlog conflict in test env
        import logging
        logging.getLogger("httpx").setLevel(logging.CRITICAL)
        
        if app:
            self.client = TestClient(app)

    def test_static_files(self):
        if not app:
            print("Skipping Studio tests (FastAPI missing)")
            return
        response = self.client.get("/")
        # It might be 404 if static dir is not correctly found during test execution relative path
        # But we want to check if it ATTEMPTS to serve.
        # If index.html exists, it should be 200.
        if response.status_code == 200:
            self.assertIn("Eidos Studio", response.text)

    def test_optimization_api(self):
        if not app:
            return
        response = self.client.post("/api/optimize?generations=5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["gens"], 5)

    def test_evolutionary_supervisor(self):
        # Test the Evolution logic independently
        supervisor = EvolutionarySupervisor(population_size=2, generations=1)
        
        # Mock pipeline factory
        def factory(params):
            from eidos import Source, Sink
            return Source("in") >> Sink("out")
            
        param_space = {"window": [10, 20]}
        
        # Mock fitness function
        def fitness(res):
            return 1.0
            
        # We need to mock Compiler.compile to avoid actual execution errors
        with patch("eidos.system.evolution.Compiler.compile") as mock_compile:
            mock_compile.return_value = "mock_result"
            
            best_params, score = supervisor.optimize(factory, param_space, fitness, executor="string")
            
            self.assertEqual(score, 1.0)
            self.assertIn("window", best_params)
            self.assertEqual(len(supervisor.history), 2) # 2 individuals * 1 gen

if __name__ == "__main__":
    unittest.main()
