import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_get_weather_endpoint(client, sample_weather):
    response = client.get("/api/weather/?city=Kyiv")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["city"] == "Kyiv"
    assert data["temperature"] == 20.5
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_get_weather_endpoint_missing_city(client):
    response = client.get("/api/weather/")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_weather_endpoint_error(app):
    from fastapi.testclient import TestClient
    from unittest.mock import AsyncMock

    mock_client = AsyncMock()
    mock_client.get_weather = AsyncMock(side_effect=Exception("API Error"))
    
    service = app.state.weather_service
    service.weather_client = mock_client

    client = TestClient(app)
    response = client.get("/api/weather/?city=InvalidCity")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "detail" in response.json()

