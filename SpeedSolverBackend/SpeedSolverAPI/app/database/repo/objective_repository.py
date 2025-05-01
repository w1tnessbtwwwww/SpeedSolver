from app.database.abstract.abc_repo import AbstractRepository
from app.database.models.models import Objective

class ObjectiveRepository(AbstractRepository):
    model = Objective