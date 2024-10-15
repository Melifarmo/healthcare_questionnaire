"""Subscription domain repository."""
from sqlalchemy import select

from app.db.base_repository import BaseRepository

from app.db.questionnaire.questionnaire import QuestionnaireModel
from app.db.user.user import UserModel
from app.schemas.questionnaire.questionnaire import Questionnaire
from app.schemas.user.user import User


class UserRepo(BaseRepository):
    model = UserModel
    schema = User

    async def get_user(self, user_id: int) -> User | None:
        row = await self._crud.get(pkey_val=user_id)
        return User.from_orm(row) if row else None
