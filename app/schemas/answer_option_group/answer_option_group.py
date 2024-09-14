from app.schemas.answer_option.answer_option import AnswerOption
from app.schemas.base_scheme import BaseScheme


class AnswerOptionGroup(BaseScheme):
    id: int

    questionnaire_id: int
    name: str

    options: list[AnswerOption]
