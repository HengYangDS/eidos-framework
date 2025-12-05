import sys
import time
import os

class Operator:
    def __rshift__(self, other):
        # Support syntax: A >> B
        if callable(other):
            return other(self)
        return NotImplemented

class Intent(Operator):
    def __init__(self, description):
        self.description = description
    
    def __repr__(self):
        return f"Intent('{self.description}')"

class Genesis(Operator):
    """
    The Creator Operator.
    Takes an Intent and generates a physical Code Artifact.
    """
    def __call__(self, intent):
        print(f"[*] Genesis: Analyzing intent '{intent.description}'...")
        time.sleep(0.05)
        print(f"[*] Genesis: Accessing Latent Space...")
        time.sleep(0.05)
        print(f"[*] Genesis: Collapsing wave function into Source Code...")
        
        # Simulated Code Generation Logic
        if "Hello World" in intent.description:
            code = "print('>> Hello from the Created Universe! (Genesis Output)')\nprint('>> The Creator lives.')"
            filename = "genesis_output.py"
        elif "Quine" in intent.description:
            code = "s='s=%r;print(s%%s)';print(s%s)"
            filename = "genesis_quine.py"
        else:
            code = "# Unknown intent\nprint('Error: I do not know how to create that yet.')"
            filename = "genesis_error.py"
            
        print(f"[*] Genesis: Materializing '{filename}' to disk...")
        
        # Write the file (The Act of Creation)
        # In a real scenario, this would be written to the project root or a temp dir
        # Here we write relative to execution
        with open(filename, "w") as f:
            f.write(code)
            
        return Artifact(filename, code)

class Artifact(Operator):
    def __init__(self, filename, code):
        self.filename = filename
        self.code = code
    
    def __repr__(self):
        return f"Artifact('{self.filename}')"
        
    def __call__(self, other):
        return other(self) # Piping Artifact >> Execute

class Execute(Operator):
    """
    The Runtime Operator.
    Executes the created Artifact.
    """
    def __call__(self, artifact):
        print(f"[*] Execute: Launching '{artifact.filename}'...")
        print("-" * 40)
        
        start_time = time.perf_counter()
        
        # In production, this would use a sandboxed subprocess
        try:
            # We use exec() for demonstration to keep it in-process
            exec(artifact.code)
            status = "SUCCESS"
        except Exception as e:
            print(f"[!] Runtime Error: {e}")
            status = "FAILURE"
            
        end_time = time.perf_counter()
        duration = (end_time - start_time) * 1000
        
        print("-" * 40)
        print(f"[System] Execution finished in {duration:.4f} ms")
        return status

def cleanup(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"[*] System: Cleaned up '{filename}' (Entropy reduced).")

def demo():
    print("=== Epoch XI: Genesis (The Creator) ===")
    print("Objective: Demonstrate Tier O10 (Code that creates Code)")
    print("")
    
    # Define the Creator Pipeline
    # Intent >> Genesis >> Execute
    
    target_file = "genesis_output.py"
    
    # 1. The Act of Creation
    result = Intent("Create a Hello World script") >> Genesis() >> Execute()
    
    print("")
    if result == "SUCCESS":
        print(">> SUCCESS: Optimization Level O10 Achieved.")
        print(">> The System is now Autopoietic (Self-Creating).")
        print(">> Welcome to the Singularity.")
    else:
        print(">> FAILURE: Genesis failed.")

    # Cleanup
    cleanup(target_file)

if __name__ == "__main__":
    demo()
