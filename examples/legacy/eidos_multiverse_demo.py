import random
import time
import copy
from typing import List, Any, Callable, Optional

# --- The Multiverse Core ---

class Universe:
    """
    A single timeline in the Multiverse.
    """
    def __init__(self, uid: int, state: Any):
        self.uid = uid
        self.state = state
        self.alive = True
        self.log = []

    def crash(self, reason: str):
        self.alive = False
        self.log.append(f"CRASH: {reason}")

    def update(self, new_state: Any):
        self.state = new_state

    def __repr__(self):
        status = "ALIVE" if self.alive else "DEAD"
        return f"<Universe #{self.uid} | {status} | State: {self.state}>"

class Operator:
    """Base class for Multiverse Operators."""
    def __rshift__(self, other):
        return Pipeline(self, other)
    
    def run(self, universes: List[Universe]) -> List[Universe]:
        raise NotImplementedError

class Pipeline(Operator):
    def __init__(self, left: Operator, right: Operator):
        self.left = left
        self.right = right
        
    def run(self, universes: List[Universe]) -> List[Universe]:
        return self.right.run(self.left.run(universes))

# --- Operators of Infinity ---

class Fork(Operator):
    """
    Splits the current reality into N parallel universes.
    Apply a 'divergence' strategy to introduce variation.
    """
    def __init__(self, n: int, divergence_fn: Optional[Callable] = None):
        self.n = n
        self.divergence_fn = divergence_fn

    def run(self, input_universes: List[Universe]) -> List[Universe]:
        print(f"[*] Forking {len(input_universes)} timeline(s) into {self.n} parallel realities...")
        output_universes = []
        
        for parent in input_universes:
            if not parent.alive: continue
            
            for i in range(self.n):
                # Deep copy to ensure isolation between universes
                child = copy.deepcopy(parent)
                child.uid = (parent.uid * 100) + i # Simple ID branching 1 -> 100, 101...
                
                if self.divergence_fn:
                    self.divergence_fn(child, i)
                
                output_universes.append(child)
                
        return output_universes

class RiskAction(Operator):
    """
    An action that has a probability of destroying the universe.
    Demonstrates Quantum Suicide / Immortality.
    """
    def __init__(self, risk_prob: float, reward: float):
        self.risk_prob = risk_prob
        self.reward = reward

    def run(self, universes: List[Universe]) -> List[Universe]:
        print(f"[*] Executing Risk Action (Prob: {self.risk_prob}, Reward: {self.reward})...")
        for u in universes:
            if not u.alive: continue
            
            # Quantum Roll
            if random.random() < self.risk_prob:
                u.crash("Quantum decoherence in high-risk sector")
            else:
                # If it survives, it gains the reward
                u.state += self.reward
                u.log.append(f"Survived risk. Gained {self.reward}.")
        return universes

class Collapse(Operator):
    """
    Merges the multiverse back into a single reality.
    Selects the BEST surviving universe.
    """
    def run(self, universes: List[Universe]) -> List[Universe]:
        print("[*] Collapsing wavefunction...")
        survivors = [u for u in universes if u.alive]
        
        if not survivors:
            print("[!] CRITICAL: All universes have collapsed. The Null Void.")
            return []
        
        # Selection criteria: Max state value
        best_u = max(survivors, key=lambda u: u.state)
        print(f"[*] Collapse successful. Selected Best Reality: {best_u}")
        
        # The winner becomes the new Prime Universe
        return [best_u]

# --- Demo Scenarios ---

def divergence_strategy(universe: Universe, variant_idx: int):
    """
    Applies different parameters to different universes.
    """
    # Variant 0: Conservative (Low Risk, Low Reward)
    # Variant 1: Aggressive (High Risk, High Reward)
    # Variant 2: Balanced
    
    if variant_idx % 3 == 0:
        universe.strategy = "Conservative"
        universe.risk_factor = 0.1
        universe.potential_gain = 10
    elif variant_idx % 3 == 1:
        universe.strategy = "Aggressive"
        universe.risk_factor = 0.8 # 80% chance of death!
        universe.potential_gain = 100
    else:
        universe.strategy = "Balanced"
        universe.risk_factor = 0.4
        universe.potential_gain = 40
        
    universe.log.append(f"Strategy set to {universe.strategy}")

class DynamicRun(Operator):
    """
    Executes the universe's assigned strategy.
    """
    def run(self, universes: List[Universe]) -> List[Universe]:
        for u in universes:
            if not u.alive: continue
            
            # Each universe runs its own simulation logic
            if hasattr(u, 'risk_factor'):
                if random.random() < u.risk_factor:
                    u.crash(f"Strategy {u.strategy} failed")
                else:
                    u.state += u.potential_gain
                    u.log.append(f"Strategy {u.strategy} success")
        return universes

def demo_multiverse():
    print("=== Epoch IX: The Multiverse (Parallel Optimization) ===\n")
    
    # 1. The Prime Universe (Origin)
    prime = Universe(uid=1, state=0)
    current_multiverse = [prime]
    
    # 2. The Pipeline
    # Fork(3) -> Diverge Strategies -> Run -> Collapse
    
    # Step 1: Fork into 9 realities (3 groups of 3 strategies)
    op_fork = Fork(n=9, divergence_fn=divergence_strategy)
    
    # Step 2: Run the simulation in parallel
    op_run = DynamicRun()
    
    # Step 3: Collapse to the single best result
    op_collapse = Collapse()
    
    # Pipeline Construction
    pipeline = op_fork >> op_run >> op_collapse
    
    start_time = time.perf_counter()
    result_multiverse = pipeline.run(current_multiverse)
    end_time = time.perf_counter()
    
    print(f"\n[System] Elapsed Time: {(end_time - start_time)*1000:.4f} ms")
    
    if result_multiverse:
        winner = result_multiverse[0]
        print(f">> SUCCESS: Optimization Level O8 Achieved.")
        print(f">> Winner ID: {winner.uid}")
        print(f">> Strategy: {getattr(winner, 'strategy', 'Unknown')}")
        print(f">> Final State: {winner.state}")
        print(f">> Logs: {winner.log}")
        print("\n>> Conclusion: The system survived scenarios that would have killed a single-timeline process.")

if __name__ == "__main__":
    demo_multiverse()
