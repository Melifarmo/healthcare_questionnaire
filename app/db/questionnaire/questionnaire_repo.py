"""Subscription domain repository."""
from sqlalchemy import select

from app.db.base_repository import BaseRepository

from app.db.questionnaire.questionnaire import QuestionnaireModel
from app.schemas.questionnaire.questionnaire import Questionnaire


class QuestionnaireRepo(BaseRepository):
    model = QuestionnaireModel
    schema = Questionnaire

    async def get_questionnaire(self, questionnaire_id: int) -> Questionnaire | None:
        query = select(QuestionnaireModel).where(
            QuestionnaireModel.id == questionnaire_id,
        )
        instance_in_db = (await self._session.execute(query)).scalar()
        return Questionnaire.from_orm(instance_in_db) if instance_in_db else None
