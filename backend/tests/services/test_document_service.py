import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.documents import DocumentService, storage_service
from app.models.user import User
from app.models.document import Document
from app.core.security import get_password_hash
import uuid
from fastapi import HTTPException

# Helper to create a user
async def create_test_user(db: AsyncSession, email: str) -> User:
    user = User(email=email, password_hash=get_password_hash("password"))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# Helper to create a document
async def create_test_document(db: AsyncSession, user_id: uuid.UUID) -> Document:
    doc = Document(user_id=user_id, filename="service_test.txt", file_path="/tmp/service_test.txt", mime_type="text/plain", file_size=100)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc

@pytest.mark.asyncio
async def test_service_delete_document_success(adb: AsyncSession, mocker):
    # 1. Setup
    user = await create_test_user(adb, "service_del_succ@test.com")
    doc = await create_test_document(adb, user.id)
    
    # Mock storage service to avoid actual file IO
    mocker.patch("app.services.documents.storage_service.delete_file", return_value=None)
    mocker.patch("os.path.exists", return_value=True)

    # 2. Execute
    await DocumentService.delete_document(adb, doc.id, user.id)

    # 3. Assert
    deleted_doc = await adb.get(Document, doc.id)
    assert deleted_doc is None
    # Verify that the mocked delete_file was called
    storage_service.delete_file.assert_called_once_with(doc.file_path)

@pytest.mark.asyncio
async def test_service_delete_document_not_found(adb: AsyncSession):
    user = await create_test_user(adb, "service_del_404@test.com")
    random_uuid = uuid.uuid4()

    with pytest.raises(HTTPException) as exc_info:
        await DocumentService.delete_document(adb, random_uuid, user.id)
    
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_service_delete_document_forbidden(adb: AsyncSession):
    user1 = await create_test_user(adb, "service_del_fbd1@test.com")
    user2 = await create_test_user(adb, "service_del_fbd2@test.com")
    doc = await create_test_document(adb, user1.id)

    with pytest.raises(HTTPException) as exc_info:
        await DocumentService.delete_document(adb, doc.id, user2.id)
        
    assert exc_info.value.status_code == 403
    
    # Verify document still exists
    not_deleted_doc = await adb.get(Document, doc.id)
    assert not_deleted_doc is not None
