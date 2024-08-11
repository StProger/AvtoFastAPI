from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
from sqladmin import Admin

from prometheus_fastapi_instrumentator import Instrumentator

from redis import asyncio as aioredis

from app.db import delete_tables, create_tables, engine
from app.users.router import router as user_router
from app.cars.router import router as car_router
from app.prometheus.router import router as prometheus_router
from app.config import settings
from app.admin.auth import authentication_backend
from app.admin.views import UserAdmin, CarAdmin
from app.logging import setup

@asynccontextmanager
async def lifespan(app: FastAPI):

    await delete_tables()
    await create_tables()
    redis = aioredis.from_url(settings.redis_url, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(car_router)
app.include_router(prometheus_router)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)

# Подключаем эндпоинт для сбора метрик
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)

instrumentator.instrument(app).expose(app)


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(CarAdmin)


