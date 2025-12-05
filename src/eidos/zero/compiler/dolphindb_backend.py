from typing import Any, List
from ..symbolism.ast import Node, OpType

class DolphinDBBackend:
    """
    Compiles Eidos AST into DolphinDB Script (.dos).
    """
    def compile_node(self, node: Node, inputs: List[str]) -> str:
        # Inputs are strings (variable names or subqueries)
        
        if node.op_type == OpType.SOURCE:
            uri = node.config.get("uri", "")
            if uri.startswith("dolphindb://"):
                # e.g. dolphindb://dfs/trades
                path = uri.replace("dolphindb://", "")
                var_name = f"t_{node.short_id}"
                return f'{var_name} = loadTable("{path}")'
            return f't_{node.short_id} = undefined'

        if not inputs:
             raise ValueError(f"Node {node.op_type} requires input")
        
        # We assume linear chain for simplicity in this MVP
        # inputs[0] is the previous script line(s) or variable name
        # But wait, Transpiler returns whatever compile_node returns.
        # If we return code, inputs is a list of code blocks.
        
        # Strategy: Return a tuple (script_lines, output_variable_name)
        # But Transpiler expects Any.
        # Let's make compile_node return the variable name, and accumulate script in a buffer?
        # No, Transpiler is recursive.
        
        # Let's make compile_node return the *full script up to this point*? No, that duplicates.
        
        # Better: compile_node returns a "ScriptBlock" object.
        pass

    # Re-thinking: To keep it simple for Transpiler generic walker,
    # let's just return the variable name, and we assume side-effect printing?
    # No, Transpiler expects a result.
    
    # Let's stick to returning a string representing the operation, 
    # and we chain them.
    # input is the variable name of the previous step.
    
    def compile(self, graph) -> str:
        # We need a custom walker for SQL generation usually, 
        # but let's try to fit into the generic one.
        # If generic walker returns the result of compile_node...
        
        # Let's act as if we are building a string.
        pass

# Actually, for SQL/Script generation, it's better to have a context.
# But to fit into `Transpiler(backend)`, `compile_node` gets `inputs` which are results of parents.
# If `compile_node` returns a variable name, and *also* appends code to a global list?
# Or returns a structure: (code, var_name)

class DolphinDBScript:
    def __init__(self, code: str, var: str):
        self.code = code
        self.var = var
    
    def __str__(self):
        return self.code

class DolphinDBBackend:
    def compile_node(self, node: Node, inputs: List[DolphinDBScript]) -> DolphinDBScript:
        
        if node.op_type == OpType.SOURCE:
            uri = node.config.get("uri", "")
            var = f"t_{node.short_id}"
            if uri.startswith("dolphindb://"):
                path = uri.replace("dolphindb://", "")
                code = f'{var} = loadTable("{path}")'
            else:
                code = f'{var} = loadTable("dfs://temp", "{uri}")'
            return DolphinDBScript(code, var)

        prev = inputs[0]
        var = f"t_{node.short_id}"
        
        if node.op_type == OpType.FILTER:
            # Assuming predicate is a string for DDB backend (e.g. Filter("price > 100"))
            # If it's a python lambda, we can't easily transpile it without strict parsing.
            # Let's assume config["predicate_sql"] exists or we parse basic lambda.
            pred = node.config.get("predicate_sql", "true") 
            code = f'{prev.code}\n{var} = select * from {prev.var} where {pred}'
            return DolphinDBScript(code, var)
            
        if node.op_type == OpType.CUSTOM:
            kind = node.config.get("kind")
            if kind == "SMA":
                win = node.config["window"]
                field = node.config["field"]
                # select *, mavg(field, win) as sma_win from prev
                code = f'{prev.code}\n{var} = select *, mavg({field}, {win}) as sma_{win} from {prev.var}'
                return DolphinDBScript(code, var)
        
        if node.op_type == OpType.SINK:
            # Sink usually means execute or save
            # For script generation, we just return the script
            return DolphinDBScript(prev.code, prev.var)

        return DolphinDBScript(f"{prev.code}\n# Unknown op {node.op_type}", var)
