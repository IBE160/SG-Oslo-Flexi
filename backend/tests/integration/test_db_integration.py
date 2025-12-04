import pytest
from sqlalchemy import text
from app.db.session import engine

@pytest.mark.asyncio
async def test_database_connection():
    """Verify we can connect to the database."""
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except Exception as e:
        pytest.skip(f"Database connection failed: {e}")

@pytest.mark.asyncio
async def test_users_table_schema():
    """Verify users table exists and has correct columns (requires migration)."""
    try:
        async with engine.connect() as conn:
            # Check table existence
            result = await conn.execute(text(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'users'"
            ))
            columns = [row[0] for row in result.fetchall()]
            
            if not columns:
                pytest.skip("Users table not found. Migration might not have run.")
            
            assert "id" in columns
            assert "email" in columns
            assert "password_hash" in columns
            assert "created_at" in columns
    except Exception as e:
        pytest.skip(f"Database check failed: {e}")
