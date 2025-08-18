"""Server factory for creating MCP servers with tools and prompts."""

from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP
from mmcp.tool_factory import ToolFactory
from mmcp.prompt_factory import PromptFactory


def create_server(
    server_name: str,
    tool_registry: Optional[Dict[str, Dict[str, Any]]] = None,
    prompt_registry: Optional[Dict[str, Dict[str, Any]]] = None,
    api_base: str = "",
    timeout: float = 30.0
) -> FastMCP:
    """Create an MCP server and register tools and prompts from registries.
    
    :param server_name: Name of the MCP server.
    :type server_name: str
    :param tool_registry: Tool registry to register (optional).
    :type tool_registry: Optional[Dict[str, Dict[str, Any]]]
    :param prompt_registry: Prompt registry to register (optional).
    :type prompt_registry: Optional[Dict[str, Dict[str, Any]]]
    :param api_base: Base URL for HTTP requests (only needed for tools).
    :type api_base: str
    :param timeout: Timeout for HTTP requests (only needed for tools).
    :type timeout: float
    :returns: Configured MCP server.
    :rtype: FastMCP
    """
    server = FastMCP(name=server_name)
    
    # Register tools if provided
    if tool_registry:
        tool_factory = ToolFactory(server, api_base, timeout)
        tool_factory.register_tools(tool_registry)
    
    # Register prompts if provided
    if prompt_registry:
        prompt_factory = PromptFactory(server)
        prompt_factory.register_prompts(prompt_registry)
    
    return server
