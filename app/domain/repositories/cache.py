from abc import ABC, abstractmethod

from app.domain.cache_entry import CacheEntry
from app.domain.weather import Weather


class CacheRepository(ABC):
    @abstractmethod
    async def get(self, city: str) -> CacheEntry | None:
        pass

    @abstractmethod
    async def set(self, city: str, weather: Weather) -> None:
        pass
