from datetime import UTC, datetime
from pathlib import Path

from app.domain.repositories.cache import CacheRepository
from app.domain.repositories.logging import LoggingRepository
from app.domain.repositories.storage import StorageRepository
from app.domain.weather import Weather
from app.domain.weather_log import WeatherLog
from app.infrastracture.external.weather_client import WeatherAPIClient
from app.schemas import WeatherResponse


class WeatherService:
    def __init__(
        self,
        weather_client: WeatherAPIClient,
        cache_repository: CacheRepository,
        storage_repository: StorageRepository,
        logging_repository: LoggingRepository,
    ) -> None:
        self.weather_client = weather_client
        self.cache_repository = cache_repository
        self.storage_repository = storage_repository
        self.logging_repository = logging_repository

    async def get_weather(self, city: str) -> WeatherResponse:
        cached_entry = await self.cache_repository.get(city)
        if cached_entry:
            weather = cached_entry.weather
            await self._save_and_log(city, weather, success=True)
            return WeatherResponse.model_validate(weather)

        try:
            weather = await self.weather_client.get_weather(city)
            await self.cache_repository.set(city, weather)
            await self._save_and_log(city, weather, success=True)
            return WeatherResponse.model_validate(weather)
        except Exception as e:
            error_message = str(e)
            await self._save_and_log(
                city, None, success=False, error_message=error_message
            )
            raise

    async def _save_and_log(
        self,
        city: str,
        weather: Weather | None,
        success: bool,
        error_message: str | None = None,
    ) -> Path | None:
        file_path = None
        if weather and success:
            file_path = await self.storage_repository.save(city, weather)

        log_entry = WeatherLog(
            city=city,
            timestamp=datetime.now(UTC),
            file_path=str(file_path) if file_path else "",
            success=success,
            error_message=error_message,
        )
        await self.logging_repository.log(log_entry)

        return file_path
