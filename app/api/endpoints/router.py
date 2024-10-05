"""Endpoints for auth."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from fastapi import Request

from app.api.dependencies.db_session import get_session
from app.db.answer.answer_repo import PatientAnswerRepo
from app.db.patient.patient_repo import PatientRepo
from app.db.period.period_repo import PeriodRepo
from app.db.questionnaire.questionnaire_repo import QuestionnaireRepo

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
    d = []
    for period in periods:
        is_answers = await patient_repo.is_answers(patient_id, period.id)
        d.append((period, is_answers))

    patient = await repo.get(patient_id)

    return templates.TemplateResponse("show_patient.html", context={
        "request": request,
        "patient": patient,
        "periods": d,
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
        "groups": groups[:2],
        "period": period,
        "patient": patient,
    })
