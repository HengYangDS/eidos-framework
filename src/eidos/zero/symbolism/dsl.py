from collections.abc import Callable
from typing import Self, Any
import uuid
from beartype import beartype
from .ast import Node, Graph, OpType

@beartype
class SymbolicStream:
    """
    Represents a stream of data in the logical graph.
    It holds the reference to the current tip of the graph (node).
    """
    def __init__(self, node: Node, graph: Graph | None = None):
        self.node = node
        self.graph = graph if graph is not None else Graph()
        self.graph.add_node(node)

    def __rshift__(self, other: "Operator") -> "SymbolicStream":
        """
        The core algebra: Stream >> Operator -> New Stream
        """
        if not isinstance(other, Operator):
            raise TypeError(f"Right operand must be an Operator, got {type(other)}")
        return other.bind(self)
    
    def _merge_graph(self, other: "SymbolicStream"):
        """Helper to merge two graphs."""
        if self.graph is not other.graph:
            for nid, n in other.graph.nodes.items():
                self.graph.add_node(n)
            for edge in other.graph.edges:
                self.graph.edges.append(edge)

    def __add__(self, other: "SymbolicStream") -> "SymbolicStream":
        """
        Interference Algebra: Stream + Stream -> Merged Stream
        """
        if not isinstance(other, SymbolicStream):
            raise TypeError(f"Right operand must be a SymbolicStream, got {type(other)}")
        
        self._merge_graph(other)
        
        # Create Merge Node
        merge_node = Node(
            id=uuid.uuid4().hex,
            op_type=OpType.MERGE,
            config={},
            parents=[self.node.id, other.node.id]
        )
        return SymbolicStream(merge_node, self.graph)

    def __or__(self, other: "SymbolicStream") -> "SymbolicStream":
        """
        Choice Algebra: Stream | Stream -> Choice Stream (Fallback/Union)
        """
        if not isinstance(other, SymbolicStream):
            raise TypeError(f"Right operand must be a SymbolicStream, got {type(other)}")
        
        self._merge_graph(other)
        
        choice_node = Node(
            id=uuid.uuid4().hex,
            op_type=OpType.CHOICE,
            config={},
            parents=[self.node.id, other.node.id]
        )
        return SymbolicStream(choice_node, self.graph)

    def __and__(self, other: "SymbolicStream") -> "SymbolicStream":
        """
        Ensemble Algebra: Stream & Stream -> Ensemble Stream (Parallel/Zip)
        """
        if not isinstance(other, SymbolicStream):
            raise TypeError(f"Right operand must be a SymbolicStream, got {type(other)}")
        
        self._merge_graph(other)
        
        ensemble_node = Node(
            id=uuid.uuid4().hex,
            op_type=OpType.ENSEMBLE,
            config={},
            parents=[self.node.id, other.node.id]
        )
        return SymbolicStream(ensemble_node, self.graph)

    def compile(self) -> Graph:
        """
        Syntactic sugar to get the graph.
        In a real scenario, this would call the Compiler.
        """
        return self.graph

@beartype
class Operator:
    """
    Base class for all logical operators.
    """
    def __init__(self, config: dict | None = None):
        self.config = config or {}

    @property
    def op_type(self) -> OpType:
        return OpType.CUSTOM

    def bind(self, upstream: SymbolicStream) -> SymbolicStream:
        """
        Connects this operator to an upstream stream.
        """
        new_node = Node(
            id=uuid.uuid4().hex,
            op_type=self.op_type,
            config=self.config,
            parents=[upstream.node.id]
        )
        return SymbolicStream(new_node, upstream.graph)

    def __rshift__(self, other: "Operator") -> "ChainOperator":
        """Composition: op1 >> op2"""
        return ChainOperator(self, other)

    def __or__(self, other: "Operator") -> "ChoiceOperator":
        """Choice: op1 | op2"""
        return ChoiceOperator(self, other)

    def __and__(self, other: "Operator") -> "EnsembleOperator":
        """Ensemble: op1 & op2"""
        return EnsembleOperator(self, other)

class ChainOperator(Operator):
    def __init__(self, left: Operator, right: Operator):
        self.left = left
        self.right = right
        super().__init__()

    def bind(self, upstream: SymbolicStream) -> SymbolicStream:
        # stream >> (A >> B) is equivalent to (stream >> A) >> B
        return upstream >> self.left >> self.right

class ChoiceOperator(Operator):
    def __init__(self, left: Operator, right: Operator):
        self.left = left
        self.right = right
        # We store the configs of sub-operators to reconstruct them in runtime
        super().__init__(config={
            "left": {"type": left.op_type.value, "config": left.config},
            "right": {"type": right.op_type.value, "config": right.config}
        })

    @property
    def op_type(self) -> OpType:
        return OpType.CHOICE

class EnsembleOperator(Operator):
    def __init__(self, left: Operator, right: Operator):
        self.left = left
        self.right = right
        super().__init__(config={
            "left": {"type": left.op_type.value, "config": left.config},
            "right": {"type": right.op_type.value, "config": right.config}
        })

    @property
    def op_type(self) -> OpType:
        return OpType.ENSEMBLE

# --- Standard Operators ---

class Source:
    """
    Entry point for data sources.
    Now a class to support static factory methods.
    """
    def __new__(cls, uri: str) -> SymbolicStream:
        """
        Default constructor: Source("uri")
        """
        node = Node(
            id=uuid.uuid4().hex,
            op_type=OpType.SOURCE,
            config={"uri": uri},
            parents=[]
        )
        return SymbolicStream(node)
    
    @staticmethod
    def from_payload(payload: Any) -> SymbolicStream:
        """
        Creates a source from a direct payload (dict/list).
        Used by REST Port.
        """
        node = Node(
            id=uuid.uuid4().hex,
            op_type=OpType.SOURCE,
            config={"uri": "payload://", "payload": payload},
            parents=[]
        )
        return SymbolicStream(node)

@beartype
class Map(Operator):
    def __init__(self, fn: Callable):
        super().__init__(config={"fn": fn, "fn_name": getattr(fn, "__name__", str(fn))})

    @property
    def op_type(self) -> OpType:
        return OpType.MAP

@beartype
class Filter(Operator):
    def __init__(self, predicate: Callable):
        super().__init__(config={"predicate": predicate, "fn_name": getattr(predicate, "__name__", str(predicate))})

    @property
    def op_type(self) -> OpType:
        return OpType.FILTER

@beartype
class Sink(Operator):
    def __init__(self, uri: str):
        super().__init__(config={"uri": uri})

    @property
    def op_type(self) -> OpType:
        return OpType.SINK

    @classmethod
    def to_response(cls) -> "Sink":
        """
        Returns a Sink that outputs to the HTTP response.
        """
        return cls(uri="http://response")
