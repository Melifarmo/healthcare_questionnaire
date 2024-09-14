from app.schemas.base_scheme import BaseScheme
from app.schemas.question.question import Question
from app.schemas.questionnaire_item.enum.questionnaire_item_type import (
    QuestionnaireItemType,
)
from app.schemas.questions_group.questions_group import QuestionsGroup


class QuestionnaireItem(BaseScheme):
    id: int

    questionnaire_id: int
    question_id: int | None
    question_group_id: int | None
    type: QuestionnaireItemType
    order: int

    # question: Question | None
    question_group: QuestionsGroup | None
