from sqlalchemy import Column, ForeignKey, Integer, VARCHAR
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class AnswerOptionGroupModel(Base):
    __tablename__ = "answer_options_groups"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id", ondelete="CASCADE"), nullable=False)

    name = Column(VARCHAR(), nullable=False)

    options = relationship("AnswerOptionModel", lazy="joined")
