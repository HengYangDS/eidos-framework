import asyncio
from pathlib import Path
import sys

# Ensure local 'src' is on sys.path when running without installation
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from eigen.runtime import activate
from eigen.techne.sources.file_source import FileSource
from eigen.techne.operators.standard import Map, Filter, Batch
from eigen.techne.emitters.csv_sink import CSVSink

async def main():
    print(">>> Eigen Standard Model Demo")
    
    # Locate data file
    root_dir = Path(__file__).parent.parent
    data_file = root_dir / "data.txt"
    output_file = root_dir / "output.csv"
    
    print(f"Reading from: {data_file}")
    
    # 1. Define Source
    source = FileSource(str(data_file))
    
    # 2. Define Logic
    # Filter lines with "a"
    filter_op = Filter(lambda line: "a" in line)
    
    # Map to dict structure for CSV
    def parse_line(line):
        parts = line.split(',')
        if len(parts) >= 2:
            return {"fruit": parts[0].strip(), "price": float(parts[1].strip())}
        return {"fruit": line.strip(), "price": 0.0}

    map_op = Map(parse_line)
    
    # 3. Define Sink
    sink = CSVSink(str(output_file))
    
    # Activate runtime (set QuantumField)
    activate()

    # 4. Compose Hamiltonian
    # source >> filter >> map >> sink
    H = source >> filter_op >> map_op >> sink
    
    print(">>> Executing Pipeline...")
    await H(None)
    print(f">>> Done. Check {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
