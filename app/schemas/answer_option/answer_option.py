from app.schemas.base_scheme import BaseScheme


class AnswerOption(BaseScheme):
    id: int

    answer_option_group_id: int
    text: str
    value: str  # noqa: WPS110
