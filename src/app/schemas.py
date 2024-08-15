from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class ChannelNumber(BaseModel):
    number: Annotated[int, Query(ge=0)]


class Channel(BaseModel):
    number: Annotated[int, Query(ge=0)]
    voltage: float
    amperage: float
