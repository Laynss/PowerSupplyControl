"""Сервисы."""

from fastapi import HTTPException, status

from .power_supply import PowerSupply
from .schemas import Channel


async def get_channel_info(ps: PowerSupply, channel_id: int) -> Channel:
    """Получить информацию об источнике питания."""

    voltage = ps.query_voltage(channel_id)
    amperage = ps.query_current(channel_id)
    channel = Channel
    channel.number = channel_id
    channel.voltage = voltage
    channel.amperage = amperage
    return channel
