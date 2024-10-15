"""Endpoints for auth."""
import io
import string

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from starlette.responses import StreamingResponse

from app.api.dependencies.db_session import get_session
from app.db.answer.answer_repo import PatientAnswerRepo
from app.db.operation.operation_repo import OperationRepo
from app.db.patient.patient_repo import PatientRepo
from app.db.period.period_repo import PeriodRepo
from app.schemas.mhq.hands_score import HandsScore
from app.schemas.patient.patient import Patient
from app.services.MHQ.hand_score_counter import HandScoreCounter

"""Service for building contacts dump in excel."""

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

DEFAULT_SHEET_NAME = "Лист1"
COLUMN_WIDTH = 15

statistics_router = APIRouter(prefix='/statistics')


@statistics_router.get('/excel')
async def dump_statistic_to_excel(
    _: Request,
    user_id: int = None,
    db_session: AsyncSession = Depends(get_session),
) -> StreamingResponse:
    patient_repo = PatientRepo(db_session)
    patients = await patient_repo.get_patients()

    excel_file = await create_excel_file(patients, db_session)

    response = StreamingResponse(
        iter([excel_file.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response.headers["Content-Disposition"] = "attachment; filename=statistics.xlsx"
    return response


async def create_excel_file(patients: list[Patient], db_session) -> io.BytesIO:
    """Создает файл Excel и возвращает его как объект BytesIO."""
    workbook = Workbook()
    default_sheet = workbook["Sheet"]
    assert isinstance(default_sheet, Worksheet)
    workbook.remove(default_sheet)

    workbook.create_sheet(DEFAULT_SHEET_NAME)
    sheet = workbook[DEFAULT_SHEET_NAME]
    assert isinstance(sheet, Worksheet)

    _setup_columns(sheet=sheet)
    await _insert_contacts_data(sheet, patients, db_session)

    excel_buffer = io.BytesIO()
    workbook.save(excel_buffer)
    excel_buffer.seek(0)
    return excel_buffer


def _setup_columns(sheet: Worksheet) -> None:
    """Set columns for vacation data."""
    for index, header in enumerate([
        'ФИО',
        'Дата рождения',
        'Телефон',
        'Почта',
        'Дата операции',
        'До операции, левая',
        'До операции, правая',
        'После операции, левая',
        'После операции, правая',
        'Месяц, левая',
        'Месяц, правая',
        '3 месяца, левая',
        '3 месяца, правая',
        'Пол года, левая',
        'Пол года, правая',
        'Год, левая',
        'Год, правая',
    ]):
        letter = string.ascii_uppercase[index]
        sheet.column_dimensions[letter].width = COLUMN_WIDTH
        sheet[f"{letter}1"] = header


def _parse_period(period_data: dict, period: str, left_before: bool = True) -> HandsScore | None:
    if not period_data.get(period):
        return None
    return period_data[period].left if left_before else period_data[period].right


async def _insert_contacts_data(
        sheet: Worksheet,
        patients: list[Patient],
        db_session: AsyncSession,
) -> None:
    """Insert contacts data to table in selected sheet."""
    periods = await (PeriodRepo(db_session).get_periods())
    patient_repo = PatientAnswerRepo(db_session)
    for index, patient in enumerate(patients, start=2):
        periods_data = {}

        counter = HandScoreCounter(db_session)
        for period in periods:
            has_answers = await patient_repo.has_answers(patient.id, period.id)
            hands_score = await counter.count(patient.id, period.id) if has_answers else None
            periods_data[period.name] = hands_score

        operation = await (OperationRepo(db_session).get_operation(patient.id))

        sheet[f"A{index}"] = patient.full_name
        sheet[f"B{index}"] = patient.birthday_date
        sheet[f"C{index}"] = patient.phone
        sheet[f"D{index}"] = patient.email if patient.email else ''
        sheet[f"E{index}"] = operation.operation_date if operation else None

        sheet[f"F{index}"] = _parse_period(periods_data, 'до операции')
        sheet[f"G{index}"] = _parse_period(periods_data, 'до операции', False)

        sheet[f"H{index}"] = _parse_period(periods_data, 'после операции')
        sheet[f"I{index}"] = _parse_period(periods_data, 'после операции', False)

        sheet[f"J{index}"] = _parse_period(periods_data, 'месяц')
        sheet[f"K{index}"] = _parse_period(periods_data, 'месяц', False)

        sheet[f"L{index}"] = _parse_period(periods_data, '3 месяца')
        sheet[f"M{index}"] = _parse_period(periods_data, '3 месяца', False)

        sheet[f"N{index}"] = _parse_period(periods_data, 'пол года')
        sheet[f"O{index}"] = _parse_period(periods_data, 'пол года', False)

        sheet[f"N{index}"] = _parse_period(periods_data, 'год')
        sheet[f"O{index}"] = _parse_period(periods_data, 'год', False)
