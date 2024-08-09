from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import delete_tables, create_tables
from app.users.router import router as user_router
from app.cars.router import router as car_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    await delete_tables()
    await create_tables()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(car_router)