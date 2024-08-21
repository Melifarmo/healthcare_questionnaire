"""Base pydantic model."""
from pydantic import BaseModel


class BaseScheme(BaseModel):
    class Config:
        orm_mode = True
