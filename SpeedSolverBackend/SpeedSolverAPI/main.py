from fastapi import FastAPI

from app.cfg.settings import settings
from app.routing.main_router import main_router
from app.utils.email_service.email_service import EmailService

from starlette.middleware.cors import CORSMiddleware

from alembic.config import Config
from alembic import command

api = FastAPI(
    title="SpeedSolverAPI",
    description="The API docs for SpeedSolver.",
    version="v1",
)

api.add_middleware (
    CORSMiddleware,
    allow_origins=[
        "https://speedsolver.ru"
        "http://speedsolver.ru"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

api.include_router(main_router)


