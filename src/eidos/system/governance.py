from typing import Dict, Any
from ..zero.symbolism.ast import Graph, OpType

class LineageRegistry:
    @staticmethod
    def extract_lineage(graph: Graph) -> Dict[str, Any]:
        """
        Extracts lineage information from the logical graph.
        """
        lineage = {
            "pipeline_id": graph.id,
            "sources": [],
            "sinks": [],
            "transformations": []
        }
        
        for node in graph.nodes.values():
            info = {
                "id": node.id,
                "type": node.op_type.value,
                "config": str(node.config)
            }
            
            if node.op_type == OpType.SOURCE:
                lineage["sources"].append(info)
            elif node.op_type == OpType.SINK:
                lineage["sinks"].append(info)
            else:
                lineage["transformations"].append(info)
                
        return lineage
