import importlib.util
from app.core.config import settings

def test_sqlalchemy_installed():
    """Verify SQLAlchemy is installed."""
    spec = importlib.util.find_spec("sqlalchemy")
    assert spec is not None

def test_asyncpg_installed():
    """Verify asyncpg is installed."""
    spec = importlib.util.find_spec("asyncpg")
    assert spec is not None

def test_alembic_installed():
    """Verify Alembic is installed."""
    spec = importlib.util.find_spec("alembic")
    assert spec is not None

def test_database_url_configuration():
    """Verify that DATABASE_URL is set in the configuration."""
    assert settings.DATABASE_URL is not None
    assert "postgresql" in settings.DATABASE_URL
