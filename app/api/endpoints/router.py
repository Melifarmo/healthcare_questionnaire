"""Endpoints for auth."""
from enum import Enum

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from fastapi import Request

from app.api.dependencies.db_session import get_session
from app.db.answer.answer_repo import PatientAnswerRepo
from app.db.patient.patient_repo import PatientRepo
from app.db.period.period_repo import PeriodRepo
from app.db.questionnaire.questionnaire_repo import QuestionnaireRepo
from app.schemas.answer_option.answer_option import AnswerOption
from app.schemas.patient_answer.patient_answer import PatientAnswer

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

from datetime import date


class HandsScore(BaseModel):
    left: float
    right: float
    operation_date: date


class FCounter:
    def count_functionality_group(self, answers) -> float:
        total_points = 0
        print(f'{len(answers) = }')
        for answer in answers:
            total_points += float(answer.value) * 5
            print(total_points)
        print('f')
        print(total_points)
        print('s')
        total_points = (-(total_points - 25) / 20) * 100
        print(total_points)
        return total_points

    def count_daily_activity_group(self, answers, both: bool = False) -> float:
        if both:
            total_points = 0
            for answer in answers:
                total_points += float(answer.value) * 5
            total_points = -(total_points - 25) / 20 * 100

        else:
            total_points = 0
            for answer in answers:
                total_points += float(answer.value) * 7
            total_points = -(total_points - 35) / 28 * 100

        return total_points

    def count_work_group(self, answers) -> float:
        total_points = 0
        for answer in answers:
            total_points += float(answer.value) * 5
        total_points = (total_points - 5) / 20 * 100
        return total_points

    def count_pain_group(self, answers) -> float:
        total_points = 0
        second_answer_value = float(answers.pop(0).value)
        if second_answer_value == 1:
            return 0

        total_points += (6 - second_answer_value) * 5

        for answer in answers:
            total_points += float(answer.value) * 5
        total_points = -(total_points - 25) * 100
        return total_points

    def count_aesthetics_group(
        self,
        answers: list,
    ) -> float:
        total_points = 0
        first_answer_value = float(answers.pop(0).value)

        total_points += (6 - first_answer_value) * 4
        for answer in answers:
            total_points += float(answer.value) * 4

        total_points = (total_points - 4) / 16 * 100
        return total_points

    def count_satisfaction_group(self, answers) -> float:
        total_points = 0
        for answer in answers:
            total_points += float(answer.value) * 6

        total_points = (-(total_points - 30))/24 * 100
        return total_points


class Hand(Enum):
    left = 'left'
    right = 'right'
    both = 'both'


class OrtoCounter:
    def __init__(self, db_session):
        self._db_session = db_session
        self._answer_repo = PatientAnswerRepo(db_session)
        self._patient_id: int | None = None
        self._period_id: int | None = None
        self._counter = FCounter()

    async def count(self, patient_id: int, period_id: int) -> HandsScore:
        self._patient_id = patient_id
        self._period_id = period_id
        hand = await self._get_hand_question()
        chosen_both = hand.option.text == 'Обе'

        print()
        for hand in [Hand.left, Hand.right]:
            # print(f'--- {hand.value}')
            # functionality_score = await self._count_functionality(hand)
            # print(f'Functionality {functionality_score}')

            # daily_activity_score = await self._count_daily_activity(hand, chosen_both)
            # print(f'Daily activity {daily_activity_score}')

            # work_score = await self._count_work()
            # print(f'Work {work_score}')
            #
            # pain_score = await self._count_pain()
            # print(f'Pain {pain_score}')

            aesthetics_score = await self._count_aesthetics(hand)
            print(f'Aesthetics {aesthetics_score}')

            # satisfaction_score = await self._count_satisfaction(hand)
            # print(f'Satisfaction {satisfaction_score}')

            total = sum([
                # functionality_score,
                # daily_activity_score,
                # work_score,
                # pain_score,
                aesthetics_score,
                # satisfaction_score,
            ])
            total = total / 6
            print(f'Total {total}')
            print()

        return HandsScore(
            left=4.32,
            right=1.2,
            operation_date=date(year=2024, month=5, day=15)
        )

    async def _get_hand_question(self) -> PatientAnswer:
        answers = await self._answer_repo.get_answers_by_tags(
            self._patient_id,
            self._period_id,
            tags=['hand'],
        )
        return answers[0]

    async def _count_functionality(self, hand: Hand) -> float:
        answers = await self._answer_repo.get_answers_by_tags(
            self._patient_id,
            self._period_id,
            tags=['functionality', hand.value],
        )
        return self._counter.count_functionality_group(self._convert_answers_to_options(answers))

    async def _count_daily_activity(self, hand: Hand, chosen_both: bool) -> float:
        answers = await self._answer_repo.get_answers_by_tags(
            self._patient_id,
            self._period_id,
            tags=['daily_activity', hand.value],
        )
        return self._counter.count_daily_activity_group(
            self._convert_answers_to_options(answers),
        )

    async def _count_work(self) -> float:
        answers = await self._answer_repo.get_answers_by_tags(
            self._patient_id,
            self._period_id,
            tags=['work', 'both'],
        )
        return self._counter.count_work_group(self._convert_answers_to_options(answers))

    async def _count_aesthetics(self, hand: Hand) -> float:
        answers = await self._answer_repo.get_answers_by_tags(
            self._patient_id,
            self._period_id,
            tags=['aesthetics', 'right'],
        )
        print(answers)
        return self._counter.count_aesthetics_group(self._convert_answers_to_options(answers))

    async def _count_satisfaction(self, hand: Hand) -> float:
        answers = await self._answer_repo.get_answers_by_tags(
            self._patient_id,
            self._period_id,
            tags=['satisfaction', hand.value],
        )
        return self._counter.count_satisfaction_group(self._convert_answers_to_options(answers))

    async def _count_pain(self) -> float:
        answers = await self._answer_repo.get_answers_by_tags(
            self._patient_id,
            self._period_id,
            tags=['pain'],
        )
        return self._counter.count_pain_group(self._convert_answers_to_options(answers))

    def _convert_answers_to_options(self, answers) -> list[AnswerOption]:
        return [answer.option for answer in answers]


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

    counter = OrtoCounter(db_session)
    for period in periods:
        has_answers = await patient_repo.is_answers(patient_id, period.id)
        hands_score = await counter.count(patient_id, period.id) if has_answers else None
        periods_data.append((period, hands_score))

    patient = await repo.get(patient_id)

    return templates.TemplateResponse("show_patient.html", context={
        "request": request,
        "patient": patient,
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
