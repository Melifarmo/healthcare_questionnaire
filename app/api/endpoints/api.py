"""Endpoints for auth."""
from enum import Enum

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from app.api.dependencies.db_session import get_session
from app.db.answer.answer_repo import PatientAnswerRepo
from app.db.operation.operation_repo import OperationRepo
from app.db.patient.patient_repo import PatientRepo
from app.schemas.operation.operation_in_creation import OperationInCreation
from app.schemas.patient.patient import Patient
from app.schemas.patient.patient_in_creation import PatientInCreation
from app.schemas.patient_answer.enum.patient_answer_type import PatientAnswerType
from app.schemas.patient_answer.patient_answer_in_creation import PatientAnswerInCreation

api_router = APIRouter(prefix='/api')


@api_router.get('/patients')
async def get_patients(
    _: Request,
    query: str = None,
    sorting: str = None,
    db_session: AsyncSession = Depends(get_session),
) -> list[Patient]:
    repo = PatientRepo(db_session)

    patients = await repo.get_patients(query)
    return patients


@api_router.post('/patients/create', response_model=Patient)
async def create_patient(
    new_patient: PatientInCreation,
    db_session: AsyncSession = Depends(get_session),
) -> Patient:
    repo = PatientRepo(db_session)

    operation_repo = OperationRepo(db_session)
    patient = await repo.create_patient(new_patient)

    operation = OperationInCreation(
        patient_id=patient.id,
        operation_date=new_patient.operation_date,
    )
    await operation_repo.create(operation)

    return patient


@api_router.post('/patients/{patient_id}')
async def get_patients(
    patient_id: int,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Patient:
    repo = PatientRepo(db_session)

    patient = await repo.get(patient_id)
    return patient


class Answer(BaseModel):
    question_id: int
    option_id: int


# Модель для группы вопросов
class AnswerGroup(BaseModel):
    question_group_id: int
    questions: list[Answer]


class AnswersRequest(BaseModel):
    answers: list[AnswerGroup]
    patient_id: int = None
    period_id: int = None


@api_router.post('/answers/create')
async def save_answers(
    answers_request: AnswersRequest,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
):
    repo = PatientAnswerRepo(db_session)
    for answer_group in answers_request.answers:
        for answer in answer_group.questions:
            answer_in_creation = PatientAnswerInCreation(
                patient_id=answers_request.patient_id,
                question_id=answer.question_id,
                questionnaire_id=1,
                period_id=answers_request.period_id,
                answer_option_id=answer.option_id,
                answer=None,
                type=PatientAnswerType.option,
            )
            await repo.create(answer_in_creation)
    return
