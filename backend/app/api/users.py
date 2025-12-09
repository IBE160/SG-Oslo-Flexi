from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponseWrapper, UserResponse
from app.services import user as user_service
from app.core.config import settings
from app.models.user import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login/access-token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = uuid.UUID(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

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

@router.post("/onboarding", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def complete_onboarding(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    current_user.is_onboarded = True
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user