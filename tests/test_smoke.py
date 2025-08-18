import importlib

def test_package_version():
    pkg = importlib.import_module("irmcp")
    assert hasattr(pkg, "__version__")
    assert isinstance(pkg.__version__, str)
    assert pkg.__version__


def test_fastmcp_importable():
    try:
        import fastmcp  # noqa: F401
    except Exception as e:
        raise AssertionError(f"fastmcp not importable: {e}")


def test_httpx_importable():
    try:
        import httpx  # noqa: F401
    except Exception as e:
        raise AssertionError(f"httpx not importable: {e}")
