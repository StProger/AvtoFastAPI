from fastapi import APIRouter, Depends

import re

from app.cars.schemas import SCars
from app.cars.dao import CarsDAO
from app.exceptions import CarAlreadyExists, InvalidCarNumber
from app.users.models import Users
from app.users.dependencies import get_current_user


number_pattern = r'^[А-Я]\d{3}[А-Я]{2}$'

router = APIRouter(prefix="/cars", tags=["cars"])


@router.post("", description="Добавление машины")
async def add_car(car: SCars, user: Users = Depends(get_current_user)):

    match_ = re.match(number_pattern, car.number.upper())
    print(match_)
    if not match_:
        raise InvalidCarNumber

    already_car = await CarsDAO.find_by_number(car.number, user.id)
    if already_car:
        raise CarAlreadyExists
    await CarsDAO.add(name=car.name, number=car.number, user_id=user.id)
