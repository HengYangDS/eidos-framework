# Rest Port: The App Interface

## 1. API as a Side Effect

In Eidos, you don't write Flask/FastAPI code. You simply expose a pipeline.

```python
@eos.expose(route="/api/v1/predict", method="POST")
def prediction_pipeline(payload: dict):
    return (
        Source.from_payload(payload)
        >> FeatureEng()
        >> ModelInference()
        >> Sink.to_response()
    )
```

## 2. Features

*   **OpenAPI Generation**: Automatically generates `openapi.json` from Pydantic schemas.
*   **Async**: Built on `uvicorn`, fully compatible with Python `asyncio`.
*   **Streaming**: Supports `Server-Sent Events (SSE)` for streaming pipelines.
