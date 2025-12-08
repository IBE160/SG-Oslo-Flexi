import importlib.util
from app.core.config import settings


def test_sqlalchemy_installed():
    """Ensure SQLAlchemy is installed and importable."""
    spec = importlib.util.find_spec("sqlalchemy")
    assert spec is not None


def test_database_url_configuration():
    """Verify that DATABASE_URL is set in the configuration."""
    assert settings.DATABASE_URL is not None
    # In dev/CI we expect SQLite; in prod, this can be overridden
    assert settings.DATABASE_URL.startswith("sqlite+aiosqlite://")
