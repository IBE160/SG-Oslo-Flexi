import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import uuid

@pytest.mark.asyncio
async def test_register_user_success():
    transport = ASGITransport(app=app)
    email = f"test_{uuid.uuid4()}@example.com"
    password = "strongPassword123"
    
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/users/register", json={
            "email": email,
            "password": password
        })
    
    assert response.status_code == 201
    data = response.json()
    assert "data" in data
    assert data["data"]["email"] == email
    assert "id" in data["data"]
    assert "password" not in data["data"]

@pytest.mark.asyncio
async def test_register_user_duplicate():
    transport = ASGITransport(app=app)
    email = f"test_dup_{uuid.uuid4()}@example.com"
    password = "strongPassword123"
    
    # First registration
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/users/register", json={
            "email": email,
            "password": password
        })
        assert response.status_code == 201
        
        # Second registration
        response = await ac.post("/api/v1/users/register", json={
            "email": email,
            "password": password
        })
        
        assert response.status_code == 409
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "USER_EXISTS"
