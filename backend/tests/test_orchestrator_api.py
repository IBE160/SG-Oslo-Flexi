import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from io import BytesIO

@pytest.mark.asyncio
async def test_upload_document(client: AsyncClient, adb: AsyncSession):
    # Setup: Create a test user
    test_user = User(
        email="test@example.com",
        password_hash="somehash"
    )
    adb.add(test_user)
    await adb.commit()
    await adb.refresh(test_user)

    # Prepare a dummy file for upload
    file_content = b"this is a test document"
    file = ("test_document.txt", BytesIO(file_content), "text/plain")

    # Make the request to the upload endpoint
    response = await client.post(
        "/orchestrator/upload",
        files={"file": file}
    )

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "document_id" in data
    
    # Optional: Verify the document was created in the DB
    # Note: This would require querying the DB again, which might be
    # better suited for a more direct data-layer test.
    # For this test, we trust the 200 OK and the response model.
