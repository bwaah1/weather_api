from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.domain.cache_entry import CacheEntry
from app.domain.weather import Weather
from app.infrastracture.cache.memory_cache import MemoryCacheRepository
from app.infrastracture.external.weather_client import WeatherAPIClient
from app.infrastracture.logging.local_logging import LocalLoggingRepository
from app.infrastracture.storage.local_storage import LocalStorageRepository
from app.main import get_app
from app.services.weather_service import WeatherService


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def sample_weather_data():
    return {
        "name": "Kyiv",
        "main": {
            "temp": 20.5,
            "humidity": 65,
            "pressure": 1013,
        },
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 3.2},
        "coord": {"lat": 50.4501, "lon": 30.5234},
        "sys": {"country": "UA"},
    }


@pytest.fixture
def sample_weather():
    return Weather(
        city="Kyiv",
        temperature=20.5,
        description="clear sky",
        humidity=65,
        pressure=1013,
        wind_speed=3.2,
        timestamp=datetime.now(UTC),
        country="UA",
        latitude=50.4501,
        longitude=30.5234,
    )


@pytest.fixture
def mock_weather_client(sample_weather):
    client = AsyncMock(spec=WeatherAPIClient)
    client.get_weather = AsyncMock(return_value=sample_weather)
    client.close = AsyncMock()
    return client


@pytest.fixture
def cache_repository():
    return MemoryCacheRepository(expiry_minutes=5)


@pytest.fixture
def storage_repository(temp_dir):
    data_dir = temp_dir / "data"
    return LocalStorageRepository(data_dir=data_dir)


@pytest.fixture
def logging_repository(temp_dir):
    log_file = temp_dir / "logs" / "weather.log"
    return LocalLoggingRepository(log_file=log_file)


@pytest.fixture
def weather_service(mock_weather_client, cache_repository, storage_repository, logging_repository):
    return WeatherService(
        weather_client=mock_weather_client,
        cache_repository=cache_repository,
        storage_repository=storage_repository,
        logging_repository=logging_repository,
    )


@pytest.fixture
def app(weather_service):
    from contextlib import asynccontextmanager
    from fastapi import FastAPI
    
    test_app = FastAPI(title="Weather API Test", version="1.0.0")
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
    
    test_app.router.lifespan_context = lifespan
    test_app.state.weather_service = weather_service
    
    from app.api import get_router
    test_app.include_router(get_router(), prefix="/api")
    
    return test_app


@pytest.fixture
def client(app):
    return TestClient(app)

