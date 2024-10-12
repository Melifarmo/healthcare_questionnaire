from sqlalchemy import Column, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.schemas.patient_answer.enum.patient_answer_type import PatientAnswerType


class PatientAnswerModel(Base):
    __tablename__ = "patient_answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="RESTRICT"))
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="RESTRICT"))
    questionnaire_id = Column(Integer, ForeignKey("questionnaires.id", ondelete="RESTRICT"))
    period_id = Column(Integer, ForeignKey("periods.id", ondelete="RESTRICT"))
    answer_option_id = Column(
        Integer,
        ForeignKey("answer_options.id", ondelete="RESTRICT"),
        nullable=True,
    )
    answer = Column(
        Text,
        nullable=True,
    )
    type = Column(Enum(PatientAnswerType, name='patient_answer_type'), nullable=False)  # type: ignore

    option = relationship('AnswerOptionModel', lazy='joined', foreign_keys=[answer_option_id])
