from sqlalchemy import VARCHAR, Boolean, Column, Integer
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class QuestionnaireModel(Base):
    __tablename__ = "questionnaires"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False)
    requires_period = Column(Boolean, nullable=False)

    questionnaire_items = relationship('QuestionnaireItemModel', lazy='joined')
