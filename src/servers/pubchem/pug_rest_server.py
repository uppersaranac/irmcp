from __future__ import annotations

import os
from typing import Any, Dict

from mmcp.server import create_server
from pubchem.pug_rest_tools import TOOL_REGISTRY
from pydantic import BaseModel, Field


# Read chemical naming rules file
def load_chemical_naming_rules() -> str:
    """Load chemical naming rules from markdown file."""
    rules_file = os.path.join(os.path.dirname(__file__), "chemical_naming_rules.md")
    try:
        with open(rules_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Chemical naming rules file not found."

# Prompt registry for the MCP server

class NamingParams(BaseModel):
    """Parameters for study search prompts."""
    SMILES: str = Field(default=None, description="The SMILES string for the molecule to be named")


PROMPT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "naming_smiles": {
        "title": "Naming chemicals",
        "description": "Given a molecule expressed as SMILES, give it a name",
        "parameters": NamingParams,
        "message": f"""Please name the molecule {{SMILES}} by first matching a
compound in Pubchem. Use the pubchem cid to retrieve a list of names for the
compound and also to retrieve the iupac name. Use the naming rules given below to 
name the chemical.

{load_chemical_naming_rules()}
"""
    },
}

# Server configuration
API_BASE = os.environ.get("API_BASE", "https://pubchem.ncbi.nlm.nih.gov/rest/pug")
DEFAULT_TIMEOUT = float(os.environ.get("API_TIMEOUT", "30"))

def main() -> None:
    """Entry point: build and run the MCP server."""
    # Build app using the server factory with both tools and prompts
    app = create_server(
        server_name="pubchem-pug",
        tool_registry=TOOL_REGISTRY,
        prompt_registry=PROMPT_REGISTRY,
        api_base=API_BASE,
        timeout=DEFAULT_TIMEOUT
    )
    app.run()

if __name__ == "__main__":
    main()
