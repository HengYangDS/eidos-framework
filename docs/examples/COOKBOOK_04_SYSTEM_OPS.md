# Cookbook IV: System Ops with Eigen

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

This cookbook demonstrates how to build **Resilient Infrastructure** and
**Observability Pipelines** using Eigen.

## Scenario 1: The Circuit Breaker (Thermodynamics)

**Goal**: Protect a fragile service from cascading failure.

### 1.1 The Circuit State Machine

```python
from eigen.core import Operator
from eigen.mechanics import CircuitBreaker, State

# --- 1. The Unstable Service ---
RemoteAPI = HttpSource("https://unstable.api")

# --- 2. The Breaker ---

# If error_rate > 50%, Open circuit for 60s.

# While Open, fail fast (don't call API).

ProtectedService = RemoteAPI | CircuitBreaker(
    threshold=0.5, 
    reset_timeout=60.0,
    fallback=StaticResponse("Service Unavailable")
)

```

This implements a **Phase Transition** (Conductor -> Insulator) based on
Temperature (Error Rate).

## Scenario 2: The Observability Pipeline (Lensing)

**Goal**: Strip PII from logs, sample 1%, and ship to Splunk.

```python

# --- 1. The Lens (Masking) ---
@atom
def RedactPII(log: dict) -> dict:
    log["email"] = "***"
    log["ssn"] = "***"
    return log

# --- 2. The Sampler (Decimator) ---

# Only let 1% of particles through
Sample = RandomFilter(p=0.01)

# --- 3. The Sink ---
Splunk = SplunkSink(host="splunk:8088")

# --- 4. The Sidecar ---

# We attach this pipeline to the main application

# The '@' operator measures the stream without blocking it.

MainApp = BusinessLogic @ (RedactPII >> Sample >> Splunk)

```

## Scenario 3: Chaos Engineering (Quantum Suicide)

**Goal**: Randomly inject latency and errors to test resilience.

```python
from eigen.cosmos import ChaosMonkey

# --- 1. The Chaos Field ---

# Inject 500ms latency with 10% probability

# Inject 500 error with 1% probability
Chaos = ChaosMonkey(latency_p=0.1, error_p=0.01)

# --- 2. The Simulation ---

# We wrap the service in the Chaos Field
with Chaos.context():

    # The service will experience random failures
    RunStressTest(ProtectedService)

```

## Scenario 4: Infrastructure as Code (Eigenform)

**Goal**: Define AWS infrastructure using the Eigen Graph.

```python

# Eigen is substrate-independent.

# We can map operators to Terraform resources.

from eigen.techne.aws import Lambda, SQS, DynamoDB

# --- 1. Define Logic ---
Process = Lambda(handler="main.handler")
Queue   = SQS(name="jobs")
Table   = DynamoDB(name="results")

# --- 2. Define Topology ---

# Queue triggers Lambda, Lambda writes to Table
Infra = Queue >> Process >> Table

# --- 3. Synthesis ---

# Generate Terraform JSON
Terraform.synthesize(Infra)

```

## Scenario 5: Auto-Scaling (Renormalization)

**Goal**: Automatically increase worker count based on queue depth.

```python

# --- 1. The Controller ---

# Read Queue Depth (Metric)

# Calculate desired replicas (Control Theory)

# Apply Scaling (Actuator)

def ScalePolicy(depth):
    return min(100, max(1, depth // 100))

AutoScaler = (
    MetricSource("queue_depth") 
    >> Map(ScalePolicy) 
    >> K8sScale("worker-deployment")
)

# Run every 10 seconds
Daemon = Timer(10.0) >> AutoScaler

```

---
**Eigen Cosmology** | [Previous: Cookbook III](COOKBOOK_03_NEURAL_PHYSICS.md) | [Index](../00_INDEX.md) | [Next: Cookbook V](COOKBOOK_05_DISTRIBUTED.md) | *© 2025 The Eigen High Council*
