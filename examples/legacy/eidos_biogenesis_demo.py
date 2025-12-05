import random
import time
from typing import List, Any, Type

# --- Genesis (Base Definitions) ---

class Operator:
    """Base class for all genetic operators."""
    def __rshift__(self, other):
        return Pipeline(self, other)
    
    def run(self, data: Any) -> Any:
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__

class Pipeline(Operator):
    """A sequence of operators (The Genome)."""
    def __init__(self, left: Operator, right: Operator):
        self.left = left
        self.right = right
        
    def run(self, data: Any) -> Any:
        return self.right.run(self.left.run(data))

    def __repr__(self):
        return f"({self.left} >> {self.right})"

    def to_list(self) -> List[Operator]:
        """Flatten the pipeline into a linear gene sequence."""
        ops = []
        if isinstance(self.left, Pipeline):
            ops.extend(self.left.to_list())
        else:
            ops.append(self.left)
            
        if isinstance(self.right, Pipeline):
            ops.extend(self.right.to_list())
        else:
            ops.append(self.right)
        return ops

    @staticmethod
    def from_list(ops: List[Operator]) -> Operator:
        """Reconstruct a pipeline from a gene sequence."""
        if not ops:
            return Identity()
        if len(ops) == 1:
            return ops[0]
        
        # Recursively build pipeline
        res = ops[0]
        for op in ops[1:]:
            res = res >> op
        return res

class Identity(Operator):
    def run(self, data): return data
    def __repr__(self): return "I"

# --- Atoms (The Gene Pool) ---

class Add(Operator):
    def __init__(self, val=1): self.val = val
    def run(self, data): return data + self.val
    def __repr__(self): return f"Add({self.val})"

class Sub(Operator):
    def __init__(self, val=1): self.val = val
    def run(self, data): return data - self.val
    def __repr__(self): return f"Sub({self.val})"

class Mul(Operator):
    def __init__(self, val=2): self.val = val
    def run(self, data): return data * self.val
    def __repr__(self): return f"Mul({self.val})"

# --- Biogenesis (Evolution Engine) ---

class Biogenesis:
    """
    Epoch VIII: The engine of self-evolution.
    Uses Genetic Algorithms to optimize the Operator Graph.
    """
    def __init__(self, target_val=42.0):
        self.target = target_val
        # The "Primordial Soup" of possible genes
        self.gene_pool = [
            Add(1), Add(2), Add(5), Add(10),
            Sub(1), Sub(2), Sub(5),
            Mul(2), Mul(3), Mul(0.5), Mul(1.5)
        ]
    
    def random_organism(self, length=4) -> Operator:
        """Creates a random pipeline (organism)."""
        ops = [random.choice(self.gene_pool) for _ in range(length)]
        return Pipeline.from_list(ops)

    def fitness(self, organism: Operator) -> float:
        """Calculates how close the organism is to the target."""
        try:
            # We test the organism with a seed input of 1.0
            result = organism.run(1.0)
            error = abs(result - self.target)
            # Fitness is inverse of error. Perfect match = Infinity (capped)
            if error < 0.0001: return 1000.0
            return 1.0 / error
        except Exception:
            return 0.0

    def mutate(self, organism: Operator) -> Operator:
        """Applies random point mutations."""
        ops = organism.to_list()
        if not ops: return organism
        
        # 30% chance to just return original
        if random.random() > 0.7: return organism

        # Mutation: Change one gene
        idx = random.randint(0, len(ops)-1)
        ops[idx] = random.choice(self.gene_pool)
        return Pipeline.from_list(ops)

    def crossover(self, p1: Operator, p2: Operator) -> Operator:
        """Recombines two parents to create a child."""
        ops1 = p1.to_list()
        ops2 = p2.to_list()
        
        if len(ops1) < 2 or len(ops2) < 2: return p1 
        
        # Split point crossover
        split = random.randint(1, min(len(ops1), len(ops2)) - 1)
        new_ops = ops1[:split] + ops2[split:]
        
        # Hard cap on length to prevent bloating
        if len(new_ops) > 8:
            new_ops = new_ops[:8]
            
        return Pipeline.from_list(new_ops)

    def evolve(self, generations=50, pop_size=20):
        print(f"=== Epoch VIII: Biogenesis (Evolutionary Optimization) ===")
        print(f"[*] Target Output: {self.target} (from Input: 1.0)")
        
        # 1. Initialize Population
        population = [self.random_organism() for _ in range(pop_size)]
        
        for g in range(generations):
            # 2. Evaluate Fitness
            scores = [(self.fitness(org), org) for org in population]
            scores.sort(key=lambda x: x[0], reverse=True)
            
            best_fit, best_org = scores[0]
            best_res = best_org.run(1.0)
            
            print(f"Gen {g+1:02d}: Best = {best_res:.4f} (Fit: {best_fit:.4f}) | DNA: {best_org}")
            
            if best_fit > 500: # Converged
                print(f"\n>> SUCCESS: Organism Evolved to Optimal State.")
                print(f">> SUCCESS: Optimization Level O7 Achieved.")
                print(f">> The Code has written itself.")
                return best_org
            
            # 3. Selection (Survival of the Fittest)
            # Keep top 40%
            survivors = [s[1] for s in scores[:int(pop_size * 0.4)]]
            
            # 4. Reproduction (Crossover + Mutation)
            next_gen = []
            while len(next_gen) < pop_size:
                parent1 = random.choice(survivors)
                parent2 = random.choice(survivors)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                next_gen.append(child)
            
            population = next_gen
            time.sleep(0.05) # Cinematic effect

if __name__ == "__main__":
    sim = Biogenesis(target_val=42.0)
    sim.evolve()

