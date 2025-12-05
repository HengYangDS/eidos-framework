from eidos import Source, Map, Filter, Sink
from eidos.quant.indicators import RSI, MACD

def main():
    # A complex topology to show off the visualizer
    
    market_data = Source("s3://market-data/btc-usd.parquet")
    
    # Branch 1: Momentum
    momentum = (
        market_data 
        >> RSI(window=14)
        >> Filter(lambda x: x['rsi'] < 30)
    )
    
    # Branch 2: Trend
    trend = (
        market_data
        >> MACD(fast=12, slow=26)
        >> Filter(lambda x: x['macd'] > 0)
    )
    
    # Ensemble (Parallel execution)
    # We want to fire if BOTH Momentum (Oversold) AND Trend (Bullish) are true
    # Or maybe we use Choice as a "Try this, else that"
    
    # Let's show a Choice (Fallback) pattern
    # Try getting data from primary, if fail (empty), try secondary
    # For logic, let's say: Strategy A | Strategy B
    
    strategy = (momentum & trend) >> Map(lambda x: {"signal": "BUY", "confidence": "HIGH"})
    
    fallback = Source("backup") >> Map(lambda x: {"signal": "HOLD"})
    
    # Final Flow: Strategy | Fallback
    flow = (strategy | fallback) >> Sink("kafka://signals")
    
    return flow

if __name__ == "__main__":
    from eidos import run
    run(main())
