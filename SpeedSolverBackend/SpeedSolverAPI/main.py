from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse as Redirect
from fastapi.staticfiles import StaticFiles

from app.database.database import get_session, create_tables
from app.exc.bad_email import BadEmail
from app.routing.main_router import main_router

from starlette.middleware.cors import CORSMiddleware


api = FastAPI(
    title="SpeedSolverAPI",
    description="The API docs for SpeedSolver.",
    version="v1",
)


api.add_middleware (
    CORSMiddleware,
    allow_origins=[
        "http://speedsolver.ru",
        "https://speedsolver.ru",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


api.include_router(main_router)

api.mount("/speedsolver-avatars", StaticFiles(directory="speedsolver-avatars"), name="avatars")

@api.exception_handler(BadEmail)
async def bad_email(request, exc: BadEmail):
    raise HTTPException(
        status_code=422,
        detail=exc.message
    )

@api.on_event("startup")
async def startup_event():
    await create_tables()