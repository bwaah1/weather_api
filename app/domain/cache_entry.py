from datetime import UTC, datetime, timedelta

from pydantic import BaseModel

from app.domain.weather import Weather


class CacheEntry(BaseModel):
    city: str
    weather: Weather
    cached_at: datetime

    def is_expired(self, expiry_minutes: int = 5) -> bool:
        expiry_time = self.cached_at + timedelta(minutes=expiry_minutes)
        return datetime.now(UTC) > expiry_time
