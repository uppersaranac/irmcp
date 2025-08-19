# Repo instructions for GitHub Copilot (VS Code)

This repository uses Python with FastMCP and httpx. Follow these conventions when proposing code, fixes, or refactors.

## Golden rules
0. Simple and DRY.
1. Always add or update unit tests for any new function, public API, or changed behavior.
2. All functions must have reStructuredText docstrings with `:param:`, `:type:`, and `:returns:`.
3. Keep code type-safe with complete type hints; do not suppress mypy unless unavoidable (explain why).
4. Use `uv` for managing virtual environments and running commands.

## Required quality gates (run locally before proposing changes)
- Lint: `uv run ruff check`
- Types: `uv run mypy src`
- Tests: `uv run pytest -q`

All three must pass. If a gate is intentionally deferred, clearly state why and the follow-up action.

## Documentation style (reStructuredText)
Use this pattern for function docstrings:

"""
Short summary.

:param foo: What this parameter does
:type foo: str
:param retries: Max retry attempts
:type retries: int
:returns: Description of the returned value
:rtype: dict[str, Any]
:raises ValueError: When input is invalid
"""

## Testing guidance
- For new functions:
  - Write tests for the happy path and at least one edge case/error path.
  - For async, mark tests appropriately (`pytest` + `anyio`).
- For OpenAPI behavior, prefer small, focused tests that assert built request URLs or query serialization (see existing tests).
- Keep tests hermetic and fast; avoid sleeps and network.

## Error handling
- Fail fast with clear exceptions (e.g., `ValueError`, or `irmcp.server.UnexpectedBehavior` when applicable).
- Do not blanket-catch `Exception` unless re-raising with additional context.
- Log meaningful details at debug level; avoid logging secrets.

## Code organization
- Shared utilities live in `irmcp/` (e.g., logging setup, OpenAPI loading).

