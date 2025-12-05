import random
import time
import copy
from typing import Callable, Dict, List, Any, Tuple
from ..zero.symbolism.dsl import SymbolicStream
from ..zero.compiler import Compiler

class EvolutionarySupervisor:
    """
    Implements Autopoiesis (Self-Creation/Evolution).
    Optimizes pipeline hyperparameters through evolutionary algorithms.
    """
    def __init__(self, population_size: int = 5, generations: int = 3):
        self.population_size = population_size
        self.generations = generations
        self.history: List[Dict[str, Any]] = []

    def optimize(
        self, 
        pipeline_factory: Callable[[Dict[str, Any]], SymbolicStream], 
        param_space: Dict[str, List[Any]],
        fitness_fn: Callable[[Any], float],
        executor: str = "polars"
    ) -> Tuple[Dict[str, Any], float]:
        """
        Runs the evolution loop to find the best parameters for the pipeline.
        
        Args:
            pipeline_factory: A function that takes params and returns a pipeline.
            param_space: Dictionary of possible values for each parameter.
            fitness_fn: Function to evaluate the result of the pipeline.
            executor: Backend to use.
            
        Returns:
            (best_params, best_score)
        """
        print(f"[Evo] Starting evolution: {self.generations} gens, pop={self.population_size}")
        
        # 1. Initialize Population
        population = [self._random_genome(param_space) for _ in range(self.population_size)]
        best_genome = None
        best_fitness = -float('inf')
        
        for gen in range(self.generations):
            print(f"[Evo] Generation {gen+1}/{self.generations}...")
            gen_results = []
            
            for genome in population:
                # 2. Compile Phenotype (The Pipeline)
                try:
                    flow = pipeline_factory(genome)
                    graph = flow.compile()
                    
                    # 3. Execute (Physics)
                    # For optimization, we might run on a sample or full data
                    start_time = time.time()
                    # Note: In a real scenario, we'd handle execution result properly
                    # Here we assume compile returns a runnable or result object
                    executable = Compiler.compile(graph, target=executor)
                    
                    result = None
                    if hasattr(executable, "collect"): # Polars
                        result = executable.collect()
                    elif callable(executable): # String/Sink
                        result = executable()
                    else:
                        result = executable
                        
                    # 4. Measure Fitness
                    score = fitness_fn(result)
                    duration = time.time() - start_time
                    
                    gen_results.append((genome, score))
                    self.history.append({
                        "gen": gen, "params": genome, "score": score, "duration": duration
                    })
                    
                    if score > best_fitness:
                        best_fitness = score
                        best_genome = genome
                        print(f"  > New Best: {score:.4f} with {genome}")
                        
                except Exception as e:
                    print(f"  ! Individual died: {e}")
                    gen_results.append((genome, -float('inf')))
            
            # 5. Selection & Reproduction (Simple Elitism + Mutation)
            # Sort by score descending
            gen_results.sort(key=lambda x: x[1], reverse=True)
            
            # Keep top 50%
            survivors = [g for g, s in gen_results[:max(1, self.population_size // 2)]]
            
            # Repopulate
            new_pop = survivors[:]
            while len(new_pop) < self.population_size:
                parent = random.choice(survivors)
                child = self._mutate(parent, param_space)
                new_pop.append(child)
            
            population = new_pop
            
        print(f"[Evo] Evolution complete. Best Score: {best_fitness}")
        return best_genome, best_fitness

    def _random_genome(self, space: Dict[str, List[Any]]) -> Dict[str, Any]:
        return {k: random.choice(v) for k, v in space.items()}

    def _mutate(self, genome: Dict[str, Any], space: Dict[str, List[Any]]) -> Dict[str, Any]:
        """Randomly change one gene."""
        child = copy.deepcopy(genome)
        gene_to_mutate = random.choice(list(space.keys()))
        child[gene_to_mutate] = random.choice(space[gene_to_mutate])
        return child
