

from app.database.repo.objective_repository import ObjectiveRepository


class ObjectiveService:
    def __init__(self, session):
        self._session = session
        self._repo = ObjectiveRepository(session)

    async def is_project_moderator(self, projectId: str, userId: str):
        await self._repo.is_project_moderator(projectId, userId)