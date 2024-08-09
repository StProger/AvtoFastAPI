from fastapi import APIRouter, Depends

import re

from app.cars.schemas import SCars
from app.cars.dao import CarsDAO
from app.exceptions import CarAlreadyExists, InvalidCarNumber, CarNotFound
from app.users.models import Users
from app.users.dependencies import get_current_user


number_pattern = r'^[А-Я]\d{3}[А-Я]{2}$'

router = APIRouter(prefix="/cars", tags=["cars"])


@router.post("", description="Добавление машины")
async def add_car(car: SCars, user: Users = Depends(get_current_user)):

    match_ = re.match(number_pattern, car.number.upper())
    if not match_:
        raise InvalidCarNumber

    already_car = await CarsDAO.find_by_number(car.number)
    if already_car:
        raise CarAlreadyExists
    await CarsDAO.add(name=car.name, number=car.number.upper(), user_id=user.id)


@router.get("", description="Получение всех машин")
async def get_cars(user: Users = Depends(get_current_user)) -> list[SCars]:

    cars = await CarsDAO.find_all(user_id=user.id)

    return cars


@router.get("/{car_id}", description="Получение автомобиля")
async def get_car(car_id: int, user: Users = Depends(get_current_user)) -> SCars:

    car = await CarsDAO.find_by_id(car_id)
    if not car:
        raise CarNotFound
    if car.user_id != user.id:
        raise CarNotFound
    return car


@router.delete("/{car_id}", description="Удаление автомобиля")
async def delete_car(car_id: int, user: Users = Depends(get_current_user)):

    car = await CarsDAO.find_by_id(car_id)
    if not car:
        raise CarNotFound
    if car.user_id != user.id:
        raise CarNotFound
    await CarsDAO.delete_(id=car_id)


@router.put("/{car_id}", description="Изменение автомобиля")
async def update_car(car_id: int, car: SCars, user: Users = Depends(get_current_user)):

    already_car = await CarsDAO.find_by_number(car.number)
    if already_car:
        raise CarAlreadyExists
    match_ = re.match(number_pattern, car.number.upper())
    if not match_:
        raise InvalidCarNumber
    await CarsDAO.update_(model_id=car_id, name=car.name, number=car.number.upper())
