from fastapi import APIRouter
from settings import settings

router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/app")
async def ping_app():
    return {
        "token": settings.GOOGLE_TOKEN_ID
    }
