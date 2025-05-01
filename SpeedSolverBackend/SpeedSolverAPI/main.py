from datetime import datetime
import json
from typing import List
from uuid import UUID
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.responses import RedirectResponse as Redirect
from fastapi.staticfiles import StaticFiles

from app.database.database import get_session, create_tables
from app.database.models.models import User
from app.exc.bad_email import BadEmail
from app.routing.main_router import main_router

from starlette.middleware.cors import CORSMiddleware

from app.security.jwtmanager import get_current_user, native_current_user
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.project_service import ProjectService
from app.utils.websocket.events import WebSocketEvent

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

project_connections: dict[UUID, List[WebSocket]] = {}


@api.websocket("/ws/{token}/{project_id}")
async def websocket_endpoint(websocket: WebSocket, 
                             project_id: UUID, 
                             token: str, 
                             session: AsyncSession = Depends(get_session)):
    
    user = await native_current_user(token, session)

       # Проверка доступа пользователя к проекту
    # if not await ProjectService(session).is_user_project_member(project_id, user.id):
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    #     return

    await websocket.accept()

    # Добавляем подключение в список для данного project_id
    if project_id not in project_connections:
        project_connections[project_id] = []
    project_connections[project_id].append(websocket)

    full_name = ""


    for conn in project_connections[project_id]:


        if user.profile is None:
            full_name = "без ФИО"
        else:
            full_name = f"{user.profile.surname} {user.profile.name} {user.profile.patronymic}"
        await conn.send_text(json.dumps({
            "event": WebSocketEvent.JOIN.value,
            "user": full_name
        }))

    try:
        while True:
            data = await websocket.receive_text()
            # Отправляем сообщение всем подключенным клиентам в этом проекте
            for conn in project_connections[project_id]:
                if id(conn) != id(websocket):
                    send_data = {
                        "event": WebSocketEvent.MESSAGE.value,
                        "user": full_name,
                        "message": {
                            "text": json.loads(data)["msg"],
                            "created_at": str(datetime.now().strftime("%d.%m.%Y %H:%M:%S")),
                        }
                    }
                    await conn.send_text(json.dumps(send_data))
    except WebSocketDisconnect:
        # Удаляем подключение из списка при отключении
        project_connections[project_id].remove(websocket)
        if not project_connections[project_id]:
            del project_connections[project_id]