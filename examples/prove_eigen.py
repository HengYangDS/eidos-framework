import asyncio
import sys
from pathlib import Path

# Ensure src is in path (project root / src)
EXAMPLES_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXAMPLES_DIR.parent
sys.path.append(str(REPO_ROOT / "src"))

from eigen.runtime import activate
from eigen.techne.sources.sql_source import SQLServerSource
from eigen.techne.detectors.filters import SZStockDetector
from eigen.techne.emitters.csv_sink import CSVSink

async def main():
    print("=== Project EIGEN: Full Link Capability Proof ===\n")
    
    # 1. Configure [Source]
    # SQL file is stored under repo_root/src/eigen/scripts
    sql_file = REPO_ROOT / "src/eigen/scripts/dz_daily.sql"
    db_config = {
        "host": "dbs.cfi",
        "user": "public_data",
        "password": "public_data",
        "database": "JYDB"
    }
    source = SQLServerSource(str(sql_file), db_config)
    
    # 2. Configure [Detector]
    # Filters SZ stocks
    filter_sz = SZStockDetector()
    
    # 3. Configure [Emitter]
    # Writes to local CSV
    output_file = EXAMPLES_DIR / "sz_stocks_result.csv"
    sink = CSVSink(str(output_file))
    
    # Activate runtime
    activate()

    # 4. Construct Hamiltonian (Pipeline)
    # Physics Semantics: H = Source >> Detector >> Emitter
    H = source >> filter_sz >> sink
    
    print(f"Constructed Hamiltonian: {H}\n")
    print(">>> Evolving System...\n")
    
    # 5. Evolve (Run)
    final_state = await H(None)
    
    print(f"\n>>> System Collapsed. Final State: {final_state}")

if __name__ == "__main__":
    asyncio.run(main())
