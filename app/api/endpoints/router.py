"""Endpoints for auth."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from fastapi import Request

from app.api.dependencies.db_session import get_session
from app.db.answer.answer_repo import PatientAnswerRepo
from app.db.operation.operation_repo import OperationRepo
from app.db.patient.patient_repo import PatientRepo
from app.db.period.period_repo import PeriodRepo
from app.db.questionnaire.questionnaire_repo import QuestionnaireRepo
from app.services.MHQ.hand_score_counter import HandScoreCounter

frontend_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@frontend_router.get('/')
async def main_page(
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> HTMLResponse:
    return templates.TemplateResponse("main.html", context={"request": request})


@frontend_router.get('/patients/add')
async def add_patient_page(
    request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse("create_patient.html", context={"request": request})


@frontend_router.get('/patients/{patient_id}')
async def patient_get(
    patient_id: int,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> HTMLResponse:
    repo = PatientRepo(db_session)
    repo_periods = PeriodRepo(db_session)
    patient_repo = PatientAnswerRepo(db_session)

    periods = await repo_periods.get_periods()
    periods_data = []

    counter = HandScoreCounter(db_session)
    for period in periods:
        has_answers = await patient_repo.has_answers(patient_id, period.id)
        hands_score = await counter.count(patient_id, period.id) if has_answers else None
        periods_data.append((period, hands_score))

    patient = await repo.get(patient_id)

    operation_repo = OperationRepo(db_session)
    operation = await operation_repo.get_operation(patient_id)
    print(operation, patient_id)
    return templates.TemplateResponse("show_patient.html", context={
        "request": request,
        "patient": patient,
        "operation": operation,
        "periods": periods_data,
    })


@frontend_router.get('/patients/{patient_id}/period/{period_id}/questionnaire/create')
async def create_questionnaire(
    patient_id: int,
    period_id: int,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> HTMLResponse:
    questionnaire_id = 1
    patient = await PatientRepo(db_session).get(patient_id)
    period = await PeriodRepo(db_session).get(period_id)

    repo = QuestionnaireRepo(db_session)
    questionnaire = await repo.get_questionnaire(questionnaire_id)
    groups = [item.question_group for item in questionnaire.questionnaire_items]

    return templates.TemplateResponse("fill_questionnaire.html", context={
        "request": request,
        "groups": groups,
        "period": period,
        "patient": patient,
    })
