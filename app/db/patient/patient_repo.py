"""Subscription domain repository."""
from sqlalchemy import select

from app.db.base_repository import BaseRepository
from app.db.patient.patient import PatientModel

from app.db.questionnaire.questionnaire import QuestionnaireModel
from app.schemas.patient.patient import Patient
from app.schemas.patient.patient_in_creation import PatientInCreation
from app.schemas.questionnaire.questionnaire import Questionnaire


class PatientRepo(BaseRepository):
    model = PatientModel
    schema = Patient

    async def create_patient(self, patient_in_creation: PatientInCreation) -> Patient:
        row = await self._crud.create(model_data=patient_in_creation.dict())
        return await self._crud.get(pkey_val=row.id)

    async def get_patients(self) -> list[Patient]:
        query = select(self.model)

        rows = (await self._session.execute(query)).scalars()
        return self._parse_to_schemas(rows)

    async def get(self, patient_id: int) -> Patient | None:
        return await self._crud.get(pkey_val=patient_id)
