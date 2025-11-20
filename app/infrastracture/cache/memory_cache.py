from datetime import UTC, datetime

from app.domain.cache_entry import CacheEntry
from app.domain.repositories.cache import CacheRepository
from app.domain.weather import Weather


class MemoryCacheRepository(CacheRepository):
    def __init__(self, expiry_minutes: int = 5) -> None:
        self._cache: dict[str, CacheEntry] = {}
        self.expiry_minutes = expiry_minutes

    async def get(self, city: str) -> CacheEntry | None:
        entry = self._cache.get(city.lower())
        if entry and not entry.is_expired(self.expiry_minutes):
            return entry
        if entry:
            del self._cache[city.lower()]
        return None

    async def set(self, city: str, weather: Weather) -> None:
        entry = CacheEntry(
            city=city.lower(),
            weather=weather,
            cached_at=datetime.now(UTC),
        )
        self._cache[city.lower()] = entry
