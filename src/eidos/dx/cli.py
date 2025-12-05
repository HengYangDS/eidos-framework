import argparse
import os
import sys
import shutil
from typing import List

def create_project(project_name: str, template: str):
    print(f"Creating Eidos project '{project_name}' using template '{template}'...")
    
    if os.path.exists(project_name):
        print(f"Error: Directory '{project_name}' already exists.")
        return

    os.makedirs(project_name)
    os.makedirs(os.path.join(project_name, "src"))
    os.makedirs(os.path.join(project_name, "tests"))
    
    # Create main.py
    main_py = """import eidos
from eidos import Source, Map, Filter, Sink

def main():
    flow = (
        Source("csv://data.csv")
        >> Filter(lambda x: x['value'] > 0)
        >> Map(lambda x: {'value': x['value'] * 2})
        >> Sink("stdout")
    )
    return flow

if __name__ == "__main__":
    eidos.run(main())
"""
    with open(os.path.join(project_name, "src", "main.py"), "w") as f:
        f.write(main_py)
        
    print(f"Project '{project_name}' created successfully.")
    print(f"Run: cd {project_name} && eidos run src/main.py")

def run_pipeline(script_path: str, cluster: str = None):
    print(f"Running Eidos pipeline from '{script_path}'...")
    if cluster:
        print(f"Connecting to cluster: {cluster}")
        
    # We need to load the script and find the flow
    import importlib.util
    import importlib.machinery
    
    if not os.path.exists(script_path):
        print(f"Error: File '{script_path}' not found.")
        return

    # Add script dir to path so it can import sibling modules
    sys.path.append(os.path.dirname(os.path.abspath(script_path)))
    
    loader = importlib.machinery.SourceFileLoader("eidos_user_script", script_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    
    # Look for a flow object or a main function that returns a flow
    if hasattr(mod, "main"):
        res = mod.main()
        if hasattr(res, "compile"): # It's a SymbolicStream or similar
            print("Compiling and executing flow...")
            from eidos.zero.compiler import Compiler
            # For now default to local execution (Polars/String)
            # In a real scenario, we'd use the 'cluster' arg to pick backend
            target = "ray" if cluster else "polars"
            
            # Check if backend is installed, else fallback
            if target == "ray":
                try:
                    import ray
                except ImportError:
                    print("Ray not installed, falling back to local.")
                    target = "polars"
            
            if target == "polars":
                try:
                    import polars
                except ImportError:
                    print("Polars not installed, falling back to string execution plan.")
                    target = "string"
            
            graph = res.compile()
            result = Compiler.compile(graph, target=target)
            
            if callable(result):
                result()
            elif hasattr(result, "collect"): # Polars
                print(result.collect())
            else:
                print(f"Execution Plan: {result}")
                
    else:
        print("Error: No 'main()' function found in script.")

def main():
    parser = argparse.ArgumentParser(description="Eidos CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # create
    create_parser = subparsers.add_parser("create", help="Create a new Eidos project")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("--template", default="standard", help="Project template")
    
    # run
    run_parser = subparsers.add_parser("run", help="Run an Eidos pipeline")
    run_parser.add_argument("script", help="Path to the pipeline script")
    run_parser.add_argument("--cluster", help="Ray cluster address")
    
    # deploy
    deploy_parser = subparsers.add_parser("deploy", help="Deploy a pipeline")
    deploy_parser.add_argument("script", help="Path to the pipeline script")
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_project(args.name, args.template)
    elif args.command == "run":
        run_pipeline(args.script, args.cluster)
    elif args.command == "deploy":
        print("Deploy functionality coming soon.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
