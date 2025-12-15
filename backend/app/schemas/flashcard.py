from pydantic import BaseModel
import uuid

class FlashcardBase(BaseModel):
    question: str
    answer: str

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardResponse(FlashcardBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
