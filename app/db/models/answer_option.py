from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class AnswerOptionModel(Base):
    __tablename__ = "answer_options"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    text = Column(Text, nullable=False)
    value = Column(Integer, nullable=False)  # noqa: WPS110

    answer_option_group_id = Column(Integer, ForeignKey("answer_options_groups.id", ondelete="CASCADE"))

    # answers = relationship('PatientAnswerModel', back_populates='option', lazy='joined')
