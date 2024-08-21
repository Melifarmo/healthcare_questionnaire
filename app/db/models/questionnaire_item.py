from sqlalchemy import VARCHAR, Column, Enum, Integer

from app.db.models.base import Base
from app.schemas.question.enum.question_type import QuestionType


class QuestionnaireItemModel(Base):
    __tablename__ = "questionnaire_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    questionnaire_id = Column(VARCHAR, nullable=False)
    question_id = Column(Integer, nullable=True)
    question_group_id = Column(Integer, nullable=True)
    type = Column(Enum(QuestionType), nullable=False)  # type: ignore
    order = Column(Integer, nullable=False)
