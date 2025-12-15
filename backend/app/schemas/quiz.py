from pydantic import BaseModel
import uuid
from typing import List
from .question import QuestionResponse

class QuizBase(BaseModel):
    title: str

class QuizCreate(QuizBase):
    pass

class QuizResponse(QuizBase):
    id: uuid.UUID
    questions: List[QuestionResponse] = []

    class Config:
        orm_mode = True
