from sqlalchemy.ext.asyncio import AsyncSession
from app.models.quiz import Quiz
from app.models.quiz_result import QuizResult
from app.schemas.quiz_result import QuizResultResponse, QuestionResult
from typing import Dict
from uuid import UUID
from fastapi import HTTPException, status

class QuizService:
    @staticmethod
    async def submit_quiz(db: AsyncSession, quiz_id: int, user_id: UUID, answers: Dict[int, str]) -> QuizResultResponse:
        quiz = await db.get(Quiz, quiz_id)
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

        score = 0
        question_results = []
        for question in quiz.questions:
            user_answer = answers.get(str(question.id))
            is_correct = user_answer == question.correct_answer
            if is_correct:
                score += 1
            
            question_results.append(QuestionResult(
                id=question.id,
                question=question.question,
                user_answer=user_answer,
                correct_answer=question.correct_answer,
                is_correct=is_correct,
            ))

        # Save the result to the database
        quiz_result = QuizResult(
            quiz_id=quiz_id,
            user_id=user_id,
            score=score,
            answers=answers
        )
        db.add(quiz_result)
        await db.commit()

        return QuizResultResponse(
            score=score,
            total_questions=len(quiz.questions),
            questions=question_results,
        )
