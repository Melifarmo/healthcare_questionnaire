from datetime import date

from app.schemas.base_scheme import BaseScheme


class Patient(BaseScheme):
    id: int

    full_name: str
    birthday_date: date
    phone: str
    passport_number: str | None
    email: str | None
