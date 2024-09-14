"""Configuration of routers for all endpoints."""
from fastapi import APIRouter

from app.api.endpoints.api import api_router
from app.api.endpoints.router import frontend_router

router = APIRouter()

router.include_router(frontend_router)
router.include_router(api_router)
