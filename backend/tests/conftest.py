import os

# Set test database URL before importing app.core.config
# We use sqlite+aiosqlite for async support in tests
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"



import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator

from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.main import app
from app.db.session import AsyncSessionLocal, engine
from app.db import base
from app.models.user import User  # noqa: F401 - Import User model to register it with Base metadata


# ---------------------
# DATABASE OVERRIDES
# ---------------------

@pytest.fixture(scope="session", autouse=True)
def apply_db_override():
    """
    Override FastAPI's `get_db` dependency so the app uses the test database.
    """
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides.clear()
    from app.db.session import get_db
    app.dependency_overrides[get_db] = override_get_db

    yield
    app.dependency_overrides.clear()


# ---------------------
# ASYNC: DB setup (create/drop tables)
# ---------------------

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    """
    Create all tables before the test session and drop them after.
    """
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)

    yield  # test session runs

    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.drop_all)


# ---------------------
# ASYNC DB fixture (for async tests)
# ---------------------

@pytest_asyncio.fixture
async def adb() -> AsyncGenerator[AsyncSession, None]:
    """
    Async DB session for async tests.
    """
    async with AsyncSessionLocal() as session:
        yield session


# ---------------------
# SYNC DB fixture (for TestClient)
# ---------------------

@pytest.fixture
def db() -> Generator:
    """
    Sync DB session for tests using TestClient.
    Uses same SQLite file as async engine.
    """
    sync_engine = create_engine("sqlite:///./test.db")
    TestingSessionLocal = sessionmaker(bind=sync_engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# ---------------------
# HTTP CLIENTS
# ---------------------

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Async HTTP client (for async API tests: test_users.py)
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sync_client() -> Generator[TestClient, None, None]:
    """
    Sync TestClient (for auth tests: test_auth_api.py)
    """
    with TestClient(app) as client:
        yield client