import logging
import sys
from typing import Any

import structlog
from rich.console import Console
from rich.logging import RichHandler

def configure_logging(level: str = "INFO", json_format: bool = False):
    """
    Configures structured logging for Eidos.
    
    Args:
        level: Logging level (DEBUG, INFO, WARN, ERROR).
        json_format: If True, output JSON logs (good for production/Sidecar).
                     If False, output pretty logs via Rich (good for CLI/Dev).
    """
    
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if json_format:
        # Production mode: JSON output
        processors.append(structlog.processors.JSONRenderer())
        formatter = structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer()
        )
        handler = logging.StreamHandler(sys.stdout)
    else:
        # Dev mode: Rich output
        # We don't add a renderer here because RichHandler handles it? 
        # Actually structlog with rich needs specific setup.
        
        # Let's use structlog's ConsoleRenderer for simple dev, or integrate with standard logging + RichHandler
        # The "modern" way:
        
        processors.append(structlog.dev.ConsoleRenderer())
        
        # But if we want to hijack standard logging calls too:
        handler = RichHandler(rich_tracebacks=True, markup=True)
        formatter = structlog.stdlib.ProcessorFormatter(
            processor=structlog.dev.ConsoleRenderer(),
            foreign_pre_chain=processors,
        )

    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(level.upper())

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def get_logger(name: str = None) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
