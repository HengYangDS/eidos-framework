from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class EidosSettings(BaseSettings):
    """
    Central configuration for Eidos Framework.
    Reads from environment variables with prefix EIDOS_.
    Example: EIDOS_LOG_LEVEL=DEBUG
    """
    model_config = SettingsConfigDict(
        env_prefix="EIDOS_",
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # System
    log_level: str = Field("INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)")
    json_logs: bool = Field(False, description="Output logs in JSON format")
    
    # Runtime
    default_backend: str = Field("polars", description="Default execution backend (polars, ray)")
    
    # Intelligence
    openai_api_key: str | None = Field(None, description="OpenAI API Key for Nous/Sidecar")
    openai_model: str = Field("gpt-4o", description="Model for code generation")
    
    # Interfaces
    mcp_port: int = Field(8810, description="Port for MCP Server")
    flight_port: int = Field(8815, description="Port for FlightSQL Server")

settings = EidosSettings()
