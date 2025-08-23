"""PubChem PUG-REST MCP server entrypoint.

Provides an async setup routine to construct a FastMCP OpenAPI server and a
sync `main()` for launching via CLI.
"""

import asyncio
import os

import httpx

# Ensure FastMCP uses the experimental OpenAPI parser
os.environ.setdefault("FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER", "true")
from fastmcp.experimental.server.openapi import FastMCPOpenAPI

from irmcp.server import load_openapi_spec, setup_httpx_logging
from servers.pubchem.pug_prompts import register_prompts

# Server configuration
API_BASE: str = os.environ.get("API_BASE", "https://pubchem.ncbi.nlm.nih.gov/rest/pug")
DEFAULT_TIMEOUT: float = float(os.environ.get("API_TIMEOUT", "30"))

async def create_pug_server() -> FastMCPOpenAPI:
    """Build the PubChem FastMCP server instance.

    Creates an :class:`httpx.AsyncClient`, loads the OpenAPI spec, configures
    HTTP logging, registers prompts, and returns a ready-to-run
    :class:`fastmcp.experimental.server.openapi.FastMCPOpenAPI`.

    :returns: Configured FastMCP server instance for PubChem
    :rtype: fastmcp.experimental.server.openapi.FastMCPOpenAPI
    """
    # Use an async client with better connection handling: FastMCP's OpenAPI server awaits HTTP calls
    client = httpx.AsyncClient(
        base_url=API_BASE,
        timeout=httpx.Timeout(DEFAULT_TIMEOUT, connect=10.0),
        limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        headers={
            "User-Agent": "irmcp-pubchem-server/1.0",
            "Accept": "application/json",
        },
    )

    schema_path = os.path.join(os.path.dirname(__file__), "pug_rest_openapi.yaml")
    openapi_spec = load_openapi_spec(schema_path)

    # Configure HTTP logging and build app
    setup_httpx_logging()
    app = FastMCPOpenAPI(openapi_spec=openapi_spec, client=client, name="pubchem")
    register_prompts(app)
    return app


def main() -> None:
    """Entry point: build and run the MCP server.

    Creates the server via :func:`pug_server`, then runs it with the default
    STDIO transport so an MCP client can connect.

    :returns: Nothing. Blocks the current process running the server.
    :rtype: None
    """
    # Setup the app with async operations
    app = asyncio.run(create_pug_server())
    # Run the server in sync context
    app.run()

if __name__ == "__main__":
    main()
