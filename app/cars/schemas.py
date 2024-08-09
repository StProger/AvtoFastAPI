from fastapi import Query
from typing import Annotated

from pydantic import BaseModel


class SCars(BaseModel):

    name: str
    number: Annotated[str, Query(max_length=6)]
