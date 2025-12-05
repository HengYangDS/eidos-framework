import asyncio
import os
import sys
from pathlib import Path

# Ensure local src on path when running from repository root
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from eidos.runtime import activate  # type: ignore
from eidos.techne.sources.sql_source import SQLServerSource  # type: ignore
from eidos.techne.emitters.csv_sink import CSVSink  # type: ignore


def _db_config_from_env() -> dict:
    host = os.getenv("EIDOS_SQL_HOST")
    user = os.getenv("EIDOS_SQL_USER")
    password = os.getenv("EIDOS_SQL_PASSWORD")
    database = os.getenv("EIDOS_SQL_DATABASE")
    if not (host and user and password):
        raise SystemExit(
            "Missing DB envs. Please set EIDOS_SQL_HOST, EIDOS_SQL_USER, EIDOS_SQL_PASSWORD (and optional EIDOS_SQL_DATABASE)."
        )
    cfg = {"host": host, "user": user, "password": password}
    if database:
        cfg["database"] = database
    return cfg


async def main() -> None:
    activate()
    sql_path = ROOT / "src" / "eidos" / "scripts" / "dz_daily.sql"
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
