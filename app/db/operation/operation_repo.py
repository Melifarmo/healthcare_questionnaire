"""Subscription domain repository."""
from sqlalchemy import select, or_

from app.db.base_repository import BaseRepository
from app.db.operation.operation import OperationModel
from app.db.patient.patient import PatientModel

from app.db.questionnaire.questionnaire import QuestionnaireModel
from app.schemas.operation.operation import Operation
from app.schemas.operation.operation_in_creation import OperationInCreation
from app.schemas.patient.patient import Patient
from app.schemas.patient.patient_in_creation import PatientInCreation
from app.schemas.questionnaire.questionnaire import Questionnaire


class OperationRepo(BaseRepository):
    model = OperationModel
    schema = Operation

    async def get_operation(self, patient_id: int) -> Operation | None:
        sql_request = select(self.model).where(
            self.model.patient_id == patient_id,
        ).limit(1)
        row = (await self._session.execute(sql_request)).scalar()
        return Operation.from_orm(row) if row else None

    async def create(self, operation: OperationInCreation) -> Patient:
        row = await self._crud.create(model_data=operation.dict())
        instance = await self._crud.get(pkey_val=row.id)
        return Operation.from_orm(instance)
