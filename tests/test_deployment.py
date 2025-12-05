import unittest
from eidos.system.deployment import generate_dockerfile, generate_compose

class TestDeployment(unittest.TestCase):
    def test_generate_dockerfile(self):
        dockerfile = generate_dockerfile("src/main.py", port=9090)
        
        self.assertIn("FROM python:3.12-slim", dockerfile)
        self.assertIn("CMD [\"eidos\", \"run\", \"src/main.py\"]", dockerfile)
        self.assertIn("EXPOSE 9090", dockerfile)
        self.assertIn("pip install eidos-framework", dockerfile)

    def test_generate_compose(self):
        compose = generate_compose("my-project", "src/app.py", port=5000)
        
        self.assertIn("version: '3.8'", compose)
        self.assertIn("container_name: my-project", compose)
        self.assertIn("5000:5000", compose)
        self.assertIn("command: eidos run src/app.py", compose)
        self.assertIn("EIDOS_DEFAULT_BACKEND=polars", compose)

if __name__ == "__main__":
    unittest.main()
