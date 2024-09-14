from datetime import date

from app.schemas.base_scheme import BaseScheme


class PatientInCreation(BaseScheme):
    full_name: str
    birthday_date: date
    phone: str
    passport_number: str | None = None
    email: str | None = None
