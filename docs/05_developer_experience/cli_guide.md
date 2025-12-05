# Eidos CLI: The Command Line Interface

The `eidos` command is your primary tool for managing the OS.

## 1. Project Management

```bash
# Create a new project from a template
eidos create my-project --template quant-strategy

# Initialize in current directory
eidos init
```

## 2. Running

```bash
# Run a pipeline locally (Vector Lane)
eidos run src/main.py

# Run on a remote cluster (Cluster Lane)
eidos run src/main.py --cluster ray://192.168.1.100:6379
```

## 3. Deployment

```bash
# Deploy to production (starts a daemon)
eidos deploy src/main.py --name alpha-v1

# List running pipelines
eidos list
```

## 4. Natural Language

```bash
# Ask the OS to do something
eidos ask "Analyze the trade logs in s3://logs and find top errors"
```
