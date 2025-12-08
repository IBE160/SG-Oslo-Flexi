from httpx import AsyncClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.core.security import get_password_hash

async def test_login_access_token(client: AsyncClient, db: Session):
    # Create a user first
    email = "testlogin@example.com"
    password = "testpassword"
    hashed_password = get_password_hash(password)
    user = User(email=email, password_hash=hashed_password)
    db.add(user)
    db.commit()

    login_data = {
        "username": email,
        "password": password
    }
    response = await client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"

async def test_login_wrong_password(client: AsyncClient, db: Session):
    # Create a user first
    email = "testwrongpassword@example.com"
    password = "testpassword"
    hashed_password = get_password_hash(password)
    user = User(email=email, password_hash=hashed_password)
    db.add(user)
    db.commit()

    login_data = {
        "username": email,
        "password": "wrongpassword"
    }
    response = await client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    
    assert response.status_code == 401
    assert "Incorrect email or password" in response.text


async def test_login_non_existent_user(client: AsyncClient, db: Session):
    login_data = {
        "username": "nonexistent@example.com",
        "password": "somepassword"
    }
    response = await client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    
    assert response.status_code == 401
    assert "Incorrect email or password" in response.text
