from app.schemas.base_scheme import BaseScheme
from app.schemas.question.question import Question


class QuestionsGroup(BaseScheme):
    id: int
    name: str

    questions: list[Question]
