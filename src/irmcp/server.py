"""Server factory helpers for creating MCP servers and HTTP clients."""

import logging
import os
from typing import Any, Dict, Optional

import httpx

# Ensure FastMCP uses the experimental OpenAPI parser
os.environ.setdefault("FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER", "true")

from fastmcp.experimental.server.openapi import FastMCPOpenAPI

from irmcp.prompt_factory import PromptFactory


def create_server(
    name: str,
    client: Any,
    openapi_spec: Dict[str, Dict[str, Any]],
    prompt_registry: Optional[Dict[str, Dict[str, Any]]] = None,
) -> FastMCPOpenAPI:
    """Create an MCP server and register tools and prompts from registries.
    
    :param name: Name of the MCP server.
    :type name: str
    :param openapi_spec: OpenAPI specification for the server (optional).
    :type openapi_spec: Optional[Dict[str, Any]]
    :param prompt_registry: Prompt registry to register (optional).
    :type prompt_registry: Optional[Dict[str, Dict[str, Any]]]
    :returns: Configured MCP server.
    :rtype: FastMCP
    """

    server = FastMCPOpenAPI(
    openapi_spec=openapi_spec,           # Required: OpenAPI specification
    client=client,         # Required: HTTP client instance
    name=name,           # Optional: Server name
)
    
    # Register prompts if provided
    if prompt_registry:
        prompt_factory = PromptFactory(server)
        prompt_factory.register_prompts(prompt_registry)
    
    return server


def make_async_httpx_client(
    *,
    base_url: str,
    timeout: float | int = 30,
    log_http: bool = False,
    log_headers: bool = False,
    log_body: bool = False,
    logger_name: str = "http",
) -> httpx.AsyncClient:
    """Create an httpx.AsyncClient with optional request/response logging.

    Enable logging by passing flags or via environment in caller.
    """
    logger = logging.getLogger(logger_name)
    if log_http and not logger.handlers:
        logging.basicConfig(level=logging.INFO)

    event_hooks: dict[str, list] = {}

    if log_http:
        async def _on_request(request: httpx.Request) -> None:  # type: ignore[no-redef]
            try:
                msg = f"HTTP {request.method} {request.url}"
                if log_headers:
                    msg += f"\n> Headers: {dict(request.headers)}"
                if log_body:
                    body_len = request.headers.get("content-length")
                    if body_len is not None:
                        msg += f"\n> Body: <{body_len} bytes>"
                logger.info(msg)
            except Exception:
                pass

        async def _on_response(response: httpx.Response) -> None:  # type: ignore[no-redef]
            try:
                req = response.request
                msg = f"HTTP {req.method} {req.url} -> {response.status_code}"
                if log_headers:
                    msg += f"\n< Headers: {dict(response.headers)}"
                if log_body:
                    body_len = response.headers.get("content-length")
                    if body_len is not None:
                        msg += f"\n< Body: <{body_len} bytes>"
                logger.info(msg)
            except Exception:
                pass

        event_hooks = {
            "request": [_on_request],
            "response": [_on_response],
        }

    return httpx.AsyncClient(
        base_url=base_url,
        timeout=timeout,
        event_hooks=event_hooks or None,
    )
