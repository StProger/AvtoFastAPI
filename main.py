from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from app.db import delete_tables, create_tables
from app.users.router import router as user_router
from app.cars.router import router as car_router
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):

    await delete_tables()
    await create_tables()
    redis = aioredis.from_url(settings.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(car_router)