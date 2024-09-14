from sqlalchemy import VARCHAR, Column, Integer
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class QuestionGroupModel(Base):
    __tablename__ = "question_groups"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False)

    # questions = relationship('QuestionModel', lazy='joined')
    questions = relationship(
        "QuestionModel",
        secondary="question_groups_mapping",
        lazy='joined',
        # back_populates="question_groups"
    )
