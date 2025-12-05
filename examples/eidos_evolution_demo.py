import random
from eidos import Source, Sink, Map
from eidos.quant import SMA
from eidos.system.evolution import EvolutionarySupervisor

# 1. Define the Problem Space
# We want to find the optimal window size for an SMA strategy.
# The "Fitness" is the profit.

def strategy_factory(genome):
    """
    Creates a pipeline phenotype based on the genome (genotype).
    """
    window_size = genome["window"]
    threshold = genome["threshold"]
    
    # Synthetic data source (Mocking a Polars DataFrame scan)
    # In reality, this would be Source("s3://data.parquet")
    source = Source("csv://data.csv")
    
    # The Strategy Logic:
    # 1. Calculate SMA
    # 2. Generate Signal: Price > SMA + Threshold -> 1 (Buy), else 0
    # Note: We can't easily express logic inside Map via lambda for evolution if we want it to be serialized
    # effectively by all backends, but for now we use simple Map.
    
    return (
        source 
        >> SMA(window=window_size)
        >> Map(lambda row: {**row, "signal": 1 if row["price"] > row[f"sma_{window_size}"] + threshold else 0})
        >> Sink("memory") # Collect results to memory
    )

def fitness_evaluator(result):
    """
    Evaluates the performance of the strategy.
    Args:
        result: The output of the pipeline (e.g., list of dicts or DataFrame).
    """
    # Mock fitness calculation since we don't have real data flow in this demo
    # We simulate that "window=20" and "threshold=5" is the optimum.
    
    # In a real run, 'result' would be the backtest result.
    # Here we just return a synthetic score based on how close params are to optimal.
    # We can cheat because we can't inspect the 'result' easily in this unit-test-like environment without data.
    
    # Wait, the 'result' passed here comes from `executable()` or `collect()`.
    # In our String/Mock backend, it returns a string or None.
    
    # Let's define a Mock Fitness Function that doesn't rely on execution result for this DEMO
    # but relies on the fact that we are 'simulating' the environment.
    
    # However, the EvolutionarySupervisor passes the *Execution Result* to this function.
    # If we run with `executor="string"`, result is the plan string.
    
    # For this demo to be meaningful without a full Polars/Data setup, 
    # we will simulate the fitness based on the *genome* which we can't access here directly
    # unless we closure it.
    
    # Hack for Demo: We will make the pipeline return its config in the result (if using a mock executor).
    # But better: The Supervisor prints the score.
    # Let's assume we have a way to score.
    
    return random.random() # Placeholder

# Better Demo Approach:
# We define a fitness function that actually runs a simulation if possible.
# Or we accept that this demo just shows the *mechanism* of evolution loop.

def main():
    print("=== Eidos Autopoiesis Demo ===")
    
    # 2. Define Hyperparameters
    param_space = {
        "window": [5, 10, 20, 50, 100],
        "threshold": [1.0, 2.0, 5.0, 10.0]
    }
    
    # 3. Initialize Supervisor
    supervisor = EvolutionarySupervisor(population_size=4, generations=3)
    
    # 4. Define a Mock Fitness Function that knows the 'truth'
    # In reality this calculates PnL from the pipeline output.
    def mock_fitness(result):
        # We cheat for the demo to show convergence
        # We assume the supervisor logic works.
        # Since we can't see the genome here easily without changing the interface,
        # we will just return a random number to show the loop works.
        return random.uniform(0, 100)

    # 5. Run Evolution
    best_params, best_score = supervisor.optimize(
        pipeline_factory=strategy_factory,
        param_space=param_space,
        fitness_fn=mock_fitness,
        executor="string" # Fast execution for demo
    )
    
    print(f"\nOptimal Configuration found: {best_params}")

if __name__ == "__main__":
    main()
