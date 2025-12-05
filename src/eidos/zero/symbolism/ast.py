from dataclasses import dataclass, field
from enum import Enum
import uuid
from typing import Any

# PEP 695 Type Aliases (Python 3.12+)
type NodeID = str
type GraphID = str
type Edge = tuple[NodeID, NodeID]

class OpType(Enum):
    SOURCE = "Source"
    MAP = "Map"
    FILTER = "Filter"
    REDUCE = "Reduce"
    WINDOW = "Window"
    JOIN = "Join"
    SINK = "Sink"
    UNION = "Union"
    CHOICE = "Choice"       # |
    ENSEMBLE = "Ensemble"   # &
    MERGE = "Merge"         # +
    CUSTOM = "Custom"

@dataclass(frozen=True)
class Node:
    """
    A node in the logical computation graph (AST).
    Immutable and serializable.
    """
    id: NodeID
    op_type: OpType
    config: dict[str, Any] = field(default_factory=dict)
    parents: list[NodeID] = field(default_factory=list)
    
    # Metadata for the compiler
    schema_in: Any | None = None
    schema_out: Any | None = None
    
    @property
    def short_id(self) -> str:
        return self.id[:8]

@dataclass
class Graph:
    """
    The Logical Plan (DAG).
    Contains all nodes and their relationships.
    """
    id: GraphID = field(default_factory=lambda: str(uuid.uuid4()))
    nodes: dict[NodeID, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    
    def add_node(self, node: Node):
        if node.id in self.nodes:
            return # Idempotent
        self.nodes[node.id] = node
        for p in node.parents:
            self.edges.append((p, node.id))
            
    @property
    def sources(self) -> list[Node]:
        return [n for n in self.nodes.values() if not n.parents]
        
    @property
    def sinks(self) -> list[Node]:
        return [n for n in self.nodes.values() if n.op_type == OpType.SINK]
        
    def to_json(self) -> dict[str, Any]:
        """Serialize graph for visualization or transport."""
        return {
            "id": self.id,
            "nodes": [
                {
                    "id": n.id,
                    "type": n.op_type.value,
                    "config": str(n.config), # Simplified for JSON
                    "parents": n.parents
                }
                for n in self.nodes.values()
            ],
            "edges": self.edges
        }
