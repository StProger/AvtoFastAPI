from sqlalchemy import insert, select, delete, update

from app.db import async_session_maker


class BaseDAO:

    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):

        async with async_session_maker() as session:

            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):

        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)

            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_(cls, **data):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_(cls, model_id, **data):
        async with async_session_maker() as session:

            query = update(cls.model).where(cls.model.c.id == model_id).values(**data)