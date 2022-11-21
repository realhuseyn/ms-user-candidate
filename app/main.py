import logging
import os
import warnings

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pymongo import MongoClient
from starlette.middleware.cors import CORSMiddleware

from app.controllers.controller.auth_controller import auth_router
from app.controllers.controller.candidate_controller import candidate_router
from app.controllers.controller.health_controller import health_router
from app.controllers.controller.user_controller import user_router
from app.utils.utils import create_default_user
from core.factories import settings

warnings.filterwarnings("ignore")
app = FastAPI()

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


async def modify_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.SERVICE_NAME,
        version=settings.API_VERSION,
        description="Microservice for user candidate",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.on_event("startup")
async def startup():
    await modify_openapi()
    print(f"app started with env {os.getenv('settings')}")
    app.mongodb_client = MongoClient(settings.DATABASE_URL)
    app.database = app.mongodb_client[settings.DB_NAME]
    await create_default_user()


@app.on_event("shutdown")
def shutdown():
    app.mongodb_client.close()
    print("SHUTDOWN")


cors_origins = [i.strip() for i in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/ms-user-candidate")
app.include_router(user_router, prefix="/ms-user-candidate")
app.include_router(candidate_router, prefix="/ms-user-candidate")
app.include_router(health_router)
