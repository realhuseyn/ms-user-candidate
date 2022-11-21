from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/health", tags=["Health Check"])
async def health():
    return ""


@health_router.get("/readiness", tags=["Health Check"])
async def readiness():
    return ""
