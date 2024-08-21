from sqlalchemy import VARCHAR, Column, Integer

from app.db.models.base import Base


class QuestionGroupModel(Base):
    __tablename__ = "question_groups"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False)
