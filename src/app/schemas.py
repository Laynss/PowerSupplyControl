from fastapi import Query
from pydantic import BaseModel
from typing import Annotated


class ChannelNumber(BaseModel):
    number: Annotated[int, Query(ge=0)]


class Channel(ChannelNumber):
    voltage: float
    amperage: float
