import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import get_password_hash
import uuid

# Helper to create a user and get auth headers
async def create_user_and_get_token(adb: AsyncSession, client: AsyncClient) -> dict:
    user_email = f"test_{uuid.uuid4()}@example.com"
    password = "password123"
    
    user = User(
        email=user_email,
        password_hash=get_password_hash(password),
        is_active=True
    )
    adb.add(user)
    await adb.commit()
    await adb.refresh(user)
    
    # Login to get token
    response = await client.post(
        "/api/v1/login/access-token",
        data={"username": user_email, "password": password}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, user

@pytest.mark.asyncio
async def test_upload_document_success(client: AsyncClient, adb: AsyncSession):
    # 1. Setup Auth
    headers, _ = await create_user_and_get_token(adb, client)
    
    # 2. Create mock PDF file
    # PDF magic bytes: %PDF-1.4
    file_content = b"%PDF-1.4\nTest PDF content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}
    
    # 3. Upload
    response = await client.post("/api/v1/documents/", headers=headers, files=files)
    
    # 4. Validate
    assert response.status_code == 202
    data = response.json()
    assert "id" in data
    assert data["filename"] == "test.pdf"
    assert data["status"] == "pending"

@pytest.mark.asyncio
async def test_upload_invalid_file_type(client: AsyncClient, adb: AsyncSession):
    headers, _ = await create_user_and_get_token(adb, client)
    
    # Executable file content (MZ header)
    file_content = b"MZ\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xff\xff\x00\x00"
    files = {"file": ("malicious.exe", file_content, "application/x-dosexec")}
    
    response = await client.post("/api/v1/documents/", headers=headers, files=files)
    
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

@pytest.mark.asyncio
async def test_upload_unauthorized(client: AsyncClient):
    file_content = b"%PDF-1.4\nTest content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}
    
    response = await client.post("/api/v1/documents/", files=files)
    
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_user_documents(client: AsyncClient, adb: AsyncSession):
    headers, _ = await create_user_and_get_token(adb, client)
    
    # Upload first
    file_content = b"%PDF-1.4\nTest content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}
    await client.post("/api/v1/documents/", headers=headers, files=files)
    
    # Get list
    response = await client.get("/api/v1/documents/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["filename"] == "test.pdf"
