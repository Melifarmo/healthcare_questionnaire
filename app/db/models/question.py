from sqlalchemy import Boolean, Column, Enum, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.schemas.question.enum.question_type import QuestionType


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    answer_options_group_id = Column(Integer, ForeignKey("answer_options_groups.id"))

    text = Column(Text, nullable=False)
    type = Column(Enum(QuestionType, name='question_type'), nullable=False)  # type: ignore
    is_required = Column(Boolean, default=False)

    answer_options = relationship("AnswerOptionGroupModel", lazy='joined')
    question_groups = relationship(
        "QuestionGroupModel",
        secondary="question_groups_mapping",
        back_populates="questions"
    )
