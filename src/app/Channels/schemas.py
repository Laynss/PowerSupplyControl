from fastapi import Query
from pydantic import BaseModel
from typing import Annotated


class Channel(BaseModel):
    number: Annotated[int, Query(ge=0)] 
    voltage: Annotated[int, Query(ge=0)] 
    amperage: Annotated[int, Query(ge=0)]

class ChannelNumber(BaseModel):
    number: Annotated[int, Query(ge=0)] 