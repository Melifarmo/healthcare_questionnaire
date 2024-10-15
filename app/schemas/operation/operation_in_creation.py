
from datetime import date

from pydantic import BaseModel


class OperationInCreation(BaseModel):
    patient_id: int
    operation_date: date
