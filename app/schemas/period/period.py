from app.schemas.base_scheme import BaseScheme


class Period(BaseScheme):
    id: int

    name: str
    questionnaire_id: int
