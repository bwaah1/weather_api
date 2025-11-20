from abc import ABC, abstractmethod

from app.domain.weather_log import WeatherLog


class LoggingRepository(ABC):
    @abstractmethod
    async def log(self, log_entry: WeatherLog) -> None:
        pass
