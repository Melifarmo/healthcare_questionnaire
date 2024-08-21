from sqlalchemy import VARCHAR, Column, Integer

from app.db.models.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, nullable=False)
    password_hash = Column(VARCHAR, nullable=False)
    password_salt = Column(VARCHAR, nullable=False)
