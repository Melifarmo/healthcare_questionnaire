"""Subscription domain repository."""
from sqlalchemy import select, delete

from app.db.answer.patient_answer import PatientAnswerModel
from app.db.base_repository import BaseRepository
from app.db.patient.patient import PatientModel

from app.db.questionnaire.questionnaire import QuestionnaireModel
from app.schemas.patient.patient import Patient
from app.schemas.patient.patient_in_creation import PatientInCreation
from app.schemas.patient_answer.patient_answer import PatientAnswer
from app.schemas.patient_answer.patient_answer_in_creation import PatientAnswerInCreation
from app.schemas.questionnaire.questionnaire import Questionnaire


class PatientAnswerRepo(BaseRepository):
    model = PatientAnswerModel
    schema = PatientAnswer

    async def create(self, answer_in_creation: PatientAnswerInCreation) -> Patient:
        await self._delete(
            period_id=answer_in_creation.period_id,
            question_id=answer_in_creation.question_id,
        )
        row = await self._crud.create(model_data=answer_in_creation.dict())
        return await self._crud.get(pkey_val=row.id)

    async def get_list(self) -> list[Patient]:
        query = select(self.model)

        rows = (await self._session.execute(query)).scalars()
        return self._parse_to_schemas(rows)

    async def is_answers(
            self,
            patient_id: int,
            period_id: int,
    ) -> bool:
        query = select(PatientAnswerModel).where(
            PatientAnswerModel.period_id == period_id,
            PatientAnswerModel.patient_id == patient_id,
        )
        instance = (await self._session.execute(query)).scalar()
        return bool(instance)

    async def _delete(self, period_id: int, question_id: int) -> None:
        query = delete(PatientAnswerModel).where(
            PatientAnswerModel.period_id == period_id,
            PatientAnswerModel.question_id == question_id,
        )
        await self._session.execute(query)
