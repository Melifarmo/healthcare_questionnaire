from app.schemas.base_scheme import BaseScheme


class User(BaseScheme):
    id: int
    full_name: str
    email: str
    password_hash: str
    password_salt: str
