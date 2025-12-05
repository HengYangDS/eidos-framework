# Cookbook V: Distributed Systems with Eigen

**Author**: HENG Yang <hengyang.2003@tsinghua.org.cn>

This cookbook demonstrates how to build **Distributed Systems** (MapReduce,
Parameter Servers, Consensus) using Eigen's Entanglement primitives.

## Scenario 1: MapReduce (Tensor Contraction)

**Goal**: Count words in a massive dataset distributed across N nodes.

### 1.1 The Topology

```python
from eigen.operators import Map, Reduce, Entangle
from eigen.techne import Shard

# --- 1. The Mapper (Local) ---
@atom
def CountWords(text: str) -> dict[str, int]:
    counts = defaultdict(int)
    for word in text.split():
        counts[word] += 1
    return counts

# --- 2. The Reducer (Global) ---
@atom
def MergeCounts(c1: dict, c2: dict) -> dict:
    for k, v in c2.items():
        c1[k] += v
    return c1

# --- 3. The Cluster ---

# We have 3 Shards (Partitions)
Shards = [Shard(f"data_{i}.txt") for i in range(3)]

# --- 4. The Algebra ---

# (M1 & M2 & M3) >> Reduce
Job = Entangle(*[s >> CountWords for s in Shards]) >> Reduce(MergeCounts)

```

## Scenario 2: The Parameter Server (Holography)

**Goal**: Train a model where workers push gradients to a central server.

```python

# --- 1. The Parameter Server (State) ---

# The 'Higgs Field' that gives mass (weights) to the model.
Weights = State(initial=zeros(1000))

# --- 2. The Worker (Gradient Calculation) ---
@atom
def CalcGrad(batch, weights):

    # Forward + Backward
    return grad(loss)(weights, batch)

# --- 3. The Training Step ---

# 1. Pull Weights

# 2. Calc Grad

# 3. Push Update

def Step(batch):
    w = Weights.read()
    g = CalcGrad(batch, w)
    Weights.update(lambda w: w - lr * g)

# --- 4. Distributed Execution ---

# Run Step on 10 workers in parallel
Cluster = Distribute(Step, workers=10)

```

## Scenario 3: Federated Learning (Privacy)

**Goal**: Train on user devices without moving data.

```python

# --- 1. Local Training (Edge) ---

# Happens on the phone
LocalTrain = (
    LocalData 
    >> TrainEpoch(GlobalModel) 
    >> EncryptUpdate
)

# --- 2. Aggregation (Cloud) ---

# Secure Aggregation of updates
GlobalUpdate = (
    Wait(n=1000) # Wait for 1000 devices
    >> DecryptAndAverage
    >> UpdateGlobalModel
)

# --- 3. The Cycle ---
Federation = Broadcast(GlobalModel) >> LocalTrain >> GlobalUpdate

```

## Scenario 4: Distributed Consensus (Raft)

**Goal**: Implement Leader Election using Eigen operators.

```python

# --- 1. The Node State ---
class Node(State):
    role: str = "FOLLOWER"
    term: int = 0

# --- 2. The Heartbeat (Metronome) ---

# If no heartbeat received, start election
Timeout = Timer(random(150, 300)) >> TriggerElection

# --- 3. The Election (Voting) ---
@atom
async def TriggerElection():
    Node.role = "CANDIDATE"
    Node.term += 1

    # Broadcast VoteRequest to all peers
    votes = await (Peer1.RequestVote() & Peer2.RequestVote())
    if count(votes) > QUORUM:
        Node.role = "LEADER"
        StartHeartbeat()

# --- 4. The Protocol ---
Raft = HeartbeatReceiver | Timeout

```

## Scenario 5: Ray Integration (Techne)

**Goal**: Compile Eigen graph to run on a Ray cluster.

```python
from eigen.techne.ray import RayCompiler

# Define Logic
Pipeline = Source >> Map(HeavyCompute) >> Sink

# Compile to Ray

# This deploys Actors and Objects to the Ray cluster
Job = RayCompiler.compile(Pipeline)

# Execute
Job.submit()

```

---
**Eigen Cosmology** | [Previous: Cookbook IV](COOKBOOK_04_SYSTEM_OPS.md) | [Index](../00_INDEX.md) | [Next: Cookbook VI](COOKBOOK_06_IOT_SMART_CITIES.md) | *© 2025 The Eigen High Council*
