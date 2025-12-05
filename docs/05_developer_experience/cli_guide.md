# Eidos CLI: The Command Line Interface

The `eidos` command is your primary tool for managing the Logic Operating System.

## 1. Project Management

```bash
# Create a new project
eidos create my-project

# Structure:
# my-project/
#   src/
#     main.py
#   tests/
```

## 2. Execution

```bash
# Run a pipeline locally (Vector Lane / Free Lane)
eidos run src/main.py

# Run on a remote cluster (Cluster Lane)
eidos run src/main.py --cluster ray://192.168.1.100:6379

# Enable verbose logging (Debug Mode)
eidos run src/main.py --verbose
```

## 3. Visualization (Web Studio)

Launch the **Visual Cortex** to inspect your topology.

```bash
# Start the Studio server
eidos studio src/main.py --port 8888

# Open http://localhost:8888 to see the Graph
```

## 4. Deployment (Production)

Generate production artifacts (Docker) for your pipeline.

```bash
# Generate Dockerfile and docker-compose.yml
eidos deploy src/main.py --port 8000

# Build and Run
docker compose up --build
```

## 5. Microservices (REST)

Serve your pipeline as an HTTP API instantly.

```bash
# Serve functions decorated with @expose
eidos serve src/main.py --port 8080
```
