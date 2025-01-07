from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.cfg.settings import settings
from app.database.database import get_session
from app.exc.bad_email import BadEmail
from app.routing.main_router import main_router
from app.utils.email_service.email_service import EmailService

from starlette.middleware.cors import CORSMiddleware

from typing import Annotated
from sqlalchemy.orm import Session
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
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


api.include_router(main_router)


@api.exception_handler(BadEmail)
async def bad_email(request, exc: BadEmail):
    raise HTTPException(
        status_code=422,
        detail=exc.message
    )

