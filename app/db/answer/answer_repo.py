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
        row = await self._delete()
        row = await self._crud.create(model_data=answer_in_creation.dict())
        return await self._crud.get(pkey_val=row.id)

    async def get_list(self) -> list[Patient]:
        query = select(self.model)

        rows = (await self._session.execute(query)).scalars()
        return self._parse_to_schemas(rows)

    async def get(self, patient_id: int) -> Patient | None:
        return await self._crud.get(pkey_val=patient_id)

    async def _delete(self, period: int) -> Patient | None:
        query = delete(PatientAnswerModel).where(
            PatientAnswerModel.period_id ==,
        )