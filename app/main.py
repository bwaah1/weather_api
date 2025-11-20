from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api import get_router
from app.domain.repositories.storage import StorageRepository
from app.infrastracture.cache.memory_cache import MemoryCacheRepository
from app.infrastracture.external.weather_client import WeatherAPIClient
from app.infrastracture.logging.local_logging import LocalLoggingRepository
from app.infrastracture.storage.factory_storage import factory_storage_repository
from app.infrastracture.storage.local_storage import LocalStorageRepository
from app.infrastracture.storage.s3_storage import S3StorageRepository
from app.services.weather_service import WeatherService
from app.settings import StorageType, settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    weather_client = WeatherAPIClient(api_key=settings.openweather_api_key)
    cache_repository = MemoryCacheRepository(
        expiry_minutes=settings.cache_expiry_minutes
    )
    storage_repository = factory_storage_repository(settings.storage_type)
    logging_repository = LocalLoggingRepository(log_file=settings.log_file)

    weather_service = WeatherService(
        weather_client=weather_client,
        cache_repository=cache_repository,
        storage_repository=storage_repository,
        logging_repository=logging_repository,
    )

    app.state.weather_service = weather_service

    yield

    await weather_client.close()


def get_app() -> FastAPI:
    app = FastAPI(
        title="Weather API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(get_router(), prefix="/api")

    return app


def main() -> None:
    uvicorn.run(
        "app.main:get_app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.server_reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


app = get_app()


if __name__ == "__main__":
    main()
