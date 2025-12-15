from pydantic import BaseModel
from typing import List

class QuestionResult(BaseModel):
    id: int
    question: str
    user_answer: str
    correct_answer: str
    is_correct: bool

class QuizResultResponse(BaseModel):
    score: int
    total_questions: int
    questions: List[QuestionResult]

    class Config:
        orm_mode = True
