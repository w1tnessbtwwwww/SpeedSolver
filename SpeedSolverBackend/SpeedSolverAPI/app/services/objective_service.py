

from app.database.repo.objective_repository import ObjectiveRepository
from app.schema.request.objective.create_objective import CreateObjective
from app.services.project_service import ProjectService
from app.utils.result import err, success


class ObjectiveService:
    def __init__(self, session):
        self._session = session
        self._repo = ObjectiveRepository(session)

    async def create_objective(self, project_id: str, author_id: str, create_objective: CreateObjective):
        project_service = ProjectService(self._session)

        can_interract = await project_service.is_project_moderator(project_id, author_id)

        if not can_interract.success:
            return err(can_interract.error)
        
        created_objective = await self._repo.create(
            projectId=project_id,
            title=create_objective.title,
            description=create_objective.description,
            parent_objectiveId=create_objective.depends_on,
            deadline_date=create_objective.deadline,
            author_id=author_id
        )
        
        return success(created_objective)