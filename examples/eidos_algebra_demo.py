import sys
import os

# Ensure we can import from src
sys.path.insert(0, os.path.abspath("src"))

from eidos import Source, Map, Filter, Sink
from eidos.zero.compiler import Compiler

def main():
    print("=== Eidos Algebra Demo ===")
    
    # 1. Flow Algebra (>>)
    print("\n[1] Flow Algebra (>>)")
    print("    Meaning: Pass output of A to B")
    s1 = Source("raw_data")
    flow = s1 >> Map(lambda x: x*2) >> Filter(lambda x: x > 10)
    print(f"    Code: Source >> Map >> Filter")
    print(f"    Plan: {Compiler.compile(flow.compile(), 'string')}")

    # 2. Choice Algebra (|)
    print("\n[2] Choice Algebra (|)")
    print("    Meaning: Try A, if fail/empty, try B")
    
    # 2a. Operator Level
    op_choice = Map(lambda x: x) | Map(lambda x: x*2)
    flow_op_choice = Source("src") >> op_choice
    print(f"    Code (Op): Source >> (Map | Map)")
    print(f"    Plan (Op): {Compiler.compile(flow_op_choice.compile(), 'string')}")
    
    # 2b. Stream Level
    s_a = Source("primary")
    s_b = Source("fallback")
    flow_stream_choice = s_a | s_b
    print(f"    Code (Stream): Source('primary') | Source('fallback')")
    # Note: The plan might show other nodes if graphs are shared, but we just look at the latest tip
    print(f"    Plan (Stream): {Compiler.compile(flow_stream_choice.compile(), 'string')}")

    # 3. Ensemble Algebra (&)
    print("\n[3] Ensemble Algebra (&)")
    print("    Meaning: Run A and B in parallel")
    
    # 3a. Operator Level
    op_ens = Map(lambda x: x+1) & Map(lambda x: x-1)
    flow_op_ens = Source("src") >> op_ens
    print(f"    Code (Op): Source >> (Map & Map)")
    print(f"    Plan (Op): {Compiler.compile(flow_op_ens.compile(), 'string')}")
    
    # 3b. Stream Level
    s_x = Source("X")
    s_y = Source("Y")
    flow_stream_ens = s_x & s_y
    print(f"    Code (Stream): Source('X') & Source('Y')")
    print(f"    Plan (Stream): {Compiler.compile(flow_stream_ens.compile(), 'string')}")

    # 4. Interference Algebra (+)
    print("\n[4] Interference Algebra (+)")
    print("    Meaning: Merge/Sum results")
    s_m = Source("M")
    s_n = Source("N")
    flow_merge = s_m + s_n
    print(f"    Code: Source('M') + Source('N')")
    print(f"    Plan: {Compiler.compile(flow_merge.compile(), 'string')}")

    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    main()
