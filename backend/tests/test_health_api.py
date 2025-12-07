import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_db_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health/db")
    
    # If DB is down, it returns 503. If up, 200.
    assert response.status_code in [200, 503]
    
    if response.status_code == 200:
        assert response.json() == {"status": "connected"}
    else:
        assert "detail" in response.json()
