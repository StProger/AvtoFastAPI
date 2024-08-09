from fastapi import APIRouter, Depends

from fastapi_cache.decorator import cache

from pydantic import parse_obj_as

import re

from asyncio import sleep

from app.cars.schemas import SCars
from app.cars.dao import CarsDAO
from app.exceptions import CarAlreadyExists, InvalidCarNumber, CarNotFound
from app.users.models import Users
from app.users.dependencies import get_current_user


number_pattern = r'^[А-Я]\d{3}[А-Я]{2}$'

router = APIRouter(prefix="/cars", tags=["cars"])


@router.post("", description="Добавление машины")
async def add_car(name: str,
                  number: str,
                  color: str,
                  user: Users = Depends(get_current_user)):

    match_ = re.match(number_pattern, number.upper())
    if not match_:
        raise InvalidCarNumber

    already_car = await CarsDAO.find_by_number(number)
    if already_car:
        raise CarAlreadyExists
    await CarsDAO.add(name=name, number=number.upper(), user_id=user.id, color=color)
    print("Добавил машину")


@router.get("", description="Получение всех машин")
@cache(expire=15)
async def get_cars(user: Users = Depends(get_current_user)):

    await sleep(2)
    cars = await CarsDAO.find_all(user_id=user.id)
    cars_json = parse_obj_as(list[SCars], cars)
    print(f"Получил все машины: {cars}")

    return cars_json


@router.get("/{car_id}", description="Получение автомобиля")
@cache(expire=10)
async def get_car(car_id: int, user: Users = Depends(get_current_user)):

    await sleep(2)
    car = await CarsDAO.find_by_id(car_id)
    if not car:
        raise CarNotFound
    if car.user_id != user.id:
        raise CarNotFound
    print(f"Получил машину: {car}")
    car_json = parse_obj_as(SCars, {
        "name": car.name,
        "number": car.number,
        "color": car.color
    })
    return car_json


@router.delete("/{car_id}", description="Удаление автомобиля")
async def delete_car(car_id: int, user: Users = Depends(get_current_user)):

    car = await CarsDAO.find_by_id(car_id)
    if not car:
        raise CarNotFound
    if car.user_id != user.id:
        raise CarNotFound
    await CarsDAO.delete_(id=car_id)
    print(f"Удалил автомобиль: {car_id}")


@router.put("/{car_id}", description="Изменение автомобиля")
async def update_car(car_id: int,
                     number: str,
                     color: str,
                     name: str,
                     user: Users = Depends(get_current_user)):

    car = await CarsDAO.find_by_id(car_id)

    if not car or car.user_id != user.id:
        raise CarNotFound

    already_car = await CarsDAO.find_by_number(number)

    if already_car:
        raise CarAlreadyExists

    match_ = re.match(number_pattern, number.upper())

    if not match_:
        raise InvalidCarNumber

    await CarsDAO.update_(model_id=car_id, name=name, number=number.upper(), color=color)
    print(f"Обновил автомобиль: {car.name} -> {name}")
