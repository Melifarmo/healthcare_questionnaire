from sqlalchemy import Boolean, Column, Enum, Integer, Text
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.schemas.question.enum.question_type import QuestionType


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)  # type: ignore
    is_required = Column(Boolean, default=False)

    answer_options = relationship("AnswerOption", back_populates="question")
