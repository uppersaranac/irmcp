"""PubChem PUG-REST prompts defined with FastMCP decorators.

Call register_prompts(app) after creating the server to attach prompts.
"""

import os
from typing import Any


def _load_chemical_naming_rules() -> str:
    """Load chemical naming rules from markdown file.
    
    :returns: Content of chemical_naming_rules.md file or error message if not found
    :rtype: str
    """
    rules_file = os.path.join(os.path.dirname(__file__), "chemical_naming_rules.md")
    try:
        with open(rules_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Chemical naming rules file not found."


def register_prompts(app: Any) -> None:
    """Register PubChem prompts on the given FastMCP app using decorators.
    
    :param app: FastMCP server instance to register prompts on
    :type app: Any
    """

    @app.prompt(
        name="naming_smiles",
        title="Naming chemicals",
        description="Given a molecule expressed as SMILES, give it a name",
    )
    def naming_smiles(SMILES: str) -> str:  # noqa: N803 - keep param name to match template
        return (
            f"Please name the molecule {SMILES} by first matching a\n"
            "compound in Pubchem. Use the pubchem cid to retrieve a list of names for the \n"
            "compound and also to retrieve the iupac name. Use the naming rules given below to \n"
            "name the chemical by selecting a name from the list and reformatting it as necessary \n"
            "to follow the rules. Examine the rules step-by-step. After naming the chemical, review the name to ensure it follows the \n"
            "rules.\n\n"
            f"{_load_chemical_naming_rules()}\n"
        )
