from app.dao.base import BaseDAO
from app.cars.models import Cars


class CarsDAO(BaseDAO):

    model = Cars
