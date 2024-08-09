from sqlalchemy import select

from app.dao.base import BaseDAO
from app.cars.models import Cars
from app.db import async_session_maker


class CarsDAO(BaseDAO):

    model = Cars

    @classmethod
    async def find_by_number(cls, number: str):

        async with async_session_maker() as session:

            query = select(Cars).filter_by(number=number)
            result = await session.execute(query)
            return result.one_or_none()
