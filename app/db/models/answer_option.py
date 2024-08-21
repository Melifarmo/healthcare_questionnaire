from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class AnswerOptionModel(Base):
    __tablename__ = "answer_options"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))

    text = Column(Text, nullable=False)
    value = Column(Integer, nullable=False)  # noqa: WPS110

    question = relationship("Question", back_populates="answer_options")
