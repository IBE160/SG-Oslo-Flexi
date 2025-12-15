from pydantic import BaseModel
import uuid
from typing import List

class QuestionBase(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
