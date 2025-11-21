"""
Main API router combining all endpoints
"""
from fastapi import APIRouter
from .jobs import router as jobs_router
from .candidates import router as candidates_router
from .matching import router as matching_router

api_router = APIRouter()

api_router.include_router(jobs_router)
api_router.include_router(candidates_router)
api_router.include_router(matching_router)