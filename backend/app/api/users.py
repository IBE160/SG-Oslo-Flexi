from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponseWrapper, UserResponse
from app.services import user as user_service
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.quiz_history import QuizHistoryItem
from app.schemas.progress_summary import ProgressSummaryResponse
from typing import List

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



@router.get("/me/quiz-history", response_model=List[QuizHistoryItem], status_code=status.HTTP_200_OK)

async def get_quiz_history(

    current_user: Annotated[User, Depends(get_current_user)],

    db: AsyncSession = Depends(get_db)

):

    """

    Retrieve the quiz history for the current user.

    """

    return await user_service.get_user_quiz_history(db, current_user.id)

@router.get("/me/progress-summary", response_model=ProgressSummaryResponse, status_code=status.HTTP_200_OK)
async def get_progress_summary(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve the progress summary for the current user.
    """
    return await user_service.get_user_progress_summary(db, current_user.id)
