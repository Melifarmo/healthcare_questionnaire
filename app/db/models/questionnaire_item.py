from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.schemas.questionnaire_item.enum.questionnaire_item_type import QuestionnaireItemType


class QuestionnaireItemModel(Base):
    __tablename__ = "questionnaire_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=True)
    question_group_id = Column(Integer, ForeignKey("question_groups.id", ondelete="CASCADE"), nullable=True)
    type = Column(Enum(QuestionnaireItemType, name='questionnaire_item_type'), nullable=False)
    order = Column(Integer, nullable=False)

    question = relationship("QuestionModel", lazy='joined')
    question_group = relationship("QuestionGroupModel", lazy='joined')
