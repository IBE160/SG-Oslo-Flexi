import os
from unittest import mock
from app.core.config import Settings

def test_redis_url_config():
    # Test default/provided value
    # We must provide DATABASE_URL as it is required
    settings = Settings(DATABASE_URL="postgresql://user:pass@localhost/db", REDIS_URL="redis://localhost:6379/0")
    assert settings.REDIS_URL == "redis://localhost:6379/0"

def test_redis_url_env_override():
    # Mock environment variable
    with mock.patch.dict(os.environ, {"REDIS_URL": "redis://otherhost:6379/1", "DATABASE_URL": "postgresql://user:pass@localhost/db"}):
        settings = Settings()
        assert settings.REDIS_URL == "redis://otherhost:6379/1"
