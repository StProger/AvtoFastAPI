from sqladmin import ModelView

from app.cars.models import Cars
from app.users.models import Users


class UserAdmin(ModelView, model=Users):

    column_list = [Users.id, Users.login, Users.car]
    column_details_exclude_list = [Users.hashed_password]

    can_edit = False
    can_create = True
    can_delete = True
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"


class CarAdmin(ModelView, model=Cars):

    column_list = [Cars.id, Cars.number, Cars.name, Cars.color, Cars.user]
    can_delete = True
    can_create = False
    can_edit = False

    name = "Car"
    name_plural = "Cars"
    icon = "fa-solid fa-car"