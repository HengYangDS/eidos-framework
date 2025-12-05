from eidos import Source, Sink
from eidos.quant import RSI, MACD, BollingerBands

def main():
    """
    Demonstrates a quantitative finance pipeline using Eidos.
    Calculates RSI, MACD, and Bollinger Bands on market data.
    """
    
    # 1. Define the Source
    # Reads local CSV
    market_data = Source("csv://examples/market_data.csv")
    
    # 2. Calculate Indicators
    
    # We build a sequential pipeline that adds features
    features = (
        market_data
        >> RSI(window=14, field="close")
        >> MACD(fast=12, slow=26, signal=9, field="close")
        >> BollingerBands(window=20, std=2, field="close")
    )
    
    # 3. Sink to Console to verify output
    pipeline = features >> Sink("console")
    
    return pipeline

if __name__ == "__main__":
    import eidos
    print("Running Quant Demo...")
    # This will default to "python" backend if Polars is missing
    res = eidos.run(main())
    
    if callable(res):
        print("Executing...")
        res()
