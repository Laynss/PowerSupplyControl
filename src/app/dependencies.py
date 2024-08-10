from fastapi import HTTPException, status, Depends

from .schemas import Channel
from .services import send_scpi_command, get_channel_info


async def valid_channel_by_id(channel_id: int) -> Channel:
    try:
        channel = await send_scpi_command(f"INFO:{channel_id}")
        channel = channel_id # здесь присвоил просто чтоб ошибки не было, так как мок
        if not channel:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
        channel = await get_channel_info(channel_id) 
        return channel
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
