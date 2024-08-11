from fastapi import Query
from typing import Annotated

from pydantic import BaseModel, Field


class SCars(BaseModel):

    name: str
    number: str
    color: str
    price: int
