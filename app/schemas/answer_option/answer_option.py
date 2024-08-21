from app.schemas.base_scheme import BaseScheme


class AnswerOption(BaseScheme):
    id: int

    question_id: int
    text: str
    value: str  # noqa: WPS110
