from pydantic import BaseModel


class Answer(BaseModel):
    question_id: int
    option_id: int


class AnswerGroup(BaseModel):
    question_group_id: int
    questions: list[Answer]


class AnswersRequest(BaseModel):
    answers: list[AnswerGroup]
    patient_id: int = None
    period_id: int = None
