from sqlalchemy import Boolean, Column, Enum, Integer, Text, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.schemas.question.enum.question_type import QuestionType


class OperationModel(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    patient_id = Column(Integer, ForeignKey("patients.id"))
    operation_date = Column(Date, nullable=False)
