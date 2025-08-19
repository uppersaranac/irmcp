import inspect
from typing import Any, Dict, List, Optional

import pytest

from irmcp.prompt_factory import PromptFactory

try:
    # FastMCP prompt classes for type hints (not strictly required)
    from fastmcp.prompts.prompt import Prompt
except Exception:  # pragma: no cover - available at runtime via deps
    Prompt = object  # type: ignore


class _StubServer:
    """Minimal server stub that collects prompts via add_prompt."""

    def __init__(self) -> None:
        self.prompts: List[Any] = []

    def add_prompt(self, prompt: Any) -> Any:  # Compatible with PromptCapableServer
        self.prompts.append(prompt)
        return prompt


def test_register_prompt_with_pydantic_schema_and_render(anyio_backend: str = "asyncio") -> None:
    # Define a simple parameters schema via Pydantic
    from pydantic import BaseModel, Field

    class Params(BaseModel):
        name: str = Field(description="Name to greet")
        suffix: Optional[str] = Field(default=None, description="Optional suffix")

    stub = _StubServer()
    factory = PromptFactory(stub)
    spec: Dict[str, Any] = {
        "title": "Greeter",
        "description": "Say hello",
        "message": "Hello {name}{suffix}!",
        "parameters": Params,
    }

    factory.register_prompts({"greet": spec})

    assert len(stub.prompts) == 1
    prompt = stub.prompts[0]

    # Prompt should come from FastMCP and have a coroutine render()
    assert hasattr(prompt, "render")
    assert inspect.iscoroutinefunction(prompt.render)

    # Render with arguments; missing suffix should default to empty string per factory
    import anyio

    async def _run() -> List[str]:
        msgs = await prompt.render({"name": "World", "suffix": ""})
        # Convert messages to simple text for assertion (TextContent->text)
        texts: List[str] = []
        for m in msgs:
            content = getattr(m, "content", None)
            if content and hasattr(content, "text"):
                texts.append(content.text)
        return texts

    texts = anyio.run(_run)
    assert any("Hello World!" in t for t in texts)


@pytest.mark.anyio("asyncio")
async def test_register_prompt_with_custom_executor() -> None:
    # Async executor that echoes params
    async def exec_fn(prompt_name: str, params: Dict[str, Any], template: str) -> str:
        return f"{prompt_name}:{params.get('x')}"

    stub = _StubServer()
    factory = PromptFactory(stub)
    # Provide a simple Pydantic schema so the prompt function has a matching signature
    from pydantic import BaseModel

    class Params(BaseModel):
        x: int
    spec: Dict[str, Any] = {
        "title": "Echo",
        "description": "Echo x",
        "message": "unused",
        "parameters": Params,
        "executor": exec_fn,
    }

    factory.register_prompts({"echo": spec})
    prompt = stub.prompts[0]

    msgs = await prompt.render({"x": 42})
    # Extract text payloads
    texts: List[str] = []
    for m in msgs:
        content = getattr(m, "content", None)
        if content and hasattr(content, "text"):
            texts.append(content.text)
    assert any("echo:42" in t for t in texts)
