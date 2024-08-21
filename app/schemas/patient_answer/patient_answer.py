from app.schemas.base_scheme import BaseScheme
from app.schemas.patient_answer.enum.patient_answer_type import PatientAnswerType


class PatientAnswer(BaseScheme):
    id: int

    patient_id: int
    question_id: int
    questionnaire_id: int
    period_id: int | None

    answer_option_id: int | None
    answer: str | None
    type: PatientAnswerType
