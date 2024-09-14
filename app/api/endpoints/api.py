"""Endpoints for auth."""
import json
from typing import Any

from fastapi import APIRouter, Depends
from httpx import HTTPError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from app.api.dependencies.db_session import get_session
from app.db.answer.answer_repo import PatientAnswerRepo
from app.db.patient.patient_repo import PatientRepo
from app.db.period.period_repo import PeriodRepo
from app.schemas.patient.patient import Patient
from app.schemas.patient.patient_in_creation import PatientInCreation
from app.schemas.patient_answer.enum.patient_answer_type import PatientAnswerType
from app.schemas.patient_answer.patient_answer_in_creation import PatientAnswerInCreation
from app.schemas.period.period import Period

api_router = APIRouter(prefix='/api')


@api_router.get('/patients')
async def get_patients(
    _: Request,
    db_session: AsyncSession = Depends(get_session),
) -> list[Patient]:
    repo = PatientRepo(db_session)

    patients = await repo.get_patients()
    return patients


@api_router.post('/patients/create')
async def create_patient(
    new_patient: PatientInCreation,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Patient:
    repo = PatientRepo(db_session)

    patient = await repo.create_patient(new_patient)
    return patient


@api_router.post('/patients/{patient_id}')
async def get_patient(
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
async def get_patient(
    answers_request: AnswersRequest,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
):
    repo = PatientAnswerRepo(db_session)
    for answer_group in answers_request.answers:
        for answer in answer_group.answers:
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

    # d = await request.body()
    # d = d.decode('utf-8')
    # c = json.loads(d)
    # print(c)
    return
