from pydantic import BaseModel


class SCars(BaseModel):

    name: str
    number: str
