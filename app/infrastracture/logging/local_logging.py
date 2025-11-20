import json
from pathlib import Path

from app.domain.repositories.logging import LoggingRepository
from app.domain.weather_log import WeatherLog


class LocalLoggingRepository(LoggingRepository):
    def __init__(self, log_file: Path) -> None:
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    async def log(self, log_entry: WeatherLog) -> None:
        log_data = log_entry.model_dump(mode="json")

        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_data) + "\n")
