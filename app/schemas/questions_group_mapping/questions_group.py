from app.schemas.base_scheme import BaseScheme


class QuestionsGroupMapping(BaseScheme):
    id: int
    question_id: int
    question_group_id: int
    order: int
