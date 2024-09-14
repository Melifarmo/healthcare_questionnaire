from app.schemas.answer_option_group.answer_option_group import AnswerOptionGroup
from app.schemas.base_scheme import BaseScheme
from app.schemas.question.enum.question_type import QuestionType


class Question(BaseScheme):
    id: int
    answer_options_group_id: int
    text: str
    type: QuestionType
    is_required: bool

    answer_options: AnswerOptionGroup
