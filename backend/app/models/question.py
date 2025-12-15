from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String, nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
