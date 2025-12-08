import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import get_db
from app.db.base import Base
# Import all models to ensure they are registered with Base
from app.models.user import User  # noqa: F401
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import uuid

# Setup SQLite in-memory DB
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

async def validate():
    print("Starting validation of Story 2.1...")
    
    # Initialize DB schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    email = f"validate_{uuid.uuid4()}@example.com"
    password = "strongPassword123"
    
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        print(f"Attempting to register user: {email}")
        try:
            response = await ac.post("/api/v1/users/register", json={
                "email": email,
                "password": password
            })
            
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.json()}")
            
            if response.status_code == 201:
                data = response.json()
                if "data" in data and data["data"]["email"] == email and "id" in data["data"]:
                     print("SUCCESS: User registered successfully.")
                else:
                    print("FAILURE: Response body malformed.")
                    return False
            else:
                print(f"FAILURE: Expected 201, got {response.status_code}")
                print(response.text)
                return False

            # Test duplicate
            print("Attempting duplicate registration...")
            response_dup = await ac.post("/api/v1/users/register", json={
                "email": email,
                "password": password
            })
            print(f"Duplicate response status: {response_dup.status_code}")
            
            if response_dup.status_code == 409:
                print("SUCCESS: Duplicate registration rejected.")
            else:
                 print(f"FAILURE: Expected 409 for duplicate, got {response_dup.status_code}")
                 print(response_dup.text)
                 return False
                 
            return True

        except Exception as e:
            print(f"EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    success = asyncio.run(validate())
    if success:
        sys.exit(0)
    else:
        sys.exit(1)