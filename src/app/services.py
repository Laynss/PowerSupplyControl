from fastapi import HTTPException, status

from .schemas import Channel

async def send_scpi_command(params: str) -> None:
    # Мокаю, возвращаю None
    return None

    
async def get_channel_info(channel_id: int) -> Channel:
    voltage = await send_scpi_command(f"MEASURE{channel_id}:VOLTAGE?")
    amperage = await send_scpi_command(f"MEASURE{channel_id}:AMPERAGE?")
    channel: Channel = Channel
    channel.number = channel_id
    channel.voltage = voltage if voltage else 0
    channel.amperage = amperage if amperage else 0
    return channel