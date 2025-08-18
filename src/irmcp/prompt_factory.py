"""Prompt factory for registering prompts with an MCP server from a registry."""

import inspect
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Prompt, PromptArgument
from pydantic import BaseModel, RootModel


class PromptFactory:
    """Factory for registering prompts with an MCP server from a registry.
    
    This class simplifies prompt registration by using the server's native
    add_prompt mechanism.
    """
    
    def __init__(self, server: FastMCP):
        """Initialize the factory with an MCP server.
        
        :param server: The FastMCP server to register prompts with.
        :type server: FastMCP
        """
        self.server = server
        self.registry: Dict[str, Dict[str, Any]] = {}
        
    def register_prompts(self, registry: Dict[str, Dict[str, Any]]) -> None:
        """Register all prompts from a registry with the server.
        
        :param registry: Prompt registry mapping prompt names to specifications.
        :type registry: Dict[str, Dict[str, Any]]
        """
        self.registry = registry
        
        for prompt_name, spec in registry.items():
            self._register_single_prompt(prompt_name, spec)
    
    def _register_single_prompt(self, prompt_name: str, spec: Dict[str, Any]) -> None:
        """Register a single prompt with the MCP server.
        
        :param prompt_name: Name of the prompt to register.
        :type prompt_name: str
        :param spec: Prompt specification containing metadata and template.
        :type spec: Dict[str, Any]
        """
        # Get prompt metadata
        title = spec.get("title", prompt_name.replace("_", " ").title())
        description = spec.get("description", "")
        message_template = spec.get("message", "")
        parameters_schema = spec.get("parameters")
        
        # Convert Pydantic model to prompt arguments if provided
        arguments: List[PromptArgument] = []
        if parameters_schema and isinstance(parameters_schema, type) and (issubclass(parameters_schema, BaseModel) or issubclass(parameters_schema, RootModel)):
            for field_name, field_info in parameters_schema.model_fields.items():
                # Check if field is required
                required = field_info.is_required()
                # Get field description
                field_description = field_info.description or f"Parameter {field_name}"
                arguments.append(PromptArgument(
                    name=field_name,
                    description=field_description,
                    required=required
                ))
        
        # Create the prompt handler function
        async def prompt_handler(**kwargs: Any) -> str:
            """Handle prompt generation with parameter substitution."""
            params = kwargs
                
            # Validate parameters if schema is provided
            if parameters_schema and isinstance(parameters_schema, type) and (issubclass(parameters_schema, BaseModel) or issubclass(parameters_schema, RootModel)):
                validated_params = parameters_schema.model_validate(params, by_alias=True)
                params = validated_params.model_dump(by_alias=True)
            
            # Check if there's a custom executor function
            executor = spec.get("executor")
            if executor and callable(executor):
                # Use custom executor (must be an async function)
                if inspect.iscoroutinefunction(executor):
                    return await executor(prompt_name, params, message_template)
                else:
                    raise ValueError(f"Executor for prompt '{prompt_name}' must be an async function")
            else:
                # Default behavior: substitute parameters in the message template
                # Replace None values with empty strings for cleaner templates
                template_params = {k: (v if v is not None else "") for k, v in params.items()}
                
                # Substitute parameters in the message template
                try:
                    return message_template.format(**template_params)
                except KeyError as e:
                    # Handle missing parameters gracefully
                    return f"Error: Missing parameter {e} for prompt '{prompt_name}'"
                except Exception as e:
                    return f"Error formatting prompt '{prompt_name}': {str(e)}"
        
        # Set the function name for debugging
        prompt_handler.__name__ = f"prompt_{prompt_name}"
        
        # Create the Prompt object
        prompt = Prompt(
            name=prompt_name,
            title=title,
            description=description,
            arguments=arguments if arguments else None,
            fn=prompt_handler
        )
        
        # Register the prompt with the server
        self.server.add_prompt(prompt)
