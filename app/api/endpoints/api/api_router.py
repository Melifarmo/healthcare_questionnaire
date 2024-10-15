from fastapi import APIRouter

from app.api.endpoints.api.answers_router import answers_router
from app.api.endpoints.api.dump_statistics import statistics_router
from app.api.endpoints.api.patients_router import patients_router

api_router = APIRouter(prefix='/api')
api_router.include_router(patients_router)
api_router.include_router(answers_router)
api_router.include_router(statistics_router)
