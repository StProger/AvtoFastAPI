from fastapi import APIRouter


router = APIRouter(prefix="/cars", tags=["cars"])


@router.post("")
async def add_car():
    ...