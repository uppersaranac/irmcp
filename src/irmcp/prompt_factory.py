"""Prompt factory for registering prompts with an MCP server from a registry."""

import inspect
from typing import Any, Dict, List, Protocol

from fastmcp.prompts.prompt import Prompt, PromptArgument
from pydantic import BaseModel, RootModel


class PromptCapableServer(Protocol):
    def add_prompt(self, prompt: Any) -> Any: ...


class PromptFactory:
    """Factory for registering prompts with an MCP server from a registry.
    
    This class simplifies prompt registration by using the server's native
    add_prompt mechanism.
    """
    
    def __init__(self, server: PromptCapableServer):
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
        
        # Build a function with explicit parameters (no **kwargs) so FastMCP can introspect it
        executor = spec.get("executor")
        is_async_executor = inspect.iscoroutinefunction(executor) if executor else False

        # Construct parameter signature from Pydantic model if provided
        params_list: List[str] = []
        param_names: List[str] = []
        if parameters_schema and isinstance(parameters_schema, type) and (
            issubclass(parameters_schema, BaseModel) or issubclass(parameters_schema, RootModel)
        ):
            for field_name, field_info in parameters_schema.model_fields.items():
                # Basic, conservative annotation to help UX; conversion handled by template or executor
                if field_info.is_required():
                    params_list.append(f"{field_name}: str")
                else:
                    params_list.append(f"{field_name}: str | None = None")
                param_names.append(field_name)

        param_sig = ", ".join(params_list)
        param_dict_build = ", ".join([f"'{n}': {n}" for n in param_names])

        func_name = f"prompt_{prompt_name}"
        if is_async_executor:
            body = (
                "async def "
                + func_name
                + f"({param_sig}):\n"
                + ("    params = {" + param_dict_build + "}\n" if param_dict_build else "    params = {}\n")
                + f"    return await _executor('{prompt_name}', params, _message_template)\n"
            )
        else:
            body = (
                "def "
                + func_name
                + f"({param_sig}):\n"
                + ("    params = {" + param_dict_build + "}\n" if param_dict_build else "    params = {}\n")
                + "    template_params = {k: (v if v is not None else '') for k, v in params.items()}\n"
                + "    return _message_template.format(**template_params)\n"
            )

        globals_ns: Dict[str, Any] = {
            "_executor": executor,
            "_message_template": message_template,
        }
        locals_ns: Dict[str, Any] = {}
        exec(body, globals_ns, locals_ns)
        prompt_fn = locals_ns[func_name]

        # Create the Prompt from the generated function (FastMCP API)
        prompt = Prompt.from_function(
            fn=prompt_fn,
            name=prompt_name,
            title=title,
            description=description,
        )

        # Register the prompt with the server
        self.server.add_prompt(prompt)
