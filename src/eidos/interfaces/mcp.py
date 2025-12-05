from typing import Any, Callable, Dict, List, Optional, Tuple
import numpy as np
from ..intelligence.driver import CognitiveDriver, OpenAIDriver
from ..zero.symbolism.dsl import SymbolicStream
from ..system.logging import get_logger

logger = get_logger(__name__)

# Mocking mcp type for static check
FastMCP = Any

class SemanticRouter:
    """
    Routes natural language queries to specific tools using Vector Search.
    """
    def __init__(self, driver: CognitiveDriver):
        self.driver = driver
        self.routes: List[Dict[str, Any]] = [] # List of {intent, embedding, tool_name}

    async def register(self, intent: str, tool_name: str):
        embedding = await self.driver.compute_embedding([intent])
        self.routes.append({
            "intent": intent,
            "embedding": np.array(embedding[0]),
            "tool_name": tool_name
        })

    async def route(self, query: str, threshold: float = 0.7) -> Optional[str]:
        if not self.routes:
            return None
            
        query_embedding = (await self.driver.compute_embedding([query]))[0]
        q_vec = np.array(query_embedding)
        
        best_match = None
        max_score = -1.0
        
        for route in self.routes:
            t_vec = route["embedding"]
            # Cosine Similarity
            score = np.dot(q_vec, t_vec) / (np.linalg.norm(q_vec) * np.linalg.norm(t_vec))
            
            if score > max_score:
                max_score = score
                best_match = route["tool_name"]
        
        if max_score >= threshold:
            return best_match
        return None

class MCPPort:
    def __init__(self, name: str, driver: CognitiveDriver = None):
        self.name = name
        self.driver = driver or OpenAIDriver()
        self.tools: List[Dict[str, Any]] = []
        self.router = SemanticRouter(self.driver)

    async def register_pipeline(self, name: str, pipeline_fn: Callable[..., SymbolicStream], description: str = ""):
        """
        Registers a pipeline function as an MCP tool.
        """
        self.tools.append({
            "name": name,
            "fn": pipeline_fn,
            "description": description
        })
        
        # Auto-register for routing based on description or name
        await self.router.register(description or name, name)
        logger.info("Registered tool", name=name)

    async def handle_query(self, query: str) -> Any:
        """
        Handles a natural language query.
        """
        tool_name = await self.router.route(query)
        if tool_name:
            logger.info("Routing query to tool", query=query, tool=tool_name)
            tool = next((t for t in self.tools if t["name"] == tool_name), None)
            return tool
        else:
            logger.info("No matching tool found for query", query=query)
            return None

    def run(self):
        logger.info("Serving MCP tools", count=len(self.tools), name=self.name)
