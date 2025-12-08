import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app

# Use a local SQLite database for ALL tests (local + CI)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Force settings to use the test DB in the test environment
settings.DATABASE_URL = TEST_DATABASE_URL

# Create async engine and session factory for tests
engine = create_async_engine(TEST_DATABASE_URL, future=True)
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency override for FastAPI routes: use the test SQLite DB."""
    async with AsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
async def prepare_database() -> AsyncGenerator[None, None]:
    """
    Create all tables once before the test session and drop them afterwards.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
def override_db_dependency() -> AsyncGenerator[None, None]:
    """
    Make the FastAPI app use override_get_db instead of the normal get_db
    for the entire test session.
    """
    app.dependency_overrides[get_db] = override_get_db
    try:
        yield
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Convenience client fixture (not strictly required for your tests, but handy).
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
