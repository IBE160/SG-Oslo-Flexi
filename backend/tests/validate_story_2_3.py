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
    print("Starting validation of Story 2.3 (Basic Onboarding)...")
    
    # Initialize DB schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    email = f"onboard_{uuid.uuid4()}@example.com"
    password = "strongPassword123"
    
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        try:
            # 1. Register User
            print(f"1. Registering user: {email}")
            reg_response = await ac.post("/api/v1/users/register", json={
                "email": email,
                "password": password
            })
            if reg_response.status_code != 201:
                print(f"FAILURE: Registration failed. {reg_response.text}")
                return False
            
            user_data = reg_response.json()["data"]
            print(f"   Registered. is_onboarded (initial): {user_data.get('is_onboarded')}")
            
            if user_data.get("is_onboarded") is not False:
                 print("FAILURE: New user should have is_onboarded=False")
                 return False
            
            # 2. Login to get token
            print("2. Logging in...")
            login_response = await ac.post("/api/v1/login/access-token", data={
                "username": email,
                "password": password
            })
            if login_response.status_code != 200:
                print(f"FAILURE: Login failed. {login_response.text}")
                return False
                
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("   Login successful.")

            # 3. Check /me before onboarding
            print("3. Checking /me status...")
            me_response = await ac.get("/api/v1/users/me", headers=headers)
            if me_response.json().get("is_onboarded") is not False:
                print("FAILURE: /me returned is_onboarded=True prematurely.")
                return False
            print("   /me status confirmed: False")

            # 4. Complete Onboarding
            print("4. Calling POST /api/v1/users/onboarding...")
            onboard_response = await ac.post("/api/v1/users/onboarding", headers=headers)
            
            if onboard_response.status_code != 200:
                print(f"FAILURE: Onboarding endpoint failed. {onboard_response.text}")
                return False
            
            updated_user = onboard_response.json()
            print(f"   Response is_onboarded: {updated_user.get('is_onboarded')}")
            
            if updated_user.get("is_onboarded") is not True:
                print("FAILURE: Endpoint did not return is_onboarded=True")
                return False

            # 5. Verify persistence via /me
            print("5. Verifying persistence via /me...")
            me_response_2 = await ac.get("/api/v1/users/me", headers=headers)
            if me_response_2.json().get("is_onboarded") is not True:
                 print("FAILURE: Persistence check failed. /me still says False.")
                 return False
            
            print("SUCCESS: Story 2.3 Backend Validation Passed!")
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
