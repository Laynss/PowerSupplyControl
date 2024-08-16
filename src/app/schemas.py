"""Схемы источников питания."""

from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class ChannelNumber(BaseModel):
    """Схема номера канала питания."""

    number: Annotated[int, Query(ge=0)]


class Channel(BaseModel):
    """Схема канала питания."""

    number: Annotated[int, Query(ge=0)]
    voltage: float
    amperage: float
