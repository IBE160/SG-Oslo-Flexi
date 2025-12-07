from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponseWrapper
from app.services import user as user_service

router = APIRouter()

@router.post("/register", response_model=UserResponseWrapper, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    existing_user = await user_service.get_user_by_email(db, user_in.email)
    if existing_user:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": {
                    "message": "User with this email already exists",
                    "code": "USER_EXISTS"
                }
            }
        )
    
    # Create user
    user = await user_service.create_user(db, user_in)
    
    return {"data": user}
