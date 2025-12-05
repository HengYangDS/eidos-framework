from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
import uuid

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
    id: str
    op_type: OpType
    config: Dict[str, Any] = field(default_factory=dict)
    parents: List[str] = field(default_factory=list)
    
    # Metadata for the compiler
    schema_in: Optional[Any] = None
    schema_out: Optional[Any] = None
    
    @property
    def short_id(self) -> str:
        return self.id[:8]

@dataclass
class Graph:
    """
    The Logical Plan (DAG).
    Contains all nodes and their relationships.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: List[tuple[str, str]] = field(default_factory=list)
    
    def add_node(self, node: Node):
        if node.id in self.nodes:
            return # Idempotent
        self.nodes[node.id] = node
        for p in node.parents:
            self.edges.append((p, node.id))
            
    @property
    def sources(self) -> List[Node]:
        return [n for n in self.nodes.values() if not n.parents]
        
    @property
    def sinks(self) -> List[Node]:
        return [n for n in self.nodes.values() if n.op_type == OpType.SINK]
        
    def to_json(self) -> Dict[str, Any]:
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
