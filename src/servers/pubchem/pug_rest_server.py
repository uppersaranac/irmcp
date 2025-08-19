import os
from typing import Any, Dict

import yaml
from fastmcp.experimental.utilities.openapi import convert_openapi_schema_to_json_schema

from irmcp.server import create_server, make_async_httpx_client

# Ensure FastMCP uses the experimental OpenAPI parser before importing fastmcp modules
os.environ.setdefault("FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER", "true")

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
    SMILES: str = Field(description="The SMILES string for the molecule to be named")


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

  # Use an async client: FastMCP's OpenAPI server awaits HTTP calls
  client = make_async_httpx_client(
    base_url=API_BASE,
    timeout=DEFAULT_TIMEOUT,
    log_http=os.environ.get("API_HTTP_LOG", "").lower() in {"1", "true", "yes", "on", "debug"},
    log_headers=os.environ.get("API_HTTP_LOG_HEADERS", "").lower() in {"1", "true", "yes", "on"},
    log_body=os.environ.get("API_HTTP_LOG_BODY", "").lower() in {"1", "true", "yes", "on"},
    logger_name="pubchem.http",
  )

  schema_path = os.path.join(os.path.dirname(__file__), "pug_rest_openapi.yaml")
  with open(schema_path, "r", encoding="utf-8") as f:
    schema = yaml.safe_load(f)

  openapi_spec = convert_openapi_schema_to_json_schema(schema=schema)

  # Build app using the server factory with both tools and prompts
  app = create_server(
    name="pubchem",
    openapi_spec=openapi_spec,
    client=client,
    prompt_registry=PROMPT_REGISTRY,
  )
  app.run()

if __name__ == "__main__":
    main()
