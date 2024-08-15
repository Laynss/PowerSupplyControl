import pytest
from httpx import AsyncClient

from main import app


@pytest.mark.asyncio
async def test_get_telemetry(ac:AsyncClient):
    response = await ac.get("/channels/info/1")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 1
    assert data["amperage"] == 0.0
    assert data["voltage"] == 0.0


@pytest.mark.asyncio
async def test_turn_channel_on(ac:AsyncClient):
    response = await ac.post("channels/channel/on", json={"number": 1, "voltage": 0.0, "amperage": 0.0})
    assert response.status_code == 200
    data = response.json()
    assert data == f"status: Channel 1 turned on"


@pytest.mark.asyncio
async def test_turn_channel_off(ac:AsyncClient):
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
    response = await ac.get("/channels/status")
    assert response.status_code == 200
    data = response.json()
    for channel in data:
        assert channel["number"] == 4
        assert channel["voltage"] == 0
        assert channel["amperage"] == 0
