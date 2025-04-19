from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import and_, select

from app.database.repo.team_project_repository import TeamProjectRepository
from app.utils.logger.telegram_bot.telegram_logger import logger
class TeamProjectService:
    def __init__(self, session):
        self.session = session
        self.repo = TeamProjectRepository(session)

    
    async def link_project(self, team_id: UUID, project_id: UUID):
        return await self.repo.create(teamId=team_id, projectId=project_id)
