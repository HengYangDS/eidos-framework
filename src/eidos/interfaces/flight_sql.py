import threading
import time
from typing import Any, Dict, Optional, Generator
from ..system.logging import get_logger
from ..zero.compiler import Compiler
from ..zero.symbolism.dsl import SymbolicStream

logger = get_logger(__name__)

try:
    import pyarrow as pa
    import pyarrow.flight as flight
    from pyarrow import flight_sql
except ImportError:
    pa = None
    flight = None
    flight_sql = None

# Mock base class if pyarrow not present to avoid NameError during definition
BaseServer = flight_sql.FlightSqlServer if flight_sql else object

class EidosFlightServer(BaseServer):
    def __init__(self, location, pipelines: Dict[str, Any]):
        if flight_sql:
            super().__init__(location)
        self.location = location
        self.pipelines = pipelines

    def get_flight_info_statement(self, context, descriptor, descriptor_sql):
        # In a real implementation, we'd parse the SQL to determine the output schema
        # For now, we assume a generic schema or try to compile the target pipeline
        query = descriptor_sql.command.decode('utf-8')
        # simplistic parser: "SELECT * FROM pipeline_name"
        table_name = query.split("FROM")[-1].strip().split(" ")[0]
        
        if table_name in self.pipelines:
            # Return a ticket that contains the query
            ticket = flight.Ticket(query.encode('utf-8'))
            # Mock schema for now, in reality derive from pipeline.compile().schema
            schema = pa.schema([("result", pa.string())])
            endpoints = [flight.FlightEndpoint(ticket, [self.location])]
            return flight.FlightInfo(schema, descriptor, endpoints, -1, -1)
        
        raise flight.FlightServerError(f"Table {table_name} not found")

    def do_get_statement(self, context, ticket):
        query = ticket.ticket.decode('utf-8')
        table_name = query.split("FROM")[-1].strip().split(" ")[0]
        
        if table_name in self.pipelines:
            pipeline = self.pipelines[table_name]
            
            logger.info("Executing pipeline", table=table_name)
            
            try:
                # Resolve pipeline if it's a factory function
                flow = pipeline() if callable(pipeline) else pipeline
                
                if hasattr(flow, "compile"):
                    graph = flow.compile()
                    # Default to Polars for FlightSQL (Vector Lane)
                    result = Compiler.compile(graph, target="polars")
                    
                    # Execute Polars
                    import polars as pl
                    if isinstance(result, pl.LazyFrame):
                        df = result.collect()
                    elif isinstance(result, pl.DataFrame):
                        df = result
                    else:
                        # Fallback for test/mock scenarios or non-polars backends
                        # If result is already Arrow-compatible
                        if hasattr(result, "to_arrow"):
                            data = result.to_arrow()
                            return flight.RecordBatchStream(data)
                        else:
                             # Return string representation as result
                            data = pa.Table.from_pydict({"result": [str(result)]})
                            return flight.RecordBatchStream(data)

                    data = df.to_arrow()
                    return flight.RecordBatchStream(data)
                    
            except Exception as e:
                logger.error("Pipeline execution error", error=str(e))
                raise flight.FlightServerError(f"Execution Error: {e}")

            # Fallback
            data = pa.Table.from_pydict({"result": ["executed", "success"]})
            return flight.RecordBatchStream(data)

        raise flight.FlightServerError(f"Unknown query: {query}")

    def list_flights(self, context, criteria):
        for name in self.pipelines:
            # Yield flight info for each registered pipeline
            yield flight.FlightInfo(
                pa.schema([("result", pa.string())]),
                flight.FlightDescriptor.for_path(name),
                [flight.FlightEndpoint(name.encode('utf-8'), [self.location])],
                -1, -1
            )

class FlightSQLPort:
    """
    Exposes Eidos pipelines as a Flight SQL server.
    """
    def __init__(self, host: str = "0.0.0.0", port: int = 8815):
        self.location = f"grpc://{host}:{port}"
        self.pipelines = {}
        self.server = None
        self.thread = None
        
    def run(self, background=True):
        if flight is None:
            logger.warning("PyArrow not installed. Skipping server start.")
            return

        logger.info("Starting FlightSQL server", location=self.location)
        self.server = EidosFlightServer(self.location, self.pipelines)
        
        if background:
            self.thread = threading.Thread(target=self.server.serve)
            self.thread.daemon = True
            self.thread.start()
        else:
            self.server.serve()

    def register_table(self, name: str, pipeline: Any):
        """
        Registers a pipeline as a virtual table.
        """
        self.pipelines[name] = pipeline
        logger.info("Registered virtual table", name=name)

    def stop(self):
        if self.server:
            self.server.shutdown()
            if self.thread:
                self.thread.join()
