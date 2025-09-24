from fastapi import APIRouter
from app.api.v1.endpoints import users, trips, upload, ai

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(trips.router, prefix="/trips", tags=["trips"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])