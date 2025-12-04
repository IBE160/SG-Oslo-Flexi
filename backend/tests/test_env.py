import importlib.util

def test_fastapi_installed():
    """Verify FastAPI is installed in the environment."""
    spec = importlib.util.find_spec("fastapi")
    assert spec is not None

def test_uvicorn_installed():
    """Verify Uvicorn is installed in the environment."""
    spec = importlib.util.find_spec("uvicorn")
    assert spec is not None

def test_dotenv_installed():
    """Verify python-dotenv is installed."""
    spec = importlib.util.find_spec("dotenv")
    assert spec is not None
