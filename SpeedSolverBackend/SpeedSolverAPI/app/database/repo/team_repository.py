from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Team
from sqlalchemy import select, update, delete, insert, and_, or_
from app.utils.result import Result, err, success

from app.utils.logger.telegram_bot.telegram_logger import logger
class TeamRepository(AbstractRepository):
    model: Team = Team


    async def create_team(self, 
                          title: str, 
                          description: str, 
                          leaderId: str, 
                          organizationId: str
                          ) -> Result[Team]:

        query = (
            select(self.model)
            .where(
                and_(
                    self.model.title == title,
                    self.model.leaderId == leaderId
                )
            )
        )

        result = await self._session.execute(query)
        team = result.scalars().first()

        if team:
            return err("У вас уже есть такая команда.")
        

        return success(value = await self.create(title=title, description=description, leaderId=leaderId, organizationId=organizationId))
    
    async def update_team(self, 
                          teamId: str, 
                          leaderId: str, 
                          new_title: str = None, 
                          new_description: str = None,
                          new_leader_id: str = None,
                          new_organization_id: str = None
                          ) -> Result[Team]:
        
        team: Team = await self.get_by_filter_one(teamId=teamId)
        
        query = (
            update(self.model)
            .where(and_(
                self.model.teamId == teamId,
                self.model.leaderId == leaderId
            )).values(
                title = new_title if new_title else team.title,
                description = new_description if new_description else team.description,
                leaderId = new_leader_id if new_leader_id else team.leaderId,
                organizationId = new_organization_id if new_organization_id else team.organizationId
            )
        )
        try:
            result = await self._session.execute(query)
            await self.commit()
        except Exception as e:
            logger.error(e)
            return err("Внутренняя ошибка сервера. Информация уже отправлена разработчику.")
        return success(result.scalars().first())