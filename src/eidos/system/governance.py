import json
import os
from typing import Dict, Any
from datetime import datetime, timezone
from pathlib import Path
from ..zero.symbolism.ast import Graph, OpType
from ..system.logging import get_logger

logger = get_logger(__name__)

class LineageRegistry:
    _LINEAGE_FILE = Path(".eidos/lineage.jsonl")

    @classmethod
    def register(cls, graph: Graph) -> None:
        """
        Extracts and persists lineage information from the logical graph.
        """
        lineage = cls._extract_lineage(graph)
        cls._persist(lineage)

    @staticmethod
    def _extract_lineage(graph: Graph) -> Dict[str, Any]:
        """
        Extracts lineage information from the logical graph.
        """
        lineage = {
            "pipeline_id": graph.id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sources": [],
            "sinks": [],
            "transformations": []
        }
        
        for node in graph.nodes.values():
            info = {
                "id": node.id,
                "type": node.op_type.value,
                "config": node.config,
                "parents": node.parents
            }
            
            if node.op_type == OpType.SOURCE:
                lineage["sources"].append(info)
            elif node.op_type == OpType.SINK:
                lineage["sinks"].append(info)
            else:
                lineage["transformations"].append(info)
                
        return lineage

    @classmethod
    def _persist(cls, lineage: Dict[str, Any]) -> None:
        """
        Appends the lineage record to the lineage file.
        """
        try:
            cls._LINEAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(cls._LINEAGE_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(lineage) + "\n")
            logger.debug("Lineage registered", pipeline_id=lineage["pipeline_id"])
        except Exception as e:
            logger.error("Failed to persist lineage", error=str(e))
