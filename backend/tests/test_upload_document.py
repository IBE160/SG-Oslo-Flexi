import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import get_password_hash
import uuid
from unittest.mock import AsyncMock, patch

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
async def test_upload_file_too_large(client: AsyncClient, adb: AsyncSession):
    headers, _ = await create_user_and_get_token(adb, client)
    
    # Create a 21MB file
    large_content = b"a" * (21 * 1024 * 1024)
    files = {"file": ("large_file.pdf", large_content, "application/pdf")}
    
    with patch("app.api.documents.os.path.getsize", return_value=len(large_content)):
        response = await client.post("/api/v1/documents/", headers=headers, files=files)
    
    assert response.status_code == 413
    assert "File too large" in response.json()["detail"]

@pytest.mark.asyncio
@pytest.mark.parametrize("filename, content, mime", [
    ("test.docx", b"PK\x03\x04", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ("test.txt", b"Just some text", "text/plain")
])
@patch("app.api.documents.magic.from_buffer")
async def test_upload_docx_and_txt_success(mock_magic, client: AsyncClient, adb: AsyncSession, filename, content, mime):
    mock_magic.return_value = mime
    headers, _ = await create_user_and_get_token(adb, client)
    files = {"file": (filename, content, mime)}
    
    response = await client.post("/api/v1/documents/", headers=headers, files=files)
    
    assert response.status_code == 202
    assert response.json()["filename"] == filename

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
    with patch("app.api.documents.os.path.getsize", return_value=len(file_content)):
        await client.post("/api/v1/documents/", headers=headers, files=files)
    
    # Get list
    response = await client.get("/api/v1/documents/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["filename"] == "test.pdf"

@pytest.mark.asyncio
async def test_document_access_is_isolated(client: AsyncClient, adb: AsyncSession):
    # User 1 uploads a doc
    headers1, _ = await create_user_and_get_token(adb, client)
    file_content1 = b"%PDF-1.4\nUser 1 doc"
    files1 = {"file": ("user1.pdf", file_content1, "application/pdf")}
    with patch("app.api.documents.os.path.getsize", return_value=len(file_content1)):
        await client.post("/api/v1/documents/", headers=headers1, files=files1)
    
    # User 2 logs in
    headers2, _ = await create_user_and_get_token(adb, client)
    
    # User 2 tries to get documents
    response = await client.get("/api/v1/documents/", headers=headers2)
    
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
@patch("app.api.documents.storage_service.save_upload", new_callable=AsyncMock)
@patch("app.api.documents.os.path.getsize", return_value=100)
async def test_filename_is_securitized(mock_getsize, mock_save_upload, client: AsyncClient, adb: AsyncSession):
    mock_save_upload.return_value = "C:/tmp/fake/path.pdf" # Mock return value for Windows
    
    headers, _ = await create_user_and_get_token(adb, client)
    
    file_content = b"%PDF-1.4\nTest content"
    files = {"file": ("original_name.pdf", file_content, "application/pdf")}
    
    await client.post("/api/v1/documents/", headers=headers, files=files)
    
    # Assert that save_upload was called
    mock_save_upload.assert_called_once()
    
    # Get the arguments it was called with
    call_args = mock_save_upload.call_args
    _, stored_filename = call_args[0]
    
    # Check if the filename is a UUID
    filename_stem = stored_filename.split('.')[0]
    try:
        uuid.UUID(filename_stem)
    except ValueError:
        pytest.fail(f"Stored filename '{stored_filename}' is not a valid UUID.")

