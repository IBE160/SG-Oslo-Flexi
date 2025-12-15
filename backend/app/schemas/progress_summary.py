from pydantic import BaseModel

class ProgressSummaryResponse(BaseModel):
    average_score: float
    total_quizzes: int

    class Config:
        orm_mode = True
