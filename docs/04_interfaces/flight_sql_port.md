# FlightSQL: The Data Interface

## 1. Headless BI

Eidos acts as a **Headless BI** server using the **Apache Arrow Flight SQL** protocol. This allows standard BI tools (Tableau, PowerBI, Excel, Superset) to connect to Eidos as if it were a high-performance database (e.g., PostgreSQL).

## 2. Architecture

1.  **Client**: Tableau sends a SQL query `SELECT * FROM metrics WHERE date > '2024'`.
2.  **Flight Port**: Eidos intercepts the query.
3.  **Compiler**:
    *   Parses the SQL.
    *   Maps tables to Eidos Pipelines (Views).
    *   Pushdown filters to the source.
4.  **Execution**: The pipeline runs in Vector Lane (Polars).
5.  **Transport**: The result Arrow Table is streamed back to Tableau without serialization (Zero-Copy).

## 3. Benefits

*   **No ETL**: Analyze raw data or computed features on the fly.
*   **Consistency**: BI tools use the same logic as the production system. No more "logic drift" between Python and SQL.
*   **Speed**: Flight is 50x-100x faster than ODBC/JDBC.
