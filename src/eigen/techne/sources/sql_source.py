from typing import Any
from ...gauge.symmetry import OperatorMixin
from pathlib import Path

try:
    import pymssql  # optional
except Exception:  # pragma: no cover - optional dependency
    pymssql = None

class SQLServerSource(OperatorMixin):
    """
    Quantum Source: Reads data from SQL Server.
    Reads SQL from a separate file.
    """
    def __init__(self, sql_path: str, db_config: dict):
        self.sql_path = Path(sql_path)
        self.db_config = db_config
        
    def _read_sql(self) -> str:
        if not self.sql_path.exists():
            raise FileNotFoundError(f"SQL file not found: {self.sql_path}")
        return self.sql_path.read_text()

    async def __call__(self, _: Any) -> list[dict]:
        if pymssql is None:
            raise RuntimeError(
                "SQLServerSource requires optional dependency 'pymssql'. Install it to use this source."
            )
        query = self._read_sql()
        print(f"[SQL Source] Loaded Query from {self.sql_path}")
        
        host = self.db_config['host']
        user = self.db_config['user']
        password = self.db_config['password']
        database = self.db_config.get('database')
        
        print(f"[SQL Source] Connecting to {host} (DB: {database or 'Default'})...")
        
        connect_kwargs = {
            'server': host,
            'user': user,
            'password': password,
            'as_dict': True
        }
        if database:
            connect_kwargs['database'] = database

        try:
            conn = pymssql.connect(**connect_kwargs)
        except Exception as e:
             print(f"[SQL Source] Connection Failed: {e}")
             raise

        try:
            with conn.cursor() as cursor:
                print("[SQL Source] Executing query...")
                cursor.execute(query)
                rows = cursor.fetchall()
                print(f"[SQL Source] Fetched {len(rows)} rows.")
                return rows
        except Exception as e:
            print(f"[SQL Source] Query Error: {e}")
            raise
        finally:
            conn.close()

    def __repr__(self):
        return f"SQLSource({self.sql_path.name})"
