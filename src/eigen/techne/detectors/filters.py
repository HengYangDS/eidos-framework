from typing import Any
from ...gauge.symmetry import OperatorMixin

class SZStockDetector(OperatorMixin):
    """
    Quantum Detector: Filters for Shenzhen stocks.
    Logic: SecuCode starts with '00' or '30', OR SecuMarket is 90.
    """
    async def __call__(self, data: list[dict]) -> list[dict]:
        print(f"[Detector] Filtering {len(data)} records for SZ Market...")
        result = []
        for row in data:
            code = str(row.get("SecuCode", "")).strip()
            market = row.get("SecuMarket")
            
            # Filter Logic
            is_sz = False
            if code.startswith(("00", "30", "002", "300", "301")):
                is_sz = True
            elif market == 90: # Common code for SZ
                is_sz = True
                
            if is_sz:
                result.append(row)
                
        print(f"[Detector] Retained {len(result)} records.")
        return result

    def __repr__(self):
        return "SZDetector()"
