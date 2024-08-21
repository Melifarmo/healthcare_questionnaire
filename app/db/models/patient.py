from sqlalchemy import VARCHAR, Column, Date, Integer

from app.db.models.base import Base


class PatientModel(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(VARCHAR, nullable=False)
    birthday_date = Column(Date, nullable=False)
    phone = Column(VARCHAR, nullable=False)
    password_number = Column(VARCHAR, nullable=True)
    email = Column(VARCHAR, nullable=True)
