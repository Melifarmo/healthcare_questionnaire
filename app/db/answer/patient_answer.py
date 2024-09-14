from sqlalchemy import Column, Enum, ForeignKey, Integer, Text

from app.db.models.base import Base
from app.schemas.patient_answer.enum.patient_answer_type import PatientAnswerType


class PatientAnswerModel(Base):
    __tablename__ = "patient_answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="RESTRICT"))
    period_id = Column(Integer, ForeignKey("periods.id", ondelete="RESTRICT"))
    answer_option_id = Column(
        Integer,
        ForeignKey("answer_options.id", ondelete="RESTRICT"),
        nullable=True,
    )
    answer = Column(
        Text,
        ForeignKey("answer_options.id", ondelete="RESTRICT"),
        nullable=True,
    )
    type = Column(Enum(PatientAnswerType), nullable=False)  # type: ignore
