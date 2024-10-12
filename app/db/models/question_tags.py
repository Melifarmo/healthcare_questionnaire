from sqlalchemy import Column, Integer, ForeignKey, VARCHAR

from app.db.models.base import Base


class QuestionGroupTagModel(Base):
    __tablename__ = "question_group_tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    question_group_id = Column(Integer, ForeignKey("question_groups.id"))
    name = Column(VARCHAR, nullable=False)
