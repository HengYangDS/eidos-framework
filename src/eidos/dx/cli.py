import sys
import shutil
from pathlib import Path
from typing import Annotated, Optional
import importlib.util
import importlib.machinery

import typer
from rich.console import Console
from rich.theme import Theme

from eidos.system.logging import configure_logging, get_logger

# Configure Console
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "error": "bold red",
    "success": "green"
})
console = Console(theme=custom_theme)
logger = get_logger("eidos.cli")

app = typer.Typer(help="Eidos: The Neuro-Symbolic Logic Operating System CLI")

@app.command()
def create(
    name: Annotated[str, typer.Argument(help="Name of the project to create")],
    template: Annotated[str, typer.Option(help="Project template to use")] = "standard"
):
    """
    Create a new Eidos project scaffolding.
    """
    console.print(f"[info]Creating Eidos project '[bold]{name}[/bold]' using template '[bold]{template}[/bold]'...[/info]")
    
    project_path = Path(name)
    if project_path.exists():
        console.print(f"[error]Error: Directory '{name}' already exists.[/error]")
        raise typer.Exit(code=1)

    project_path.mkdir(parents=True)
    (project_path / "src").mkdir()
    (project_path / "tests").mkdir()
    
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
    (project_path / "src" / "main.py").write_text(main_py)
        
    console.print(f"[success]Project '{name}' created successfully.[/success]")
    console.print(f"[info]Run: cd {name} && eidos run src/main.py[/info]")

@app.command()
def run(
    script: Annotated[str, typer.Argument(help="Path to the pipeline script")],
    cluster: Annotated[Optional[str], typer.Option(help="Ray cluster address (e.g. ray://localhost:6379)")] = None,
    verbose: Annotated[bool, typer.Option(help="Enable verbose logging")] = False
):
    """
    Run an Eidos pipeline locally or on a cluster.
    """
    if verbose:
        configure_logging("DEBUG")
    else:
        configure_logging("INFO")

    console.print(f"[info]Running Eidos pipeline from '[bold]{script}[/bold]'...[/info]")
    if cluster:
        console.print(f"[info]Connecting to cluster: [bold]{cluster}[/bold][/info]")
        
    script_path = Path(script)
    if not script_path.exists():
        console.print(f"[error]Error: File '{script}' not found.[/error]")
        raise typer.Exit(code=1)

    # Add script dir to path so it can import sibling modules
    sys.path.append(str(script_path.parent.resolve()))
    
    try:
        loader = importlib.machinery.SourceFileLoader("eidos_user_script", str(script_path))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        mod = importlib.util.module_from_spec(spec)
        loader.exec_module(mod)
        
        # Look for a flow object or a main function that returns a flow
        if hasattr(mod, "main"):
            res = mod.main()
            if hasattr(res, "compile"): # It's a SymbolicStream or similar
                console.print("[info]Compiling and executing flow...[/info]")
                from eidos.zero.compiler import Compiler
                
                target = "ray" if cluster else "polars"
                
                # Check if backend is installed, else fallback
                if target == "ray":
                    try:
                        import ray
                    except ImportError:
                        console.print("[warning]Ray not installed, falling back to local.[/warning]")
                        target = "polars"
                
                if target == "polars":
                    try:
                        import polars
                    except ImportError:
                        console.print("[warning]Polars not installed, falling back to Python Native Execution (Free Lane).[/warning]")
                        target = "python"
                
                graph = res.compile()
                result = Compiler.compile(graph, target=target)
                
                if callable(result):
                    result()
                elif hasattr(result, "collect"): # Polars
                    print(result.collect())
                else:
                    console.print(f"[success]Execution Plan generated: {result}[/success]")
                    
        else:
            console.print("[error]Error: No 'main()' function found in script.[/error]")
            raise typer.Exit(code=1)
            
    except Exception as e:
        logger.exception("Pipeline execution failed")
        console.print(f"[error]Execution failed: {e}[/error]")
        raise typer.Exit(code=1)

@app.command()
def serve(
    script: Annotated[str, typer.Argument(help="Path to the pipeline script containing @expose functions")],
    port: Annotated[int, typer.Option(help="Port to bind")] = 8000,
    host: Annotated[str, typer.Option(help="Host to bind")] = "0.0.0.0"
):
    """
    Serve exposed pipelines as a REST API.
    """
    try:
        from eidos.interfaces.rest import RestPort
    except ImportError as e:
        console.print(f"[error]Error importing REST Port: {e}[/error]")
        console.print("[info]Hint: Install with 'pip install eidos-framework[http]'[/info]")
        raise typer.Exit(code=1)
    
    console.print(f"[info]Loading pipelines from '[bold]{script}[/bold]'...[/info]")
    
    try:
        server = RestPort(host=host, port=port)
        server.load_module(script)
        server.run()
    except Exception as e:
        console.print(f"[error]Failed to start server: {e}[/error]")
        raise typer.Exit(code=1)

@app.command()
def studio(
    script: Annotated[Optional[str], typer.Argument(help="Path to the pipeline script to visualize")] = None,
    port: Annotated[int, typer.Option(help="Port to bind")] = 8888,
    host: Annotated[str, typer.Option(help="Host to bind")] = "127.0.0.1"
):
    """
    Launch the Eidos Web Studio.
    """
    try:
        from eidos.interfaces.studio import start_studio
    except ImportError:
        console.print("[error]Error importing Studio. Install with 'pip install eidos-framework[http]'[/error]")
        raise typer.Exit(code=1)

    start_studio(host=host, port=port, script=script)

@app.command()
def deploy(
    script: Annotated[str, typer.Argument(help="Path to the pipeline script")],
    port: Annotated[int, typer.Option(help="Exposed port")] = 8000
):
    """
    Generates deployment artifacts (Dockerfile, docker-compose.yml).
    """
    from eidos.system.deployment import generate_dockerfile, generate_compose
    
    script_path = Path(script)
    if not script_path.exists():
        console.print(f"[error]Error: Script '{script}' not found.[/error]")
        raise typer.Exit(code=1)
        
    console.print(f"[info]Generating deployment artifacts for [bold]{script}[/bold]...[/info]")
    
    # Generate Dockerfile
    dockerfile = generate_dockerfile(script, port)
    Path("Dockerfile").write_text(dockerfile)
    console.print("[success]Created Dockerfile[/success]")
    
    # Generate Compose
    project_name = script_path.parent.parent.name if script_path.parent.name == "src" else "eidos-app"
    compose = generate_compose(project_name, script, port)
    Path("docker-compose.yml").write_text(compose)
    console.print("[success]Created docker-compose.yml[/success]")
    
    console.print("\n[info]To deploy, run:[/info]")
    console.print("  [bold]docker compose up --build[/bold]")

def main():
    app()

if __name__ == "__main__":
    main()
