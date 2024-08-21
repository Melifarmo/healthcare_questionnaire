from app.schemas.base_scheme import BaseScheme
from app.schemas.question.enum.question_type import QuestionType


class Question(BaseScheme):
    id: int
    text: str
    type: QuestionType
    is_required: bool
