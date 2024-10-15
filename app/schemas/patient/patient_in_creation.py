from datetime import date

from pydantic import Field

from app.schemas.base_scheme import BaseScheme


class PatientInCreation(BaseScheme):
    full_name: str
    birthday_date: date
    phone: str
    passport_number: str | None = None
    email: str | None = None
    operation_date: date = Field(
        ...,
        exclude=True,
        title="operation_date"
    )
