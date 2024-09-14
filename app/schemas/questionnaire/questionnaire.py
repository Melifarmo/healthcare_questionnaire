from app.schemas.base_scheme import BaseScheme
from app.schemas.questionnaire_item.questionnaire_item import QuestionnaireItem


class Questionnaire(BaseScheme):
    id: int

    name: str
    requires_period: bool

    questionnaire_items: list[QuestionnaireItem]
