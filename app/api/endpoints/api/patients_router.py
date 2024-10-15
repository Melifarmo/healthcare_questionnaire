"""Endpoints for auth."""
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from app.api.dependencies.db_session import get_session
from app.db.patient.patient_repo import PatientRepo
from app.schemas.patient.patient import Patient
from app.schemas.patient.patient_in_creation import PatientInCreation

patients_router = APIRouter(prefix='/patients')


@patients_router.get('/')
async def get_patients(
    _: Request,
    query: str = None,
    db_session: AsyncSession = Depends(get_session),
) -> list[Patient]:
    repo = PatientRepo(db_session)

    patients = await repo.get_patients(query)
    return patients


@patients_router.post('/create', response_model=Patient)
async def create_patient(
    new_patient: PatientInCreation,
    db_session: AsyncSession = Depends(get_session),
) -> Patient:
    repo = PatientRepo(db_session)

    patient = await repo.create_patient(new_patient)
    return patient


@patients_router.post('/{patient_id}')
async def get_patient(
    patient_id: int,
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Patient:
    repo = PatientRepo(db_session)

    patient = await repo.get(patient_id)
    return patient
