import sys
import importlib.util
import importlib.machinery
from pathlib import Path
from typing import Any, Dict, Callable

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    import uvicorn
except ImportError:
    FastAPI = None
    Request = Any
    JSONResponse = Any
    uvicorn = None

from ..system.logging import get_logger
from ..zero.compiler import Compiler

logger = get_logger(__name__)

class RestPort:
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        if FastAPI is None:
            raise ImportError("FastAPI not installed. Install with 'pip install eidos-framework[http]'")
            
        self.host = host
        self.port = port
        self.app = FastAPI(title="Eidos Logic Service")
        
    def load_module(self, script_path: str):
        """Loads a python script and registers exposed pipelines."""
        path = Path(script_path)
        if not path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
            
        sys.path.append(str(path.parent.resolve()))
        
        loader = importlib.machinery.SourceFileLoader("eidos_app", str(path))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        mod = importlib.util.module_from_spec(spec)
        loader.exec_module(mod)
        
        count = 0
        for name in dir(mod):
            obj = getattr(mod, name)
            if callable(obj) and getattr(obj, "_is_exposed", False):
                self._register_route(obj)
                count += 1
        
        if count == 0:
            logger.warning("No exposed pipelines found in script", script=script_path)
        else:
            logger.info("Registered pipelines", count=count, script=script_path)

    def _register_route(self, fn: Callable):
        route_path = getattr(fn, "_route", "/")
        method = getattr(fn, "_method", "POST")
        name = fn.__name__
        
        logger.info("Registering route", path=route_path, method=method, name=name)
        
        async def endpoint(request: Request):
            try:
                # parse payload
                if method in ["POST", "PUT"]:
                    try:
                        payload = await request.json()
                    except Exception:
                         payload = {}
                else:
                    payload = dict(request.query_params)
                
                logger.info("Received request", route=route_path)
                
                # Call the pipeline function to get the flow
                try:
                    flow = fn(payload)
                except TypeError:
                    # Fallback if fn doesn't take args
                    flow = fn()
                
                if hasattr(flow, "compile"):
                    graph = flow.compile()
                    
                    # Default to Polars for synchronous REST
                    result = Compiler.compile(graph, target="polars")
                    
                    # Execute if it's a LazyFrame
                    try:
                        import polars as pl
                        if isinstance(result, pl.LazyFrame):
                            df = result.collect()
                            return JSONResponse(content=df.to_dicts())
                        elif isinstance(result, pl.DataFrame):
                            return JSONResponse(content=result.to_dicts())
                    except ImportError:
                        pass
                        
                    return JSONResponse(content={"result": str(result)})
                else:
                    return JSONResponse(content={"result": str(flow)})
                    
            except Exception as e:
                logger.error("Request failed", error=str(e))
                return JSONResponse(content={"error": str(e)}, status_code=500)

        self.app.add_api_route(
            route_path, 
            endpoint, 
            methods=[method],
            summary=f"Pipeline: {name}"
        )

    def run(self):
        if uvicorn is None:
             raise ImportError("Uvicorn not installed.")
             
        logger.info("Starting REST Server", host=self.host, port=self.port)
        uvicorn.run(self.app, host=self.host, port=self.port)
