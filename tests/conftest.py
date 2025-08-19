import pytest


@pytest.fixture
def anyio_backend():
    # Run any @pytest.mark.anyio tests with asyncio backend only
    return "asyncio"
