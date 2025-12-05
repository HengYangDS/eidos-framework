import json
import importlib.util
import importlib.machinery
from pathlib import Path
from typing import Any
import uvicorn

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
except ImportError:
    FastAPI = None

from ..system.logging import get_logger
from ..system.evolution import EvolutionarySupervisor
from ..system.governance import LineageRegistry

logger = get_logger(__name__)

app = FastAPI(title="Eidos Studio") if FastAPI else None

if app:
    # CORS for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

# State
CURRENT_SCRIPT: Path | None = None

if app:
    @app.get("/api/graph")
    def get_graph(script: str | None = None):
        """
        Parses the script and returns the AST Graph JSON.
        """
        target = script or (str(CURRENT_SCRIPT) if CURRENT_SCRIPT else None)
        if not target:
            return {"error": "No script specified"}
        
        try:
            p = Path(target)
            if not p.exists():
                return {"error": f"File not found: {p}"}
                
            # Load module dynamically
            # We use a unique name to avoid caching issues during hot-reload
            loader = importlib.machinery.SourceFileLoader(f"studio_target_{p.stem}", str(p))
            spec = importlib.util.spec_from_loader(loader.name, loader)
            mod = importlib.util.module_from_spec(spec)
            loader.exec_module(mod)
            
            if hasattr(mod, "main"):
                flow = mod.main()
                if hasattr(flow, "compile"):
                    graph = flow.compile()
                    return graph.to_json()
            
            return {"error": "No main() returning a flow found"}
            
        except Exception as e:
            logger.error("Failed to parse graph", error=str(e))
            return {"error": str(e)}

    @app.get("/api/lineage")
    def get_lineage():
        """
        Returns the contents of the lineage registry.
        """
        lineage_file = Path(".eidos/lineage.jsonl")
        if not lineage_file.exists():
            return []
        
        data = []
        try:
            with open(lineage_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        data.append(json.loads(line))
        except Exception as e:
            logger.error("Failed to read lineage", error=str(e))
            return []
        return data

    @app.post("/api/optimize")
    def run_optimization(generations: int = 3):
        """
        Triggers the Evolutionary Supervisor.
        """
        return {"status": "Optimization triggered (Mock)", "gens": generations}

def start_studio(host="127.0.0.1", port=8888, script: str | None = None):
    global CURRENT_SCRIPT
    if script:
        CURRENT_SCRIPT = Path(script)
    
    if not app:
        print("Error: FastAPI not installed. Run `pip install eidos-framework[http]`")
        return

    # Mount static files
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    else:
        logger.warning("Static directory not found", path=str(static_dir))
    
    logger.info("Starting Eidos Studio", url=f"http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
