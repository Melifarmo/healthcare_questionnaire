from datetime import date

from pydantic import BaseModel


class HandsScore(BaseModel):
    left: float
    right: float
