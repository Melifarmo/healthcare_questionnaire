from sqlalchemy import Column, ForeignKey, Integer

from app.db.models.base import Base


class QuestionGroupMappingModel(Base):
    __tablename__ = "question_groups_mapping"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    question_group_id = Column(
        Integer,
        ForeignKey("question_groups.id", ondelete="RESTRICT"),
    )
    order = Column(Integer, nullable=False)
