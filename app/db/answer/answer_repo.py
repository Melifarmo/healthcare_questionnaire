"""Subscription domain repository."""
from sqlalchemy import select, delete

from app.db.answer.patient_answer import PatientAnswerModel
from app.db.base_repository import BaseRepository
from app.db.models import QuestionModel, QuestionGroupModel, QuestionGroupMappingModel
from app.db.models.question_tags import QuestionGroupTagModel
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

    async def get_answers(self, patient_id: int, period_id: int) -> list[PatientAnswer]:
        query = select(self.model).\
            where(self.model.patient_id == patient_id).\
            where(self.model.period_id == period_id)

        rows = (await self._session.execute(query)).scalars()
        return self._parse_to_schemas(rows)

    async def get_answers_by_tags(
        self,
        patient_id: int,
        period_id: int,
        tags: list[str],
    ) -> list[PatientAnswer]:
        query = select(self.model).\
            join(QuestionModel, QuestionModel.id == self.model.question_id).\
            join(QuestionGroupMappingModel, QuestionGroupMappingModel.question_id == QuestionModel.id).\
            join(QuestionGroupModel, QuestionGroupModel.id == QuestionGroupMappingModel.question_group_id).\
            join(QuestionGroupTagModel, QuestionGroupTagModel.question_group_id == QuestionGroupModel.id).\
            where(self.model.patient_id == patient_id).\
            where(self.model.period_id == period_id)

        ws = []
        for tag in tags:
            print(tag)
            ws.append(QuestionGroupTagModel.name == tag)
        query = query.where(*ws)

        rows = (await self._session.execute(query)).scalars()
        return self._parse_to_schemas(rows)

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
