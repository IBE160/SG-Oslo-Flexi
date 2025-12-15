from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        password_hash=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_user_quiz_history(db: AsyncSession, user_id: int):
    from app.models.quiz_result import QuizResult
    from app.models.quiz import Quiz
    from app.schemas.quiz_history import QuizHistoryItem

    result = await db.execute(
        select(QuizResult.score, Quiz.title, QuizResult.created_at)
        .join(Quiz, QuizResult.quiz_id == Quiz.id)
        .where(QuizResult.user_id == user_id)
        .order_by(QuizResult.created_at.desc())
    )
    
    # Manually construct the response to match the Pydantic schema
    history = [
        QuizHistoryItem(
            quiz_title=row.title,
            score=row.score,
            taken_at=row.created_at
        ) for row in result.all()
    ]
    
    return history

async def get_user_progress_summary(db: AsyncSession, user_id: int):
    from app.models.quiz_result import QuizResult
    from sqlalchemy import func

    result = await db.execute(
        select(
            func.avg(QuizResult.score),
            func.count(QuizResult.id)
        )
        .where(QuizResult.user_id == user_id)
    )
    
    avg_score, total_quizzes = result.one_or_none() or (0, 0)

    return {
        "average_score": avg_score if avg_score is not None else 0,
        "total_quizzes": total_quizzes
    }

