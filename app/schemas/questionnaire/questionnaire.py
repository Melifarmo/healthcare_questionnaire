from app.schemas.base_scheme import BaseScheme


class Questionnaire(BaseScheme):
    id: int

    name: str
    requires_period: bool
