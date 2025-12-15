from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.quiz_result import QuizResultResponse
from app.services.quiz_service import QuizService
import uuid
from typing import Dict

router = APIRouter()

@router.post("/{quiz_id}/submit", response_model=QuizResultResponse)
async def submit_quiz(
    quiz_id: int,
    answers: Dict[int, str],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Submit answers for a quiz and get the results.
    """
    #
    # In a real app, you would have a QuizService to handle the business logic
    #
    results = await QuizService.submit_quiz(db, quiz_id, current_user.id, answers)
    
    return results

