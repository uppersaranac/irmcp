"""ClinicalTrials tool transformations using FastMCP Tool.from_tool.

Call register_tools(app) after creating the server to transform existing tools.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from fastmcp.tools import Tool

from irmcp.server import UnexpectedBehavior


def load_essie_rules() -> str:
    """Load ESSIE search guide rules from markdown file.
    
    :returns: Content of essie_gpt.md file or error message if not found
    :rtype: str
    """
    rules_file = os.path.join(os.path.dirname(__file__), "essie_gpt.md")
    try:
        with open(rules_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "ClinicalTrials.gov study search guide file not found."


async def register_tools(app: Any) -> None:
    """Transform existing tools by enhancing their descriptions with ESSIE rules.
    
    Gets the original 'studies' tool, creates an enhanced version with ESSIE guidelines
    appended to the description, adds the enhanced tool, and disables the original.
    
    :param app: FastMCP server instance with get_tool, add_tool methods
    :type app: Any
    """
    
    # List available tools to see what's available
    try:
        # Get the actual tool object
        original_studies_tool = await app.get_tool("listStudies")
        if not original_studies_tool:
            raise UnexpectedBehavior("Original 'studies' tool not found")
        
        # Load ESSIE rules to append to description
        essie_rules = load_essie_rules()
        
        # Create enhanced description by combining original with ESSIE rules
        original_description = getattr(original_studies_tool, 'description', '') or ""
        enhanced_description = (
            f"{original_description}\n\n"
            f"{essie_rules}\n\n"
            "When composing queries you must follow these guidelines:\n"
            "1. Only use the search fields, search areas, sections, modules and structs given above. "
            "Use full names and do not invent names.\n"
            "2. Use ESSIE search syntax for params that can accept that format except when doing free text searching.\n"
            "3. When filling out the fields parameter, use only fields, not modules."
        )
        
        # Create transformed tool with enhanced description
        enhanced_studies_tool = Tool.from_tool(
            original_studies_tool,
            name="search_studies",
            description=enhanced_description,
        )
        
        # Add the enhanced tool to the server
        app.add_tool(enhanced_studies_tool)
        
        # Disable the original tool to avoid confusion
        original_studies_tool.disable()

    except UnexpectedBehavior as e:
        logging.warning(e)
        pass

    
