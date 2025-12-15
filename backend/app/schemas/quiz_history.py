from pydantic import BaseModel
from datetime import datetime

class QuizHistoryItem(BaseModel):
    quiz_title: str
    score: int
    taken_at: datetime
