import os

import httpx

# Ensure FastMCP uses the experimental OpenAPI parser
os.environ.setdefault("FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER", "true")
from fastmcp.experimental.server.openapi import FastMCPOpenAPI

from irmcp.server import load_openapi_spec, setup_httpx_logging
from servers.pubchem.pug_prompts import register_prompts

# Ensure FastMCP uses the experimental OpenAPI parser before importing fastmcp modules
os.environ.setdefault("FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER", "true")

# Server configuration
API_BASE = os.environ.get("API_BASE", "https://pubchem.ncbi.nlm.nih.gov/rest/pug")
DEFAULT_TIMEOUT = float(os.environ.get("API_TIMEOUT", "30"))


def main() -> None:
    """Entry point: build and run the MCP server.
    
    Creates an async HTTP client, loads OpenAPI spec, configures logging,
    builds FastMCP server, registers prompts, then runs the server.
    """

    # Use an async client with better connection handling: FastMCP's OpenAPI server awaits HTTP calls
    client = httpx.AsyncClient(
        base_url=API_BASE, 
        timeout=httpx.Timeout(DEFAULT_TIMEOUT, connect=10.0),
        limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        headers={
            "User-Agent": "irmcp-pubchem-server/1.0",
            "Accept": "application/json",
        }
    )

    schema_path = os.path.join(os.path.dirname(__file__), "pug_rest_openapi.yaml")
    openapi_spec = load_openapi_spec(schema_path)

    # Configure HTTP logging and build app
    setup_httpx_logging()
    app = FastMCPOpenAPI(openapi_spec=openapi_spec, client=client, name="pubchem")
    register_prompts(app)
    app.run()

if __name__ == "__main__":
    main()
