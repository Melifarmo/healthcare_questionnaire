from sqlalchemy import VARCHAR, Column, Integer

from app.db.models.base import Base


class PeriodModel(Base):
    __tablename__ = "periods"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False)
    questionnaire_id = Column(Integer, nullable=False)
