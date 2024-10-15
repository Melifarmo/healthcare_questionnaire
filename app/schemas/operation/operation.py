from datetime import date

from app.schemas.base_scheme import BaseScheme


class Operation(BaseScheme):
    id: int
    patient_id: int
    operation_date: date
