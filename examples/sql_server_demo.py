import asyncio
import os
import sys
from pathlib import Path

# Ensure local src on path when running from repository root
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from eigen.runtime import activate  # type: ignore
from eigen.techne.sources.sql_source import SQLServerSource  # type: ignore
from eigen.techne.emitters.csv_sink import CSVSink  # type: ignore


def _db_config_from_env() -> dict:
    host = os.getenv("EIGEN_SQL_HOST")
    user = os.getenv("EIGEN_SQL_USER")
    password = os.getenv("EIGEN_SQL_PASSWORD")
    database = os.getenv("EIGEN_SQL_DATABASE")
    if not (host and user and password):
        raise SystemExit(
            "Missing DB envs. Please set EIGEN_SQL_HOST, EIGEN_SQL_USER, EIGEN_SQL_PASSWORD (and optional EIGEN_SQL_DATABASE)."
        )
    cfg = {"host": host, "user": user, "password": password}
    if database:
        cfg["database"] = database
    return cfg


async def main() -> None:
    activate()
    sql_path = ROOT / "src" / "eigen" / "scripts" / "dz_daily.sql"
    db_cfg = _db_config_from_env()
    src = SQLServerSource(str(sql_path), db_cfg)

    # Write results to CSV to demonstrate composition
    out_csv = ROOT / "dz_daily_sample.csv"
    sink = CSVSink(str(out_csv))
    H = src >> sink
    path = await H(None)
    print(f"Wrote query results to {path}")


if __name__ == "__main__":
    asyncio.run(main())
