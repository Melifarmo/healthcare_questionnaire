from app.schemas.base_scheme import BaseScheme


class QuestionsGroup(BaseScheme):
    id: int
    name: str
    questionnaire_id: int
