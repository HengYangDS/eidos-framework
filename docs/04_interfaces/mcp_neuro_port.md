# MCP: The Neuro-Interface

Eidos implements the **Model Context Protocol (MCP)** to function as a native extension of Large Language Models (LLMs).

## 1. The Concept

Instead of using a "Chat with Data" wrapper, Eidos exposes itself as a set of **Tools** to the LLM. The LLM uses these tools to inspect, compile, and execute logic.

## 2. Auto-Registration

Any Eidos pipeline can be exposed as an MCP tool with a single decorator.

```python
@eos.mcp_tool(
    name="analyze_stock",
    description="Calculates RSI and MACD for a given ticker symbol."
)
def analyze_stock_pipeline(ticker: str, window: int = 14):
    return (
        Source(f"s3://market/{ticker}")
        >> QuantOps(window)
        >> Sink("memory")
    )
```

When the MCP Server starts, this function is registered in the MCP capability manifest. Claude/GPT sees a tool named `analyze_stock` with arguments `ticker` and `window`.

## 3. Semantic Routing

Eidos includes a **Semantic Router** that maps natural language queries to pipelines.

*   **User**: "Show me the volatility of AAPL."
*   **Router**: Vector search matches "volatility" to `VolatilityPipeline`.
*   **Execution**: The pipeline is JIT-compiled and executed.
*   **Response**: The result (Arrow Table) is formatted as Markdown or JSON for the LLM.

## 4. Safety

The MCP Port includes a **Sandbox**.
*   **Read-Only Mode**: Prevents LLMs from executing `Sink` operators that overwrite data.
*   **Quota**: Limits CPU/RAM usage per LLM request.
