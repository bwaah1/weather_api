from datetime import datetime

from pydantic import BaseModel


class WeatherLog(BaseModel):
    city: str
    timestamp: datetime
    file_path: str
    success: bool = True
    error_message: str | None = None
