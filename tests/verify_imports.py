import sys
import os
from pathlib import Path

# Add src to path (robust to arbitrary working directories)
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

try:
    # Public API (stable, top-level re-exports)
    from eigen import activate, Operator, Flow, Tensor, Map, Filter, Batch, Interference

    # Optional: HTTPPort (only when fastapi/uvicorn installed)
    try:
        from eigen.techne.ports.http_port import HTTPPort  # type: ignore
        _http_available = True
    except Exception:
        _http_available = False

    print("SUCCESS: Public API imports are available.")
    if _http_available:
        print("INFO: HTTPPort available (optional deps installed).")
    else:
        print("INFO: HTTPPort not available (optional deps not installed) — OK.")

except ImportError as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
