import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.documents import DocumentService, storage_service
from app.models.user import User
from app.models.document import Document
from app.core.security import get_password_hash
import uuid
from fastapi import HTTPException
from datetime import datetime, timedelta

# Helper to create a user
async def create_test_user(db: AsyncSession, email: str) -> User:
    user = User(email=email, password_hash=get_password_hash("password"))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# Helper to create a document
async def create_test_document(db: AsyncSession, user_id: uuid.UUID, filename="service_test.txt") -> Document:
    file_path = f"/tmp/{uuid.uuid4()}_{filename}"
    doc = Document(user_id=user_id, filename=filename, file_path=file_path, mime_type="text/plain", file_size=100)
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

@pytest.mark.asyncio
async def test_delete_old_documents_expiration(adb: AsyncSession, mocker):
    # Setup
    user = await create_test_user(adb, "ttl_test@test.com")
    
    # Create an OLD document (should be deleted)
    doc_old = await create_test_document(adb, user.id, filename="old.txt")
    # Manually update created_at to 30 hours ago
    doc_old.created_at = datetime.utcnow() - timedelta(hours=30)
    adb.add(doc_old)
    
    # Create a NEW document (should be kept)
    doc_new = await create_test_document(adb, user.id, filename="new.txt")
    # Manually update created_at to 1 hour ago
    doc_new.created_at = datetime.utcnow() - timedelta(hours=1)
    adb.add(doc_new)
    
    await adb.commit()
    
    # Mock storage to avoid actual IO
    mocker.patch("app.services.documents.storage_service.delete_file", return_value=None)
    mocker.patch("os.path.exists", return_value=True)
    
    # Execute deletion with TTL = 24 hours
    count = await DocumentService.delete_old_documents(adb, ttl_hours=24)
    
    # Assert
    assert count == 1
    
    # Check old doc is gone
    res_old = await adb.get(Document, doc_old.id)
    assert res_old is None
    
    # Check new doc is present
    res_new = await adb.get(Document, doc_new.id)
    assert res_new is not None

@pytest.mark.asyncio
async def test_perform_document_deletion_handles_missing_file(adb: AsyncSession, mocker):
    # Setup
    user = await create_test_user(adb, "missing_file@test.com")
    doc = await create_test_document(adb, user.id)
    
    # Mock storage to simulate file not found (os.path.exists -> False)
    mocker.patch("os.path.exists", return_value=False)
    # Ensure delete_file is NOT called
    mock_delete = mocker.patch("app.services.documents.storage_service.delete_file")
    
    # Execute internal deletion method directly
    success = await DocumentService._perform_document_deletion(adb, doc)
    await adb.commit()
    
    # Assert
    assert success is True
    # DB record should be gone
    res = await adb.get(Document, doc.id)
    assert res is None
    # delete_file should not have been called
    mock_delete.assert_not_called()

@pytest.mark.asyncio
async def test_delete_old_documents_idempotency(adb: AsyncSession, mocker):
    # Setup: 1 expired document
    user = await create_test_user(adb, "idempotency@test.com")
    doc = await create_test_document(adb, user.id, filename="idempotency.txt")
    doc.created_at = datetime.utcnow() - timedelta(hours=30)
    adb.add(doc)
    await adb.commit()

    mocker.patch("app.services.documents.storage_service.delete_file", return_value=None)
    mocker.patch("os.path.exists", return_value=True)

    # 1st Run
    count1 = await DocumentService.delete_old_documents(adb, ttl_hours=24)
    assert count1 == 1
    
    # 2nd Run (should find nothing)
    count2 = await DocumentService.delete_old_documents(adb, ttl_hours=24)
    assert count2 == 0

@pytest.mark.asyncio
async def test_delete_old_documents_logging(adb: AsyncSession, mocker, capsys):
    # Setup: 2 expired documents
    user = await create_test_user(adb, "logging@test.com")
    doc1 = await create_test_document(adb, user.id, filename="log1.txt")
    doc1.created_at = datetime.utcnow() - timedelta(hours=30)
    adb.add(doc1)
    doc2 = await create_test_document(adb, user.id, filename="log2.txt")
    doc2.created_at = datetime.utcnow() - timedelta(hours=30)
    adb.add(doc2)
    await adb.commit()

    mocker.patch("app.services.documents.storage_service.delete_file", return_value=None)
    mocker.patch("os.path.exists", return_value=True)

    # Run
    await DocumentService.delete_old_documents(adb, ttl_hours=24)

    # Check stdout
    captured = capsys.readouterr()
    assert "Successfully deleted 2 old document(s)." in captured.out