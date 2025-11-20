from datetime import datetime

from pydantic import BaseModel


class Weather(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    pressure: int
    wind_speed: float
    timestamp: datetime
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None
