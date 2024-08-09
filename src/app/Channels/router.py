from fastapi import APIRouter, HTTPException, Query
from typing import Annotated

from app.Channels.schemas import Channel, ChannelNumber

router = APIRouter(prefix='/channels', tags=['Источник питания'])

@router.get("/info/{channel_id}", response_model=Channel)
async def get_telemetry(channel_id:int):
    try:
        return 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/turn/on")
async def turn_channel_on(params: Channel):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("//turn/off")
async def turn_channel_off(channel: ChannelNumber):
    try:
        return {"status": f"Channel {channel.number} turned off"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status", response_model=list[Channel])
async def get_channels_status():
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))