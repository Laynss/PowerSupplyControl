"""Тесты API."""

from unittest.mock import patch

import pytest
from httpx import AsyncClient

from app.schemas import Channel


@pytest.mark.asyncio
async def test_get_telemetry(ac:AsyncClient):
    channel = Channel(number=5, voltage=4, amperage=1)
    with patch('app.router.ps.is_connected', return_value=True):
         with patch('app.router.get_channel_info', return_value=channel):
            response = await ac.get("/channels/info/1")
    assert response.status_code == 200
    data = response.json()
    assert data == {'number': 5, 'amperage': 1.0,  'voltage': 4.0}


@pytest.mark.asyncio
async def test_turn_channel_on(ac:AsyncClient):
    response = await ac.post("channels/channel/on", json={"number": 1, "voltage": 0.0, "amperage": 0.0})
    assert response.status_code == 200
    data = response.json()
    assert data == f"status: Channel 1 turned on"


@pytest.mark.asyncio
async def test_turn_channel_off(ac:AsyncClient):
    with patch('app.router.ps.is_connected', return_value=True):
        response = await ac.post("channels/channel/off", json={"number": 1})
    assert response.status_code == 200
    data = response.json()
    assert data == f"status: Channel 1 turned off"


@pytest.mark.asyncio
async def test_turn_channel_on_invalid_data(ac:AsyncClient):
    response = await ac.post("/channel/on", json={"channel": 1, "voltage": "invalid", "amperage": 1.0})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_turn_channel_off_invalid_data(ac:AsyncClient):
    response = await ac.post("/channel/off", json={"channel": 1, "voltage": "invalid", "amperage": 1.0})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_channels_status(ac:AsyncClient):
    with patch('app.router.ps.is_connected', return_value=True):
        with patch('app.router.ps.query_all_channel_status', return_value={}):
            response = await ac.get("/channels/status")
    assert response.status_code == 200
 
