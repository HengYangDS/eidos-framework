from typing import Any, Callable, Awaitable
from eigen.gauge.symmetry import OperatorMixin

# Uranium Isotope: MCP
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    FastMCP = None

class MCPPort(OperatorMixin):
    """
    A Boundary Port that exposes a Hamiltonian as an MCP Tool.
    """
    def __init__(self, name: str = "EigenMCP"):
        self.server_name = name
        self.mcp = FastMCP(name) if FastMCP else None
        self.name = f"MCPPort({name})"

    def bind(self, handler: Callable[[Any], Awaitable[Any]], tool_name: str, description: str):
        if not self.mcp:
            return
        
        @self.mcp.tool(name=tool_name, description=description)
        async def run_eigen_tool(query: str) -> str:
            # Simple string-in string-out for now
            # In reality, we might parse query to dict
            result = await handler({"query": query})
            return str(result)

    async def __call__(self, input: Any) -> Any:
        if not self.mcp:
            raise RuntimeError("mcp not installed")
        
        print(f"[{self.name}] Starting MCP server...")
        await self.mcp.run()
