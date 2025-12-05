# Integration Guides

## 1. DolphinDB Integration

Eidos supports **Compute Pushdown** to DolphinDB.

### 1.1 Setup
```bash
pip install eidos-os[dolphindb]
```

### 1.2 Usage
```python
source = Source("dolphindb://admin:123@192.168.1.10:8848/dfs/trades")
# This filter runs inside DolphinDB
flow = source >> Filter(price > 100)
```

## 2. Prefect / Dagster Integration

Eidos can be compiled into a Prefect Flow.

```python
from eidos.transpilers import to_prefect

flow = Source() >> Map() >> Sink()
prefect_flow = to_prefect(flow)
```
