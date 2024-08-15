import datetime
import logging
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status

from .power_supply import PowerSupply
from .schemas import Channel, ChannelNumber
from .services import get_channel_info

load_dotenv()

power_supply_host = os.getenv("POWER_SUPPLY_HOST")
power_supply_port = os.getenv("POWER_SUPPLY_PORT")
ps = PowerSupply(host=power_supply_host, port=power_supply_port)

logging.basicConfig(filename='telemetry.log', level=logging.INFO, format='%(asctime)s - %(message)s')

router = APIRouter(prefix='/channels', tags=['Источник питания'])


@router.get("/info/{channel_id}", response_model=Channel)
async def get_telemetry(channel_id: int):
    try:
        if not await ps.is_connected():
            await ps.connect()
        channel = await get_channel_info(channel_id)
        log_message = f"{datetime.datetime.now()} - Power supply channel: {channel.number}, Amperage: {channel.amperage}, Voltage: {channel.voltage}"
        logging.info(log_message)
        return channel
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/channel/on")
async def turn_channel_on(params: Channel) -> str:
    try:
        if not await ps.is_connected():
            await ps.connect()
        await ps.set_channel_voltage(params.number, params.voltage)
        await ps.set_channel_current(params.number, params.amperage)
        await ps.enable_channel_output(params.number)
        return f"status: Channel {params.number} turned on"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/channel/off")
async def turn_channel_off(channel: ChannelNumber) -> str:
    try:
        if not await ps.is_connected():
            await ps.connect()
        await ps.disable_channel_output(channel)
        return f"status: Channel {channel.number} turned off"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/status", response_model=list[Channel])
async def get_channels_status():
    try:
        if not await ps.is_connected():
            await ps.connect()
        status = await ps.query_all_channel_status()
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
