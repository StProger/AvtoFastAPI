from fastapi import APIRouter, Depends, Query

from fastapi_cache.decorator import cache

from typing import Annotated

from pydantic import parse_obj_as

import re

from asyncio import sleep

from app.cars.models import Cars
from app.cars.schemas import SCars
from app.cars.dao import CarsDAO
from app.exceptions import CarAlreadyExists, InvalidCarNumber, CarNotFound, InvalidPriceFilter
from app.users.models import Users
from app.users.dependencies import get_current_user


number_pattern = r'^[А-Я]\d{3}[А-Я]{2}$'

desc_name = "Название машины"
desc_number = "Номер машины"
desc_color = "Цвет машины"
desc_price = "Цена машины"

router = APIRouter(prefix="/cars", tags=["Cars"])


@router.post("", description="Добавление машины")
async def add_car(name: Annotated[str, Query(example="LADA", description=desc_name)],
                  number: Annotated[str, Query(pattern=number_pattern, example="У456ТН", description=desc_number)],
                  color: Annotated[str, Query(example="Чёрный", description=desc_color)],
                  price: Annotated[int, Query(example=100000, description=desc_price, gt=0)],
                  user: Users = Depends(get_current_user)):

    # match_ = re.match(number_pattern, number.upper())
    # if not match_:
    #     raise InvalidCarNumber

    already_car = await CarsDAO.find_by_number(number)
    if already_car:
        raise CarAlreadyExists
    await CarsDAO.add(name=name, number=number.upper(), user_id=user.id, color=color, price=price)


@router.get("", description="Получение машин")
@cache(expire=15)
async def get_cars(
        min_price: Annotated[int, Query(example=0, description="Минимальная цена", ge=0)] = None,
        max_price: Annotated[int, Query(example=100000, description="Максимальная цена", gt=0)] = None,
        # user: Users = Depends(get_current_user)
):
    if (min_price and max_price) and (min_price > max_price):
        raise InvalidPriceFilter

    filters = []
    if min_price:
        filters.append(Cars.price >= min_price)
    if max_price:
        filters.append(Cars.price <= max_price)
    cars = await CarsDAO.find_with_filters(*filters)
    cars_json = parse_obj_as(list[SCars], cars)
    return cars_json


@router.get("/my_cars", description="Получение всех машин пользователя")
@cache(expire=15)
async def get_cars(user: Users = Depends(get_current_user)):

    await sleep(2)
    cars = await CarsDAO.find_all(user_id=user.id)
    cars_json = parse_obj_as(list[SCars], cars)

    return cars_json


@router.get("/my_cars/{car_id}", description="Получение автомобиля пользователя")
@cache(expire=10)
async def get_car(car_id: int, user: Users = Depends(get_current_user)):

    await sleep(2)
    car = await CarsDAO.find_by_id(car_id)
    if not car:
        raise CarNotFound
    if car.user_id != user.id:
        raise CarNotFound
    car_json = parse_obj_as(SCars, {
        "name": car.name,
        "number": car.number,
        "color": car.color,
        "price": car.price
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


@router.put("/{car_id}", description="Изменение автомобиля")
async def update_car(car_id: int,
                     number: Annotated[str, Query(example="У456ТН", pattern=number_pattern, description=desc_number)],
                     color: Annotated[str, Query(example="Чёрный", description=desc_color)],
                     name: Annotated[str, Query(example="LADA", description=desc_name)],
                     price: Annotated[int, Query(example=100000, description=desc_price, gt=0)],
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

    await CarsDAO.update_(model_id=car_id, name=name, number=number.upper(), color=color, price=price)
