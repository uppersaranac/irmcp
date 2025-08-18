# IR MCP

A Python project using FastMCP and httpx. Managed with uv, tested with pytest.

## Setup

1. Ensure Python 3.13+ is installed.
2. Install uv (https://docs.astral.sh/uv/):
   - macOS (Homebrew): `brew install uv`

## Development

- Create and use a virtual environment with uv.
- Install dependencies.
- Run tests with pytest.

See commands at the end of this file.

## Structure

- `src/irmcp/`: package source
- `tests/`: pytest tests

## License

Proprietary. All rights reserved.

## Quickstart (commands)

Optional, if you prefer to run manually:

```bash
# Create venv with Python 3.13
uv venv --python 3.13
source .venv/bin/activate

# Sync/install project deps
uv sync

# Run tests
uv run pytest
```
