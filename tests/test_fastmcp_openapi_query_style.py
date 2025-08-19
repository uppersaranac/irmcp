import sys
from typing import List

import fastmcp
import httpx
import pytest
from fastmcp.experimental.server.openapi import FastMCPOpenAPI
from fastmcp.experimental.utilities.openapi import convert_openapi_schema_to_json_schema


def _make_server_and_capture_urls(openapi_dict: dict, args: dict) -> List[str]:
    calls: List[str] = []

    async def handler(request: httpx.Request):
        calls.append(str(request.url))
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    client = httpx.AsyncClient(base_url="https://api.test", transport=transport)
    spec = convert_openapi_schema_to_json_schema(openapi_dict)
    server = FastMCPOpenAPI(openapi_spec=spec, client=client, name="t")
    # Use the MCP call path to exercise the generated tool
    # Note: _mcp_call_tool is an internal API but adequate for this repro
    import anyio

    anyio.run(server._mcp_call_tool, "echo", args)  # type: ignore[arg-type]
    return calls


@pytest.mark.xfail(reason="FastMCPOpenAPI encodes arrays as repeated params even when explode=false (form)")
def test_query_array_form_explode_false_is_not_respected():
    # Minimal OpenAPI spec: array query param with style=form, explode=false
    openapi = {
        "openapi": "3.1.0",
        "info": {"title": "T", "version": "1.0.0"},
        "paths": {
            "/echo": {
                "get": {
                    "operationId": "echo",
                    "parameters": [
                        {
                            "name": "ids",
                            "in": "query",
                            "style": "form",
                            "explode": False,
                            "schema": {"type": "array", "items": {"type": "string"}},
                        }
                    ],
                    "responses": {"200": {"description": "ok"}},
                }
            }
        },
    }

    urls = _make_server_and_capture_urls(openapi, {"ids": ["1", "2", "3"]})

    # Expected per OpenAPI (form+explode=false): `ids=1,2,3`
    # Actual (bug): multiple entries: `ids=1&ids=2&ids=3`
    assert any(
        url.endswith("/echo?ids=1,2,3") for url in urls
    ), f"Expected comma-delimited value, got: {urls}"


@pytest.mark.xfail(reason="FastMCPOpenAPI encodes arrays as repeated params even when explode=false (pipeDelimited)")
def test_query_array_pipe_explode_false_is_not_respected():
    # pipeDelimited example: expect ids=1|2|3 when explode=false
    openapi = {
        "openapi": "3.1.0",
        "info": {"title": "T", "version": "1.0.0"},
        "paths": {
            "/echo": {
                "get": {
                    "operationId": "echo",
                    "parameters": [
                        {
                            "name": "ids",
                            "in": "query",
                            "style": "pipeDelimited",
                            "explode": False,
                            "schema": {"type": "array", "items": {"type": "string"}},
                        }
                    ],
                    "responses": {"200": {"description": "ok"}},
                }
            }
        },
    }

    urls = _make_server_and_capture_urls(openapi, {"ids": ["1", "2", "3"]})
    assert any(
        url.endswith("/echo?ids=1|2|3") for url in urls
    ), f"Expected pipe-delimited value, got: {urls}"


def test_print_versions_for_diagnostics(capfd):
    print("PYTHON:", sys.version)
    print("FASTMCP:", fastmcp.__version__)
    out, _ = capfd.readouterr()
    assert "PYTHON:" in out and "FASTMCP:" in out
