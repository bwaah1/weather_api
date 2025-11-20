from datetime import datetime

from pydantic import BaseModel, field_serializer


class WeatherResponse(BaseModel):
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

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> str:
        return value.isoformat()

    model_config = {
        "from_attributes": True,
    }
