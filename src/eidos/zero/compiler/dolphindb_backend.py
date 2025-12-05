from typing import Any, List
from ..symbolism.ast import Node, OpType

class DolphinDBScript:
    def __init__(self, code: str, var: str):
        self.code = code
        self.var = var
    
    def __str__(self):
        return self.code

class DolphinDBBackend:
    """
    Compiles Eidos AST into DolphinDB Script (.dos).
    """
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
            pred = node.config.get("predicate_sql", "true") 
            code = f'{prev.code}\n{var} = select * from {prev.var} where {pred}'
            return DolphinDBScript(code, var)
            
        if node.op_type == OpType.CUSTOM:
            kind = node.config.get("kind")
            code = prev.code
            
            if kind == "SMA":
                win = node.config["window"]
                field = node.config["field"]
                code += f'\n{var} = select *, mavg({field}, {win}) as sma_{win} from {prev.var}'
                
            elif kind == "EMA":
                win = node.config["window"]
                field = node.config["field"]
                code += f'\n{var} = select *, ema({field}, {win}) as ema_{win} from {prev.var}'
                
            elif kind == "WMA":
                win = node.config["window"]
                field = node.config["field"]
                code += f'\n{var} = select *, wma({field}, {win}) as wma_{win} from {prev.var}'
                
            elif kind == "RSI":
                win = node.config["window"]
                field = node.config["field"]
                code += f'\n{var} = select *, rsi({field}, {win}) as rsi_{win} from {prev.var}'
                
            elif kind == "CCI":
                win = node.config["window"]
                high = node.config["high"]
                low = node.config["low"]
                close = node.config["close"]
                code += f'\n{var} = select *, cci({high}, {low}, {close}, {win}) as cci from {prev.var}'
                
            elif kind == "MACD":
                fast = node.config["fast"]
                slow = node.config["slow"]
                signal = node.config["signal"]
                field = node.config["field"]
                # DolphinDB macd returns 3 columns: diff, dea, macd
                # We assume we can perform this assign
                code += f'\n{var} = select *, macd({field}, {slow}, {fast}, {signal}) as (macd, macd_signal, macd_hist) from {prev.var}'
                
            elif kind == "OBV":
                close = node.config["close"]
                vol = node.config["vol"]
                # OBV not built-in in older versions? Assuming 'obv' plugin or manually
                # Manual: cumsum(sign(diff(close))*vol)
                code += f'\n{var} = select *, cumsum(sign(deltas({close})) * {vol}) as obv from {prev.var}'
                
            else:
                code += f'\n{var} = select * from {prev.var} // Unsupported op {kind}'
                
            return DolphinDBScript(code, var)
        
        if node.op_type == OpType.SINK:
            uri = node.config.get("uri", "")
            if uri == "stdout":
                code = f'{prev.code}\nprint({prev.var})'
                return DolphinDBScript(code, var)
            
            return DolphinDBScript(prev.code, prev.var)

        # Fallback
        return DolphinDBScript(f"{prev.code}\n# Unknown op {node.op_type}", var)
