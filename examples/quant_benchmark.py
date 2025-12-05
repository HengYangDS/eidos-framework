from eidos import Source, Sink
from eidos.quant.indicators import (
    SMA, EMA, WMA, RSI, MACD, BollingerBands, Stoch, CCI, ATR, ADX, OBV, VWAP
)
import eidos
import sys

def main():
    print("--- Constructing Quantitative Strategy ---")
    
    # A pipeline with EVERYTHING
    # market_data.csv now contains close, high, low, volume
    flow = (
        Source("csv://examples/market_data.csv")
        >> SMA(window=5, field="close")
        >> EMA(window=5, field="close")
        >> WMA(window=5, field="close")
        >> RSI(window=14, field="close")
        >> MACD(fast=12, slow=26, signal=9, field="close")
        >> BollingerBands(window=20, std=2, field="close")
        >> Stoch(window=14, smooth=3)
        >> CCI(window=14)
        >> ATR(window=14)
        >> ADX(window=14)
        >> OBV(field_close="close", field_vol="volume")
        >> VWAP(field_price="close", field_vol="volume")
        >> Sink("collect")
    )
    
    print("--- Compiling to Polars (Vector Lane) ---")
    try:
        res = eidos.run(flow, engine="polars")
        # Polars backend sink returns a callable that returns the result
        df = res()
            
        print(f"Polars Result Type: {type(df)}")
        if hasattr(df, "shape"):
            print(f"Polars Result Shape: {df.shape}")
            # Print columns to verify all indicators are present
            print(f"Columns: {df.columns}")
            print(df.tail(1))
        else:
            print(f"Polars Result: {df}")

    except Exception as e:
        print(f"Polars Failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n--- Compiling to Python (Free Lane) ---")
    try:
        gen = eidos.run(flow, engine="python")
        res = gen() # Execute sink
        print(f"Python Result Count: {len(res)}")
        if res:
            print("Keys:", list(res[-1].keys()))
    except Exception as e:
        print(f"Python Failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n--- Compiling to DolphinDB (Pushdown Lane) ---")
    try:
        from eidos.zero.compiler import Compiler
        script = Compiler.compile(flow.compile(), target="dolphindb")
        print("Generated Script (Tail):")
        print("\n".join(str(script).split("\n")[-5:]))
    except Exception as e:
        print(f"DolphinDB Failed: {e}")

if __name__ == "__main__":
    main()
