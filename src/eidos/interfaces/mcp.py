from typing import Any, Callable, Dict, List, Optional

# Mocking mcp type for static check
FastMCP = Any

from ..zero.symbolism.dsl import SymbolicStream

class SemanticRouter:
    """
    Routes natural language queries to specific tools.
    """
    def __init__(self):
        self.routes: Dict[str, str] = {}

    def register(self, intent: str, tool_name: str):
        self.routes[intent] = tool_name

    def route(self, query: str) -> Optional[str]:
        # Simple keyword match for PoC (Simulating Vector Search)
        import re
        def tokenize(text):
            return set(re.findall(r'\w+', text.lower()))

        best_match = None
        max_score = 0
        query_tokens = tokenize(query)
        
        for intent, tool in self.routes.items():
            intent_tokens = tokenize(intent)
            score = len(query_tokens.intersection(intent_tokens))
            if score > max_score and score > 0:
                max_score = score
                best_match = tool
        
        return best_match

class MCPPort:
    def __init__(self, name: str):
        self.name = name
        self.tools: List[Dict[str, Any]] = []
        self.router = SemanticRouter()

    def register_pipeline(self, name: str, pipeline_fn: Callable[..., SymbolicStream], description: str = ""):
        """
        Registers a pipeline function as an MCP tool.
        """
        # In a real implementation, this would inspect the pipeline_fn signature
        # and register it with FastMCP.
        self.tools.append({
            "name": name,
            "fn": pipeline_fn,
            "description": description
        })
        
        # Auto-register for routing based on description or name
        self.router.register(description or name, name)
        print(f"[MCP] Registered tool: {name}")

    def handle_query(self, query: str) -> Any:
        """
        Handles a natural language query.
        """
        tool_name = self.router.route(query)
        if tool_name:
            print(f"[MCP] Routing query '{query}' to tool '{tool_name}'")
            # In real world, we would extract args from query using LLM
            # Here we just return the tool function for demo
            tool = next((t for t in self.tools if t["name"] == tool_name), None)
            return tool
        else:
            print(f"[MCP] No matching tool found for query '{query}'")
            return None

    def run(self):
        print(f"[MCP] Serving {len(self.tools)} tools on {self.name}...")
