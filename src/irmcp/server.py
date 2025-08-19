"""Server utilities: environment setup and HTTPX logging configuration."""

import logging
import os
from typing import Any, Dict, Optional

import yaml
from fastmcp.experimental.utilities.openapi import convert_openapi_schema_to_json_schema


class UnexpectedBehavior(Exception):
    """Raised when code encounters an unexpected but non-fatal condition."""
    pass

def load_openapi_spec(schema_path: str) -> Dict[str, Any]:
    """Load and convert OpenAPI YAML schema to JSON schema for FastMCP.
    
    :param schema_path: Absolute path to the OpenAPI YAML file
    :returns: Converted JSON schema ready for FastMCPOpenAPI
    """
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    return convert_openapi_schema_to_json_schema(schema=schema)


def setup_httpx_logging(default_level: Optional[int] = logging.DEBUG) -> None:
    """Configure HTTPX/HTTPCORE logging once for the process.

    Honors HTTPX_LOG_LEVEL env var (numeric or name). If set, uses that; otherwise
    uses default_level if provided. No-op if neither is provided.
    
    :param default_level: Default log level to use if HTTPX_LOG_LEVEL is not set
    :type default_level: Optional[int]
    """
    level_name = os.environ.get("HTTPX_LOG_LEVEL")
    level: Optional[int] = default_level
    if level_name:
        try:
            level = int(level_name) if level_name.isdigit() else getattr(logging, level_name.upper())
        except Exception:
            level = default_level

    if level is None:
        return

    # Ensure a basic handler exists
    if not logging.getLogger().handlers:
        logging.basicConfig(level=level)
    # Set levels for httpx/httpcore loggers
    for name in ("httpx", "httpcore"):
        lg = logging.getLogger(name)
        lg.setLevel(level)
