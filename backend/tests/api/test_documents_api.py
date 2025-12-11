from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models.user import User
from app.models.document import Document
from app.core.security import get_password_hash
import uuid

async def create_test_user(db: AsyncSession, email: str = "test@example.com", password: str = "testpassword") -> User:
    hashed_password = get_password_hash(password)
    user = User(email=email, password_hash=hashed_password, is_active=True)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def create_test_document(db: AsyncSession, user_id: uuid.UUID) -> Document:
    doc = Document(user_id=user_id, filename="test.pdf", file_path="/tmp/test.pdf", mime_type="application/pdf", file_size=1234)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc

async def test_delete_document_success(client: AsyncClient, adb: AsyncSession):
    # 1. Create user and document
    user = await create_test_user(adb, email="delete_success@test.com")
    doc = await create_test_document(adb, user.id)

    # 2. Login to get token
    login_data = {"username": user.email, "password": "testpassword"}
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    token = r.json()["access_token"]

    # 3. Call delete endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.delete(f"{settings.API_V1_STR}/documents/{doc.id}", headers=headers)

    # 4. Assert response and DB state
    assert response.status_code == 204

    # Verify document is deleted
    deleted_doc = await adb.get(Document, doc.id)
    assert deleted_doc is None

async def test_delete_document_not_found(client: AsyncClient, adb: AsyncSession):
    user = await create_test_user(adb, email="delete_notfound@test.com")
    
    login_data = {"username": user.email, "password": "testpassword"}
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    random_uuid = uuid.uuid4()
    response = await client.delete(f"{settings.API_V1_STR}/documents/{random_uuid}", headers=headers)

    assert response.status_code == 404

async def test_delete_document_forbidden(client: AsyncClient, adb: AsyncSession):
    # Create two users
    user1 = await create_test_user(adb, email="delete_forbidden1@test.com")
    user2 = await create_test_user(adb, email="delete_forbidden2@test.com")

    # User1 owns the document
    doc = await create_test_document(adb, user1.id)

    # User2 tries to delete it
    login_data = {"username": user2.email, "password": "testpassword"}
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    token = r.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.delete(f"{settings.API_V1_STR}/documents/{doc.id}", headers=headers)

    assert response.status_code == 403

    # Verify document is NOT deleted
    not_deleted_doc = await adb.get(Document, doc.id)
    assert not_deleted_doc is not None
