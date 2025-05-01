from sqladmin import ModelView

from app.database.models.models import Team, User

class UserAdmin(ModelView, model=User):
    column_list=[User.email]