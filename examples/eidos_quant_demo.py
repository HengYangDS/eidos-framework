from eidos import Source, Sink
from eidos.quant import RSI, MACD, BollingerBands

def main():
    """
    Demonstrates a quantitative finance pipeline using Eidos.
    Calculates RSI, MACD, and Bollinger Bands on market data.
    """
    
    # 1. Define the Source
    # Reads parquet file from S3 (or local)
    market_data = Source("s3://market-data/sp500/aapl.parquet")
    
    # 2. Calculate Indicators
    # Eidos handles the windowing and vectorization automatically.
    # Note: In a real scenario, these might be parallelized or fused.
    
    # RSI Strategy
    rsi_signal = (
        market_data 
        >> RSI(window=14, field="close")
    )
    
    # MACD Strategy
    macd_signal = (
        market_data 
        >> MACD(fast=12, slow=26, signal=9, field="close")
    )
    
    # Bollinger Bands
    bb_signal = (
        market_data 
        >> BollingerBands(window=20, std=2, field="close")
    )
    
    # 3. Combine Signals (Ensemble)
    # Logic: Combine all indicators into a single feature set
    # We use the Ensemble operator (&) to run them in parallel logic
    # and then merge the results.
    
    # Wait, we can pipe them sequentially if we want to augment the stream
    # or use & to create a tuple of streams.
    # Ideally, we want to "add columns" to the original stream.
    # The '>>' operator on an indicator usually implies "transform stream".
    # If RSI returns just the RSI column, we lose the original data.
    # The Quant library implementation (indicators.py) defines them as Operators.
    # Let's assume they return the transformed stream (e.g. with_columns in Polars).
    # If they return just the metric, we need to join them.
    
    # For this demo, let's assume we are building a feature set.
    
    features = (
        market_data
        >> RSI(window=14)
        >> MACD(fast=12, slow=26)
        >> BollingerBands(window=20)
    )
    
    # 4. Sink
    pipeline = features >> Sink("db://features_store")
    
    return pipeline

if __name__ == "__main__":
    import eidos
    plan = eidos.run(main())
    print(f"Execution Plan:\n{plan}")
