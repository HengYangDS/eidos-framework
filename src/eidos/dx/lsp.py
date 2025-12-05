import json
import sys
import io
import contextlib
import traceback
from typing import Dict, Any, Optional

# Assuming eidos is in path
from ..zero.symbolism.ast import Graph

class TopologyExtractor:
    """
    Core logic for the Eidos Language Server.
    Extracts topology from Python code containing Eidos DSL.
    """
    
    @staticmethod
    def extract_from_source(source_code: str) -> Dict[str, Any]:
        """
        Executes the provided source code in a sandbox and extracts
        any Eidos Graphs generated.
        """
        # Capture variables
        local_scope = {}
        
        # Redirect stdout/stderr to avoid polluting LSP stream
        capture_io = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(capture_io), contextlib.redirect_stderr(capture_io):
                # We need to inject 'eidos' into the execution scope or assume user imports it
                # But if we exec, the user code imports eidos. 
                # If eidos is not installed, it fails.
                # The runner of this script must have eidos in PYTHONPATH.
                exec(source_code, {}, local_scope)
        except Exception as e:
            return {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            
        # Find any Graph or SymbolicStream objects in the scope
        graphs = []
        for name, value in local_scope.items():
            # Check for SymbolicStream (has .compile()) or Graph
            if hasattr(value, "compile"): 
                try:
                    g = value.compile()
                    if isinstance(g, Graph):
                        graphs.append({
                            "variable": name,
                            "topology": g.to_json()
                        })
                except Exception:
                    pass
            elif isinstance(value, Graph):
                graphs.append({
                    "variable": name,
                    "topology": value.to_json()
                })
                
        return {
            "graphs": graphs,
            "logs": capture_io.getvalue()
        }

class EidosLSP:
    """
    A mock Language Server for demonstration.
    """
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "eidos/extractTopology":
            content = params.get("textDocument", {}).get("text", "")
            return TopologyExtractor.extract_from_source(content)
        
        return {"error": "Method not found"}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Python file to analyze")
    args = parser.parse_args()
    
    with open(args.file, "r") as f:
        content = f.read()
        
    extractor = TopologyExtractor()
    result = extractor.extract_from_source(content)
    print(json.dumps(result, indent=2))
