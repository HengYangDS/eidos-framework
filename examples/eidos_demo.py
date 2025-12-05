from eidos import Source, Map, Filter, Sink

def main():
    print("=== Eidos Hello World ===")
    
    # A simple pipeline using the provided market data
    flow = (
        Source("csv://examples/market_data.csv")
        >> Filter(lambda x: float(x["close"]) > 105.0)
        >> Map(lambda x: {**x, "value": float(x["close"]) * float(x["volume"])})
        >> Sink("console")
    )
    
    return flow

if __name__ == "__main__":
    import eidos
    # This will use Python Native Backend if Polars is missing
    executable = eidos.run(main())
    
    if callable(executable):
        executable()
    else:
        print(executable)
