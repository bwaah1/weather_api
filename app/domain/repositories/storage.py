from abc import ABC, abstractmethod
from pathlib import Path

from app.domain.weather import Weather


class StorageRepository(ABC):
    @abstractmethod
    async def save(self, city: str, weather: Weather) -> Path:
        pass
