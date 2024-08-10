from fastapi import APIRouter, HTTPException, status, Depends
import logging

from .schemas import Channel, ChannelNumber
from .dependencies import valid_channel_by_id
from .services import send_scpi_command, get_channel_info

logging.basicConfig(filename='telemetry.log', level=logging.INFO, format='%(asctime)s - %(message)s')

router = APIRouter(prefix='/channels', tags=['Источник питания'])


@router.get("/info/{channel_id}", response_model=Channel)
async def get_telemetry(channel: Channel = Depends(valid_channel_by_id)):
    logging.info(f"Telemetry channel: {channel.number}, Amperage: {channel.amperage}, Voltage: {channel.voltage}")
    return channel


@router.post("/channel/on")
async def turn_channel_on(params: Channel) -> str:
    try:
        await send_scpi_command(f"SOURCE{params.voltage}:AMPERAGE {params.voltage}")
        await send_scpi_command(f"SOURCE{params.amperage}:VOLTAGE {params.amperage}")
        await send_scpi_command(f"OUTPUT{params.number}:STATE ON")
        return f"status: Channel {params.number} turned on"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/channel/off")
async def turn_channel_off(channel: ChannelNumber) -> str:
    try:
        await send_scpi_command(f"OUTPUT{channel.number}:STATE OFF")
        return f"status: Channel {channel.number} turned off"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/status", response_model=list[Channel])
async def get_channels_status():
    try:
        status = []
        for channel_id in range(1, 5):  # Предполагаем, что у нас 4 канала
            channel = await get_channel_info(channel_id)
            status.append(channel)
        return status
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
