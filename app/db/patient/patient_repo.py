"""Subscription domain repository."""
from sqlalchemy import select, or_

from app.db.base_repository import BaseRepository
from app.db.patient.patient import PatientModel

from app.schemas.patient.patient import Patient
from app.schemas.patient.patient_in_creation import PatientInCreation


class PatientRepo(BaseRepository):
    model = PatientModel
    schema = Patient

    async def create_patient(self, patient_in_creation: PatientInCreation) -> Patient:
        row = await self._crud.create(model_data=patient_in_creation.dict())
        instance = await self._crud.get(pkey_val=row.id)
        return Patient.from_orm(instance)

    async def get_patients(self, query: str | None = None) -> list[Patient]:
        sql_request = select(self.model).\
            order_by(self.model.id.desc())

        if query:
            pattern = f'%{query}%'
            sql_request = sql_request.where(
                or_(
                    self.model.full_name.ilike(pattern),
                    self.model.phone.ilike(pattern),
                    self.model.passport_number.ilike(pattern),
                    self.model.email.ilike(pattern),
                )
            )

        rows = (await self._session.execute(sql_request)).scalars()
        return self._parse_to_schemas(rows)

    async def get(self, patient_id: int) -> Patient | None:
        return await self._crud.get(pkey_val=patient_id)
