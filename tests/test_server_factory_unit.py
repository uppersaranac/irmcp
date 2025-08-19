import httpx
from fastmcp.experimental.server.openapi import FastMCPOpenAPI

from irmcp.server import setup_httpx_logging


def test_create_server__minimal_openapi():
    # Minimal OpenAPI that should be acceptable to FastMCP
    openapi = {
        "openapi": "3.1.0",
        "info": {"title": "T", "version": "1.0.0"},
        "paths": {},
    }

    # Mock transport; no calls are made in this test
    async def handler(request: httpx.Request):  # pragma: no cover - safety
        return httpx.Response(200, json={"ok": True})

    client = httpx.AsyncClient(base_url="https://api.test", transport=httpx.MockTransport(handler))

    setup_httpx_logging()
    server = FastMCPOpenAPI(openapi_spec=openapi, client=client, name="t")

    # Server has a client and can run http app (smoke)
    assert hasattr(server, "http_app")

    # Quick lifecycle: start/stop HTTP app coroutine (does not start a server)
    # Not running run_http_async to avoid event loop conflicts in test env
    assert callable(getattr(server, "http_app", None))
