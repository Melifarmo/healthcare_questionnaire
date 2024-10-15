"""Endpoints for auth."""
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from app.api.dependencies.db_session import get_session
from app.db.answer.answer_repo import PatientAnswerRepo
from app.schemas.answers_request import AnswersRequest
from app.schemas.patient_answer.enum.patient_answer_type import PatientAnswerType
from app.schemas.patient_answer.patient_answer_in_creation import PatientAnswerInCreation


answers_router = APIRouter(prefix='/answers')


@answers_router.post('/create')
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
